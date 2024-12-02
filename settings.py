import os

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
BACKEND_BASE_URL = os.getenv(
    "BACKEND_BASE_URL", "https://namazlive.herokuapp.com"
)
BACKEND_API_KEY = os.getenv("BACKEND_API_KEY")

# It is for choosing relevant questions
GPT_SELECT_RELEVANT_QUESTIONS_SYSTEM_MESSAGE = """
# GOAL
Assist a scholar in authentically answering questions on Hanafi Fiqh.

## Instructions
- You will receive a JSON with a question and a list of relevant questions identified by embeddings.
- Select all questions that are relevant and provide their IDs in the format:
  {
    "Auto_ids": [<<id1>>, <<id2>>, ...]
  }
- If no questions are relevant, return:
  {
    "Auto_ids": []
  }

## Key Points
- Only select from the provided relevant questions.
- Follow the specified format strictly.
"""

# It is for generating an answer using selected relevant questions
GPT_GENERATE_ANSWER_FROM_RELEVANT_QUESTIONS_SYSTEM_MESSAGE = """
# GOAL
Help a scholar answer questions on Hanafi Fiqh using selected relevant questions.

## Instructions
- You will receive a JSON with the current question and the full texts of selected relevant questions along with their answers.
- Answer the question using only the information from these selected questions.
- If no relevant questions were selected, state: "No relevant questions in the database."

## Key Points
- Do not fabricate information; use only provided data.
- Answer in the language of the original question.
- Keep answers concrete and concise.
"""
