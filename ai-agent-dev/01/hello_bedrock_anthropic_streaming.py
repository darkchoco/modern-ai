from anthropic import AnthropicBedrock
import rich

client = AnthropicBedrock()

model_id = "eu.anthropic.claude-haiku-4-5-20251001-v1:0"

prompt = "anthropic 발음은 앤트로픽이 맞나요? 앤스로픽이 맞나요?"
# ① 컨텍스트 매니저를 사용한 스트리밍 세션 생성
with client.messages.stream(
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}],
        model=model_id
) as stream:
    for event in stream:
        if event.type == "text":  # ② 텍스트 타입 이벤트만 처리
            print(event.text, end="")
    print()
    # ③ 최종 응답 출력
    rich.print(stream.get_final_message())
