import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import unittest
from unittest.mock import patch, MagicMock, mock_open
from src.app.transcript_extractor import YouTubeTranscriptExtractor


class TestYouTubeTranscriptExtractor(unittest.TestCase):

    def setUp(self):
        self.extractor = YouTubeTranscriptExtractor()

    def test_extract_video_id(self):
        urls = {
            "https://www.youtube.com/watch?v=dQw4w9WgXcQ": "dQw4w9WgXcQ",
            "https://youtu.be/dQw4w9WgXcQ": "dQw4w9WgXcQ",
            "https://www.youtube.com/embed/dQw4w9WgXcQ": "dQw4w9WgXcQ",
        }
        for url, expected_id in urls.items():
            self.assertEqual(self.extractor.extract_video_id(url), expected_id)

    @patch("src.app.transcript_extractor.YouTubeTranscriptApi")
    def test_get_transcript_youtube_api_success(self, mock_api):
        mock_api.get_transcript.return_value = [
            {"text": "hello world", "start": 0.0, "duration": 1.0}
        ]
        transcript = self.extractor.get_transcript_youtube_api("dQw4w9WgXcQ")
        self.assertIsNotNone(transcript)
        if transcript:
            self.assertEqual(transcript[0]["text"], "hello world")

    @patch("src.app.transcript_extractor.YouTubeTranscriptApi")
    def test_get_transcript_youtube_api_failure(self, mock_api):
        mock_api.get_transcript.side_effect = Exception("API Error")
        transcript = self.extractor.get_transcript_youtube_api("dQw4w9WgXcQ")
        self.assertIsNone(transcript)

    @patch("src.app.transcript_extractor.tempfile.TemporaryDirectory")
    @patch("src.app.transcript_extractor.os.listdir")
    @patch(
        "builtins.open",
        new_callable=mock_open,
        read_data="WEBVTT\n\n00:00:00.000 --> 00:00:01.000\nhello from ytdlp",
    )
    @patch("src.app.transcript_extractor.yt_dlp")
    def test_get_transcript_ytdlp_success(
        self, mock_ytdlp, mock_file, mock_listdir, mock_tempdir
    ):
        # Mock the temporary directory
        mock_temp_path = "/tmp/test"
        mock_tempdir.return_value.__enter__.return_value = mock_temp_path

        # Mock the yt-dlp instance
        mock_ydl_instance = MagicMock()
        mock_ydl_instance.extract_info.return_value = {
            "title": "Test Video",
            "duration": 60,
            "subtitles": {},
            "automatic_captions": {},
        }
        mock_ytdlp.YoutubeDL.return_value.__enter__.return_value = mock_ydl_instance

        # Mock file listing to return a VTT file
        mock_listdir.return_value = ["test_video.en.vtt"]

        transcript = self.extractor.get_transcript_ytdlp("dQw4w9WgXcQ")
        self.assertIsNotNone(transcript)
        if transcript:
            self.assertEqual(transcript[0]["text"], "hello from ytdlp")

    @patch("src.app.transcript_extractor.yt_dlp")
    def test_get_transcript_ytdlp_failure(self, mock_ytdlp):
        mock_ydl_instance = MagicMock()
        mock_ydl_instance.extract_info.side_effect = Exception("yt-dlp Error")
        mock_ytdlp.YoutubeDL.return_value.__enter__.return_value = mock_ydl_instance
        transcript = self.extractor.get_transcript_ytdlp("dQw4w9WgXcQ")
        self.assertIsNone(transcript)

    @patch(
        "src.app.transcript_extractor.YouTubeTranscriptExtractor.get_transcript_youtube_api"
    )
    @patch(
        "src.app.transcript_extractor.YouTubeTranscriptExtractor.get_transcript_ytdlp"
    )
    def test_extract_transcript_api_success(self, mock_ytdlp, mock_api):
        mock_api.return_value = [{"text": "api transcript"}]
        transcript, status = self.extractor.extract_transcript(
            "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
        )
        self.assertIsNotNone(transcript)
        self.assertIn("Success using YouTube Transcript API", status)
        mock_ytdlp.assert_not_called()

    @patch(
        "src.app.transcript_extractor.YouTubeTranscriptExtractor.get_transcript_youtube_api"
    )
    @patch(
        "src.app.transcript_extractor.YouTubeTranscriptExtractor.get_transcript_ytdlp"
    )
    def test_extract_transcript_fallback_to_ytdlp(self, mock_ytdlp, mock_api):
        mock_api.return_value = None
        mock_ytdlp.return_value = [{"text": "ytdlp transcript"}]
        transcript, status = self.extractor.extract_transcript(
            "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
        )
        self.assertIsNotNone(transcript)
        self.assertIn("Success using yt-dlp", status)

    def test_parse_vtt_content(self):
        vtt_content = """WEBVTT

00:00:00.000 --> 00:00:01.000
hello world

00:00:01.000 --> 00:00:02.000
this is a test"""

        transcript = self.extractor._parse_vtt_content(vtt_content)
        self.assertEqual(len(transcript), 2)
        self.assertEqual(transcript[0]["text"], "hello world")
        self.assertEqual(transcript[0]["start"], 0.0)
        self.assertEqual(transcript[1]["text"], "this is a test")
        self.assertEqual(transcript[1]["start"], 1.0)

    def test_parse_srt_content(self):
        srt_content = """1
00:00:00,000 --> 00:00:01,000
hello world

2
00:00:01,000 --> 00:00:02,000
this is a test"""

        transcript = self.extractor._parse_srt_content(srt_content)
        self.assertEqual(len(transcript), 2)
        self.assertEqual(transcript[0]["text"], "hello world")
        self.assertEqual(transcript[0]["start"], 0.0)
        self.assertEqual(transcript[1]["text"], "this is a test")
        self.assertEqual(transcript[1]["start"], 1.0)

    def test_parse_timestamp(self):
        # Test VTT timestamp parsing
        self.assertEqual(self.extractor._parse_timestamp("00:00:01.500"), 1.5)
        self.assertEqual(self.extractor._parse_timestamp("00:01:30.250"), 90.25)
        self.assertEqual(self.extractor._parse_timestamp("01:00:00.000"), 3600.0)

    def test_parse_srt_timestamp(self):
        # Test SRT timestamp parsing
        self.assertEqual(self.extractor._parse_srt_timestamp("00:00:01,500"), 1.5)
        self.assertEqual(self.extractor._parse_srt_timestamp("00:01:30,250"), 90.25)
        self.assertEqual(self.extractor._parse_srt_timestamp("01:00:00,000"), 3600.0)


if __name__ == "__main__":
    unittest.main()
