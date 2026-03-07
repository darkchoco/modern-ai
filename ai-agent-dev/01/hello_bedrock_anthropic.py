from anthropic import AnthropicBedrock


# client = anthropic.Anthropic()
client = AnthropicBedrock()

# ① 대화 기록을 저장할 리스트
conversation = [{"role": "user", "content": "안녕, 나는 익훈이야."}]

model_id = "eu.anthropic.claude-haiku-4-5-20251001-v1:0"

# ② Claude 호출
response = client.messages.create(
    model=model_id,
    max_tokens=1000,
    messages=conversation
)

# ③ 응답 출력 및 대화 기록에 추가
assistant_message = response.content[0].text
print(assistant_message)
conversation.append({"role": "assistant", "content": assistant_message})

# ④ 다음 사용자 입력
conversation.append({"role": "user", "content": "내 이름이 뭐라고?."})

# 다시 Claude 호출
response = client.messages.create(
    model=model_id,
    max_tokens=1000,
    messages=conversation
)

# ⑤ 두번째 응답 출력
print(response.content[0].text)
