import re
import google.generativeai as genai
from src.config_manager import config_manager
from src.utils.logger import setup_logger

logger = setup_logger('llm_summarizer', 'logs/llm.log')

class LLMSummarizer:
    def __init__(self):
        api_key = config_manager.get("GEMINI_API_KEY")
        if api_key:
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel('models/gemma-4-31b-it')
        else:
            self.model = None
            logger.warning("GEMINI_API_KEY not found. LLM features will be disabled.")

    def analyze_opportunity(self, opportunity_data):
        if not self.model:
            return 50, "LLM analysis unavailable."

        prompt = f"""
Analyze the following career opportunity for a B.Tech CS student aspiring to be an AI/LLM Engineer.

Title: {opportunity_data.get('title')}
Company: {opportunity_data.get('company')}
Category: {opportunity_data.get('category')}
Description: {opportunity_data.get('description')}

Tasks:
1. Rate relevance from 0-100 based on the goal of becoming an AI/LLM Engineer.
2. Provide a 2-sentence summary of why it's useful or not.
3. Format your response exactly as:
Score: [number]
Summary: [text]
"""

        try:
            response = self.model.generate_content(prompt)
            text = response.text

            score_match = re.search(r'Score:\s*(\d+)', text)
            summary_match = re.search(r'Summary:\s*(.*)', text, re.DOTALL)

            score = int(score_match.group(1)) if score_match else 50
            summary = summary_match.group(1).strip() if summary_match else "No summary generated."

            return score, summary
        except Exception as e:
            logger.error(f"Error calling Gemini API: {e}")
            return 50, "Error during LLM analysis."

llm_summarizer = LLMSummarizer()
