import telebot
from telebot import types
import requests
import os
import json

from settings import (
    TELEGRAM_BOT_TOKEN,
    GPT_RELEVANT_QUESTION_SYSTEM_MESSAGE,
    GPT_GENERATE_ANSWER_SYSTEM_MESSAGE,
)
import api


bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

state = {}


@bot.message_handler(commands=["start", "help"])
def send_welcome(message):
    state[message.chat.id] = {}
    bot.reply_to(message, "This bot is mufti helper bot")


@bot.message_handler(commands=["relevant_documents", "ask_question"])
def relevant_documents1(message: types.Message):
    if message.chat.id not in state:
        state[message.chat.id] = {}
    state[message.chat.id]["command"] = message.text.strip("/")
    bot.send_message(message.chat.id, "Please, ask your question:")
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
        relevant_questions += "Question: " + i["question"] + "\n"
        relevant_questions += "Link: " + i["link"] + "\n"
        if "answer" in i:
            relevant_questions += "Answer: " + i["answer"] + "\n"
        relevant_questions += "\n"
    bot.send_message(message.chat.id, "Here is the relevant questions:")
    bot.send_message(message.chat.id, relevant_questions)
    state[message.chat.id]["relevant_questions"] = relevant_questions
    state[message.chat.id]["relevant_questions_json"] = relevant_questions_json
    if state[message.chat.id]["command"] == "ask_question":
        answer_question(message)
    else:
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
        system_message=GPT_RELEVANT_QUESTION_SYSTEM_MESSAGE,
    )
    relevant_question_id = json.loads(gpt_answer)["Auto_id"]
    document = api.specific_document_from_knowledgebase(relevant_question_id)
    document_for_print = document.copy()
    document_for_print["answer"] = document_for_print["answer"][:1000]
    bot.send_message(
        message.chat.id,
        f"Here is the most relevant question from the database (id={relevant_question_id})",
    )
    bot.send_message(
        message.chat.id,
        json.dumps(
            document_for_print,
            indent=4,
            ensure_ascii=False,
        )[:4096],
    )
    bot.send_chat_action(message.chat.id, "typing")
    user_message2 = {
        "question": question,
        "relevant_question": document,
    }
    gpt_answer = api.query_gpt(
        user_message=json.dumps(user_message2),
        system_message=GPT_GENERATE_ANSWER_SYSTEM_MESSAGE,
    )
    bot.send_message(message.chat.id, gpt_answer)
    state[message.chat.id]["command"] = None


bot.infinity_polling()
