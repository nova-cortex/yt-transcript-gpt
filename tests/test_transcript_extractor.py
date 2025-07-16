import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import unittest
from unittest.mock import patch, MagicMock
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

    @patch("src.app.transcript_extractor.yt_dlp")
    def test_get_transcript_ytdlp_success(self, mock_ytdlp):
        mock_ydl_instance = MagicMock()
        mock_ydl_instance.extract_info.return_value = {
            "subtitles": {"en": [{"ext": "vtt", "url": "..."}]}
        }
        mock_ytdlp.YoutubeDL.return_value.__enter__.return_value = mock_ydl_instance

        with patch.object(
            self.extractor,
            "_process_ytdlp_subtitles",
            return_value=[{"text": "hello from ytdlp"}],
        ):
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


if __name__ == "__main__":
    unittest.main()
