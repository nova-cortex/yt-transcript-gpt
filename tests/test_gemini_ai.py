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
        self.mock_model_instance = MagicMock()
        mock_model.return_value = self.mock_model_instance
        self.gemini_ai = GeminiAI(api_key=self.api_key)
        self.transcript_text = "This is a test transcript."

    def test_initialization_with_key(self):
        with patch("src.app.gemini_ai.genai.configure") as mock_configure, patch(
            "src.app.gemini_ai.genai.GenerativeModel"
        ) as mock_model:

            gemini_ai = GeminiAI(api_key="test_key")
            mock_configure.assert_called_once_with(api_key="test_key")
            mock_model.assert_called_once_with("gemini-1.5-flash")
            self.assertIsNotNone(gemini_ai.model)

    def test_initialization_without_key(self):
        gemini_ai_no_key = GeminiAI(api_key=None)
        self.assertIsNone(gemini_ai_no_key.model)

    def test_is_configured(self):
        self.assertTrue(self.gemini_ai.is_configured())

        gemini_ai_no_key = GeminiAI(api_key=None)
        self.assertFalse(gemini_ai_no_key.is_configured())

    def test_generate_summary_success(self):
        mock_response = MagicMock()
        mock_response.text = "This is a summary."
        self.mock_model_instance.generate_content.return_value = mock_response

        summary = self.gemini_ai.generate_summary(self.transcript_text)
        self.assertEqual(summary, "This is a summary.")
        self.mock_model_instance.generate_content.assert_called_once()

    def test_generate_summary_failure(self):
        self.mock_model_instance.generate_content.side_effect = Exception("API Error")

        summary = self.gemini_ai.generate_summary(self.transcript_text)
        self.assertIn("Error generating summary", summary)
        self.assertIn("API Error", summary)

    def test_extract_key_quotes_success(self):
        mock_response = MagicMock()
        mock_response.text = "These are key quotes."
        self.mock_model_instance.generate_content.return_value = mock_response

        quotes = self.gemini_ai.extract_key_quotes(self.transcript_text)
        self.assertEqual(quotes, "These are key quotes.")

    def test_extract_key_quotes_failure(self):
        self.mock_model_instance.generate_content.side_effect = Exception("API Error")

        quotes = self.gemini_ai.extract_key_quotes(self.transcript_text)
        self.assertIn("Error extracting quotes", quotes)

    def test_create_study_guide_success(self):
        mock_response = MagicMock()
        mock_response.text = "This is a study guide."
        self.mock_model_instance.generate_content.return_value = mock_response

        study_guide = self.gemini_ai.create_study_guide(self.transcript_text)
        self.assertEqual(study_guide, "This is a study guide.")

    def test_create_study_guide_failure(self):
        self.mock_model_instance.generate_content.side_effect = Exception("API Error")

        study_guide = self.gemini_ai.create_study_guide(self.transcript_text)
        self.assertIn("Error creating study guide", study_guide)

    def test_generate_qa_success(self):
        mock_response = MagicMock()
        mock_response.text = "Q: Test question?\nA: Test answer."
        self.mock_model_instance.generate_content.return_value = mock_response

        qa = self.gemini_ai.generate_qa(self.transcript_text)
        self.assertEqual(qa, "Q: Test question?\nA: Test answer.")

    def test_generate_qa_failure(self):
        self.mock_model_instance.generate_content.side_effect = Exception("API Error")

        qa = self.gemini_ai.generate_qa(self.transcript_text)
        self.assertIn("Error generating Q&A", qa)

    def test_create_flashcards_success(self):
        mock_response = MagicMock()
        mock_response.text = "FRONT: Test term\nBACK: Test definition\n---"
        self.mock_model_instance.generate_content.return_value = mock_response

        flashcards = self.gemini_ai.create_flashcards(self.transcript_text)
        self.assertEqual(flashcards, "FRONT: Test term\nBACK: Test definition\n---")

    def test_create_flashcards_failure(self):
        self.mock_model_instance.generate_content.side_effect = Exception("API Error")

        flashcards = self.gemini_ai.create_flashcards(self.transcript_text)
        self.assertIn("Error creating flashcards", flashcards)

    def test_highlight_insights_success(self):
        mock_response = MagicMock()
        mock_response.text = "🔍 Key Insights: Test insights"
        self.mock_model_instance.generate_content.return_value = mock_response

        insights = self.gemini_ai.highlight_insights(self.transcript_text)
        self.assertEqual(insights, "🔍 Key Insights: Test insights")

    def test_highlight_insights_failure(self):
        self.mock_model_instance.generate_content.side_effect = Exception("API Error")

        insights = self.gemini_ai.highlight_insights(self.transcript_text)
        self.assertIn("Error extracting insights", insights)

    def test_chat_with_transcript_success(self):
        mock_response = MagicMock()
        mock_response.text = "This is an answer."
        self.mock_model_instance.generate_content.return_value = mock_response

        answer = self.gemini_ai.chat_with_transcript(
            self.transcript_text, "What is this?"
        )
        self.assertEqual(answer, "This is an answer.")

    def test_chat_with_transcript_failure(self):
        self.mock_model_instance.generate_content.side_effect = Exception("API Error")

        answer = self.gemini_ai.chat_with_transcript(
            self.transcript_text, "What is this?"
        )
        self.assertIn("Error in chat", answer)


if __name__ == "__main__":
    unittest.main()
