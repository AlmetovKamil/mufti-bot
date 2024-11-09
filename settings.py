import os

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
BACKEND_BASE_URL = os.getenv(
    "BACKEND_BASE_URL", "https://namazlive.herokuapp.com"
)
BACKEND_API_KEY = os.getenv("BACKEND_API_KEY")

# It is for choosing the most relevant question
GPT_RELEVANT_QUESTION_SYSTEM_MESSAGE = """
# GOAL
Your goal is to help a scholar to authentically answer questions on Hanafi Fiqh. 

We have a collection of previously answered questions. 
We will provide you a json with the question and the list of relevant questions.
The json will look the following:
{
    "question": <<question>>,
    "relevant_questions": [
        {
            "Auto_id": <<id>>,
            "question": <<relevant_question>>,
        }
    ]
}
Where <<question>> is the question that is being asked, 
<<id>> is an id (integer) of a relevant question,
<<relevant_question>> is a relevant question (also it might be a topic title) itself

You need to  choose exactly one of them and write only its id on the following format:
{
    "Auto_id": <<id>>,
}
<<id>> is the id you have chosen.

# DOs AND DONTs
- Choose the most relevant question only among provided relevant questions.
- Write the answer only in the specified format
"""
