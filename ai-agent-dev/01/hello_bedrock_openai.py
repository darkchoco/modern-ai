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

# api_key = os.environ.get("OPENAI_API_KEY")
# client = OpenAI(api_key=api_key)

# AWS 설정에 맞춰 환경 변수를 업데이트해야 합니다.
# 2026년 기준, Bedrock은 특정 리전에서 OpenAI 호환 엔드포인트를 제공합니다.
api_key = os.environ.get("BEDROCK_API_KEY")
base_url = "https://bedrock-runtime.eu-west-1.amazonaws.com/openai/v1"

# OpenAI 클라이언트를 Bedrock 엔드포인트로 초기화
client = OpenAI(
    api_key=api_key,
    base_url=base_url
)


def get_chat_completion(prompt, model="openai.gpt-oss-20b-1:0"):
    res = client.chat.completions.create(
        model=model,
        messages=[
            ChatCompletionSystemMessageParam(
                role="system",
                content="당신은 친절하고 도움이 되는 AI 비서입니다. 답변 시 <reasoning> 태그나 추론 과정은 생략하고, 최종 답변만 제공하세요."
            ),
            ChatCompletionUserMessageParam(
                role="user",
                content=prompt),
        ],
    )
    return res.choices[0].message.content


def get_responses(prompt, model="openai.gpt-oss-20b-1:0"):
    """
        Bedrock의 Responses API는 OpenAI의 신규 Responses API와 호환됩니다.
        서버 측에서 상태(Context)를 관리하는 기능을 지원합니다.
    """
    res = client.responses.create(
        model=model,
        input=prompt,
        # Bedrock에서 지원하는 서버 측 도구(Web Search 등) 설정 가능
        tools=[{"type": "web_search_preview"}]  # type: ignore
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
    # 주석 처리.
    # 1. Amazon Bedrock의 OpenAI 호환 엔드포인트는 현재 Chat Completions(/chat/completions)를 주력으로 지원하며,
    #    모든 모델이 responses 엔드포인트를 지원하는 것은 아님.
    # 2. tools=[{"type": "web_search_preview"}] 기능 미지원. Bedrock Knowledge Bases를 사용하던가 Search를 직접
    #    구현해야 한다.
    # response = get_responses(another_prompt)

    print("\nAI 응답:")
    print(response)
