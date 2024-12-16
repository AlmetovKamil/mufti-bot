import telebot
from telebot import types
import requests
import os
import json

from settings import (
    TELEGRAM_BOT_TOKEN,
    GPT_SELECT_RELEVANT_QUESTIONS_SYSTEM_MESSAGE,
    GPT_GENERATE_ANSWER_FROM_RELEVANT_QUESTIONS_SYSTEM_MESSAGE,
)
import api


bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

state = {}


@bot.message_handler(commands=["start", "help"])
def send_welcome(message):
    state[message.chat.id] = {}
    bot.reply_to(message, "Этот бот - помощник муфтия-ханафита.")


@bot.message_handler(commands=["relevant_documents", "ask_question"])
def relevant_documents1(message: types.Message):
    if message.chat.id not in state:
        state[message.chat.id] = {}
    state[message.chat.id]["command"] = message.text.strip("/")
    bot.send_message(message.chat.id, "Пожалуста, напишите свой вопрос:")
    bot.register_next_step_handler(message, relevant_documents2)


def relevant_documents2(message):
    bot.send_chat_action(message.chat.id, "typing")
    message_text = message.text
    state[message.chat.id]["question"] = message_text
    result_json = api.relevant_documents(message_text)
    relevant_questions = ""
    relevant_questions_json = []
    for i in result_json["data"]:
        relevant_questions_json.append(
            {
                "Auto_id": i["Auto_id"],
                "question": i["question"],
            }
        )
        relevant_questions += "Question: " + i["question"] + ". "
        relevant_questions += "Link: " + i["link"] + "\n"
        if "answer" in i:
            relevant_questions += "Answer: " + i["answer"] + "\n"
        relevant_questions += "\n"
    bot.send_message(message.chat.id, "Нашел похожие вопросы из базы знаний, сейчас попробую отработать.")
    state[message.chat.id]["relevant_questions"] = relevant_questions
    state[message.chat.id]["relevant_questions_json"] = relevant_questions_json
    if state[message.chat.id]["command"] == "ask_question":
        answer_question(message)
    else:
        bot.send_message(message.chat.id, relevant_questions)
        state[message.chat.id]["command"] = None


def answer_question(message):
    bot.send_chat_action(message.chat.id, "typing")
    question = state[message.chat.id]["question"]
    relevant_questions_json = state[message.chat.id]["relevant_questions_json"]
    user_message = {
        "question": question,
        "relevant_questions": relevant_questions_json,
    }
    gpt_answer = api.query_gpt(
        user_message=json.dumps(user_message),
        system_message=GPT_SELECT_RELEVANT_QUESTIONS_SYSTEM_MESSAGE,
    )
    relevant_question_ids = json.loads(gpt_answer)["Auto_ids"]
    
    if not relevant_question_ids:
        bot.send_message(
            message.chat.id,
            "No relevant questions found in the database."
        )
        state[message.chat.id]["command"] = None
        return
    
    documents = []
    for question_id in relevant_question_ids:
        document = api.specific_document_from_knowledgebase(question_id)
        documents.append(document)
    
    # Send the list of chosen relevant questions
    relevant_question_titles = "\n".join(
        [f"Question: {doc['question']}\nLink: {doc['link']}\n" for doc in documents]
    )

    bot.send_message(
        message.chat.id,
        "Вот эти вопросы были выбраны как наиболее релевантные:\n" + relevant_question_titles
    )
    
    bot.send_chat_action(message.chat.id, "typing")
    user_message2 = {
        "question": question,
        "relevant_questions": documents,
    }
    gpt_answer = api.query_gpt(
        user_message=json.dumps(user_message2),
        system_message=GPT_GENERATE_ANSWER_FROM_RELEVANT_QUESTIONS_SYSTEM_MESSAGE,
    )
    bot.send_message(message.chat.id, gpt_answer, parse_mode="Markdown",)
    state[message.chat.id]["command"] = None


bot.infinity_polling()
