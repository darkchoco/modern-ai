# -*- coding: utf-8 -*-

"""
아래 언급한 이유 중 하나로 동작하지 않는다.
1. 모델 이름 오류: "openai.gpt-oss-20b-1:0" 모델이 Bedrock Runtime에서 지원되지 않음
2. API 불일치: client.responses.stream()은 OpenAI의 새로운 API로, Bedrock Runtime이 지원하지 않음
"""
import os
from dotenv import load_dotenv
from openai import OpenAI
import rich


# client = OpenAI()
# default_model = "gpt-5-mini"

load_dotenv()

api_key = os.environ.get("BEDROCK_API_KEY")
base_url = "https://bedrock-runtime.eu-west-1.amazonaws.com/openai/v1"

client = OpenAI(
    api_key=api_key,
    base_url=base_url
)
default_model = "openai.gpt-oss-20b-1:0"


def stream_chat_completion(prompt, model):
    # ① chat.completions API를 사용한 스트리밍 응답 함수
    stream = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        stream=True,  # ② 스트리밍 모드 활성화
    )
    for chunk in stream:  # ③ 응답 청크(조각)를 하나씩 처리
        content = chunk.choices[0].delta.content
        if content is not None:
            print(content, end="")


def stream_response(prompt, model):
    # ④ 새로운 responses API를 사용한 스트리밍 함수( 컨텍스트 매니저로 스트림 관리)
    with client.responses.stream(model=model, input=prompt) as stream:
        for event in stream:  # ⑤ 스트림에서 발생하는 각 이벤트 처리
            if "output_text" in event.type:  # ⑥ 텍스트 출력 이벤트인 경우
                rich.print(event)
    rich.print(stream.get_final_response())  # 최종 응답 출력


if __name__ == "__main__":
    stream_chat_completion("스트리밍이 뭔지 아주 간단하게 설명 부탁해요.", default_model)
    stream_response("점심 메뉴 추천 해주세요.", default_model)
