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

# It is for choosing the most relevant question
GPT_GENERATE_ANSWER_SYSTEM_MESSAGE = """
# GOAL
Your goal is to help a scholar to authentically answer questions on Hanafi Fiqh. 

We have a collection of previously answered questions. Previously, you have already chosen the most relevant among them. 
We will provide you a json with the question that is being asked the most relevant question you have chosen before.
The json will look the following:
{
    "question": <<question>>,
    "relevant_question": {
            "Auto_id": <<id>>,
            "question": <<relevant_question>>,
            "answer": <<answer>>,
            "link": <<link>>
    }
}
Where <<question>> is the question that is being asked, 
<<id>> is an id (integer) of the most relevant question,
<<relevant_question>> is the most relevant question (also it might be a topic title) itself,
<<answer>> is the answer to the most relevant question,
<<link>> is the source from which the most relevant question is taken.

You need to answer the question that is being asked based on the most relevant question.


# DOs AND DONTs
- Don't make things up, use only the information that you obtained from the most relevant question.
- Answer in the language of the question asked.
- The answer should be concrete and concise.
"""
