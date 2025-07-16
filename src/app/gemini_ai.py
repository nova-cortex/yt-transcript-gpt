"""
Gemini AI Module.

This module provides the `GeminiAI` class, which interfaces with the Google
Generative AI API (Gemini). It includes methods for generating various types
of content based on a given transcript, such as summaries, key quotes, study
guides, Q&A, flashcards, and highlighted insights. It also provides a chat
functionality to interact with the transcript content.
"""

import google.generativeai as genai


class GeminiAI:
    """
    A class to interact with the Google Gemini AI model.

    This class handles the configuration of the API key and provides methods
    to generate various AI-powered content from a video transcript.
    """

    def __init__(self, api_key):
        """
        Initializes the GeminiAI class and configures the generative model.

        Args:
            api_key (str): The API key for the Google Gemini service.
        """
        if api_key:
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel("gemini-1.5-flash")
        else:
            self.model = None

    def is_configured(self):
        """
        Checks if the Gemini AI model is configured with an API key.

        Returns:
            bool: True if the model is configured, False otherwise.
        """
        return self.model is not None

    def generate_summary(self, transcript_text):
        """
        Generates a comprehensive summary of the transcript.

        Args:
            transcript_text (str): The text of the video transcript.

        Returns:
            str: The generated summary, or an error message on failure.
        """
        prompt = f"""
        Please provide a comprehensive summary of the following video transcript:
        
        {transcript_text}
        
        Include:
        1. Main topics discussed
        2. Key points and insights
        3. Important conclusions or takeaways
        
        Keep the summary clear and well-structured.
        """

        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Error generating summary: {str(e)}"

    def extract_key_quotes(self, transcript_text):
        """
        Extracts key quotes from the transcript.

        Args:
            transcript_text (str): The text of the video transcript.

        Returns:
            str: The extracted key quotes, or an error message on failure.
        """
        prompt = f"""
        From the following transcript, extract 5-10 of the most important and impactful quotes:
        
        {transcript_text}
        
        Format each quote as:
        "Quote text" - [Approximate timestamp if available]
        
        Focus on quotes that:
        - Capture main ideas
        - Are memorable or impactful
        - Represent key insights
        """

        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Error extracting quotes: {str(e)}"

    def create_study_guide(self, transcript_text):
        """
        Creates a study guide from the transcript.

        Args:
            transcript_text (str): The text of the video transcript.

        Returns:
            str: The generated study guide, or an error message on failure.
        """
        prompt = f"""
        Create a comprehensive study guide from this video transcript:
        
        {transcript_text}
        
        Structure the study guide with:
        1. Main Topics/Chapters
        2. Key Concepts and Definitions
        3. Important Facts and Figures
        4. Study Questions
        5. Review Points
        
        Make it suitable for learning and revision.
        """

        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Error creating study guide: {str(e)}"

    def generate_qa(self, transcript_text):
        """
        Generates a Q&A session from the transcript.

        Args:
            transcript_text (str): The text of the video transcript.

        Returns:
            str: The generated Q&A, or an error message on failure.
        """
        prompt = f"""
        Create a Q&A session based on this video transcript:
        
        {transcript_text}
        
        Generate 10-15 relevant questions and provide detailed answers based on the content.
        Format as:
        
        Q: [Question]
        A: [Answer]
        
        Include a mix of factual, analytical, and conceptual questions.
        """

        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Error generating Q&A: {str(e)}"

    def create_flashcards(self, transcript_text):
        """
        Creates flashcards from the transcript.

        Args:
            transcript_text (str): The text of the video transcript.

        Returns:
            str: The generated flashcards, or an error message on failure.
        """
        prompt = f"""
        Create 15-20 flashcards from this video transcript:
        
        {transcript_text}
        
        Format each flashcard as:
        FRONT: [Question/Term]
        BACK: [Answer/Definition]
        ---
        
        Focus on key concepts, definitions, and important facts that would be useful for memorization.
        """

        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Error creating flashcards: {str(e)}"

    def highlight_insights(self, transcript_text):
        """
        Extracts key insights and highlights from the transcript.

        Args:
            transcript_text (str): The text of the video transcript.

        Returns:
            str: The extracted insights, or an error message on failure.
        """
        prompt = f"""
        Analyze this video transcript and extract the key insights and highlights:
        
        {transcript_text}
        
        Provide:
        1. 🔍 Key Insights (3-5 main insights)
        2. 💡 Important Revelations
        3. 📊 Data/Statistics mentioned
        4. 🎯 Actionable takeaways
        5. 🔗 Connections to broader topics
        
        Use emojis and clear formatting for easy reading.
        """

        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Error extracting insights: {str(e)}"

    def chat_with_transcript(self, transcript_text, question):
        """
        Allows chatting with the transcript content.

        Args:
            transcript_text (str): The text of the video transcript.
            question (str): The user's question about the transcript.

        Returns:
            str: The AI-generated answer, or an error message on failure.
        """
        prompt = f"""
        Based on this video transcript:
        
        {transcript_text}
        
        User Question: {question}
        
        Please provide a detailed answer based on the transcript content. If the question cannot be answered from the transcript, please mention that clearly.
        """

        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Error in chat: {str(e)}"
