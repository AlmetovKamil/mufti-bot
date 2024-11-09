import requests
import json

from settings import BACKEND_BASE_URL, BACKEND_API_KEY
import api_endpoints


def relevant_documents(
    query: str, limit=10, with_answer=False, source_id="islamqa"
):
    url = BACKEND_BASE_URL + api_endpoints.RELEVANT_DOCUMENTS
    params = {
        "source_id": source_id,
        "query": query,
        "limit": limit,
        "with_answer": with_answer,
    }
    headers = {"x-api-key": BACKEND_API_KEY}
    response = requests.get(url, params=params, headers=headers)
    return response.json()


def query_gpt_raw(
    user_message: str,
    system_message: str,
    llm_model="gpt-4o-mini",
    json_only=False,
    temperature=1,
):
    url = BACKEND_BASE_URL + api_endpoints.QUERY_GPT
    data = {
        "user_message": user_message,
        "system_message": system_message,
        "llm_model": llm_model,
        "json_only": json_only,
        "temperature": temperature,
    }
    headers = {"x-api-key": BACKEND_API_KEY}
    response = requests.post(url, json=data, headers=headers)
    response_json = response.json()
    print(response_json)
    return response_json


def query_gpt(
    user_message: str,
    system_message: str,
    llm_model="gpt-4o-mini",
    json_only=False,
    temperature=1,
) -> int:
    answer_json = query_gpt_raw(
        user_message, system_message, llm_model, json_only, temperature
    )
    # TODO - can be there multiple choices?
    # if len(answer_json['choices']) == 1:
    return json.loads(answer_json['choices'][0]['message']['content'])['Auto_id']
    # answer = []
    # for choice in answer_json['choices']:
    #     answer.append(choice['message']['content'])

