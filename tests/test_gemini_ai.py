import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import unittest
from unittest.mock import patch, MagicMock
from src.app.gemini_ai import GeminiAI


class TestGeminiAI(unittest.TestCase):

    @patch("src.app.gemini_ai.genai.GenerativeModel")
    @patch("src.app.gemini_ai.genai.configure")
    def setUp(self, mock_configure, mock_model):
        self.api_key = "test_api_key"
        self.gemini_ai = GeminiAI(api_key=self.api_key)
        self.transcript_text = "This is a test transcript."
        self.mock_model = mock_model

    @patch("src.app.gemini_ai.genai.GenerativeModel")
    def test_initialization(self, mock_model):
        self.assertIsNotNone(self.gemini_ai.model)

        gemini_ai_no_key = GeminiAI(api_key=None)
        self.assertIsNone(gemini_ai_no_key.model)

    def test_is_configured(self):
        self.assertTrue(self.gemini_ai.is_configured())

        gemini_ai_no_key = GeminiAI(api_key=None)
        self.assertFalse(gemini_ai_no_key.is_configured())

    def test_generate_summary_success(self):
        self.mock_model.return_value.generate_content.return_value = MagicMock(
            text="This is a summary."
        )
        summary = self.gemini_ai.generate_summary(self.transcript_text)
        self.assertEqual(summary, "This is a summary.")

    def test_generate_summary_failure(self):
        self.mock_model.return_value.generate_content.side_effect = Exception(
            "API Error"
        )

        summary = self.gemini_ai.generate_summary(self.transcript_text)
        self.assertIn("Error generating summary", summary)

    def test_chat_with_transcript_success(self):
        self.mock_model.return_value.generate_content.return_value = MagicMock(
            text="This is an answer."
        )
        answer = self.gemini_ai.chat_with_transcript(
            self.transcript_text, "What is this?"
        )
        self.assertEqual(answer, "This is an answer.")


if __name__ == "__main__":
    unittest.main()
