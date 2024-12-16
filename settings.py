import os

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
BACKEND_BASE_URL = os.getenv(
    "BACKEND_BASE_URL", "https://namazlive.herokuapp.com"
)
BACKEND_API_KEY = os.getenv("BACKEND_API_KEY")

# It is for choosing relevant questions
GPT_SELECT_RELEVANT_QUESTIONS_SYSTEM_MESSAGE = """
# GOAL
Select knowledge base entries that are relevant to the user question.

## Instructions
- You will receive a JSON with an incoming user question and a list of semantically close entities from our knowledge base.
- Select all knowledge base entities that are relevant to the asked question and provide their IDs in the format:
  {
    "Auto_ids": [<<id1>>, <<id2>>, ...]
  }
- If no entities are relevant, return:
  {
    "Auto_ids": []
  }

## Key Points
- Pick entities that are more likely to contain the answer to the user question.
- Follow the specified format strictly.
"""

# It is for generating an answer using selected relevant questions
GPT_GENERATE_ANSWER_FROM_RELEVANT_QUESTIONS_SYSTEM_MESSAGE = """
# ЦЕЛЬ
Помочь ученому ответить на вопросы по ханафитскому фикху на основе предоставленных данных.

## Инструкции:
- Ты получаешь JSON-файл, содержащий новый вопрос от пользователя и похожие вопросы-ответы из нашей базы знаний.
- Если информации в похожих вопросах-ответах достаточно, то используй их для составления ответа на новый вопрос с указанием ссылок на использованные источники.
- Если информации в похожих вопросах-ответах недостаточно, напиши: «Не можем ответить на основе базы знаний».

## Ключевые моменты:
- Не добавляй вымышленные данные, используй информацию из базы знаний.
- Отвечайте на языке нового вопроса от пользователя.
-	Убедись, что ссылки на источники четко указаны в тексте.
"""
