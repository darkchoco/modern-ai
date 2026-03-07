# -*- coding: utf-8 -*-

"""
OpenAI API를 사용한 간단한 프로그램

용도:

사용법:

참고:
    매우 느림 :-) 중간에 멈춘 것 아니니 참을성이 필요.

"""
import os
from dotenv import load_dotenv
from openai import OpenAI
from openai.types.chat import ChatCompletionSystemMessageParam, ChatCompletionUserMessageParam

load_dotenv()
api_key = os.environ.get("OPENAI_API_KEY")
# OpenAI 클라이언트 초기화.
# client = OpenAI() --> 이렇게 해도 문제 없음
client = OpenAI(api_key=api_key)


def get_chat_completion(prompt, model="gpt-5-mini"):
    # OpenAI Chat Completion API를 사용하여 AI의 응답을 받는 함수"
    res = client.chat.completions.create(
        model=model,
        messages=[
            ChatCompletionSystemMessageParam(role="system", content="당신은 친절하고 도움이 되는 AI 비서입니다."),
            ChatCompletionUserMessageParam(role="user", content=prompt),
        ],
    )
    return res.choices[0].message.content


def get_responses(prompt, model="gpt-5-mini"):
    res = client.responses.create(
        model=model,
        tools=[{"type": "web_search_preview"}],
        input=prompt,
    )
    return res.output_text


if __name__ == "__main__":
    user_prompt = input("AI에게 물어볼 질문을 입력하세요: ")

    response = get_chat_completion(user_prompt)

    print("\nAI 응답:")
    print(response)

    another_prompt = """
    https://platform.openai.com/docs/api-reference/responses/create 
    내용을 읽어서 이 API에 대해 요약 정리 부탁합니다.
    """

    response = get_responses(another_prompt)

    print("\nAI 응답:")
    print(response)
