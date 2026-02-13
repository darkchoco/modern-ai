import boto3
from langchain_aws import ChatBedrock
from langchain_core.messages import HumanMessage, AIMessage


class SimpleConversationMemory:
    """Simple memory implementation for LangChain 1.0+"""
    def __init__(self, max_history=10):
        self.conversation_history = []
        self.max_history = max_history

    def save_context(self, input_text, output_text):
        self.conversation_history.append({"human": input_text, "ai": output_text})

        if len(self.conversation_history) > self.max_history:
            self.conversation_history.pop(0)

    def get_messages(self):
        """LangChain 메시지 객체 리스트 반환"""
        messages = []
        for entry in self.conversation_history:
            messages.append(HumanMessage(content=entry["human"]))
            messages.append(AIMessage(content=entry["ai"]))
        return messages

    # def load_memory_variables(self, inputs):
    #     """Load memory variables"""
    #     history = "\n".join(self.conversation_history)
    #     return {"history": history}

    def clear(self):
        self.conversation_history = []


def get_llm():
    # AUTHENTICATION METHODS:

    # Method 1: Default AWS credential chain (current approach)
    # Uses environment variables, AWS CLI config, or IAM roles

    # Option A: Use default credentials (current)
    bedrock_client = boto3.client(
        service_name="bedrock-runtime",
        region_name="eu-west-1"
    )

    llm = ChatBedrock(
        model="google.gemma-3-27b-it",
        client=bedrock_client,  # 실제 모델이 활성화된 리전 확인 필요
        model_kwargs={
            "max_tokens": 1024,
            "temperature": 0.7,  # 얼마나 창의적인지
            "top_p": 0.9,
        },
        beta_use_converse_api=True  # 최신 모델은 AWS의 Converse API를 통해 통신한다. LangChain의 ChatBedrock
                                    # 인스턴스 생성 시 이 옵션을 추가하면 해결되는 경우가 많다.
    )

    # Option B: Use specific AWS profile (uncomment and replace 'your-profile-name')
    # import boto3
    # import os
    #
    # # Set profile name - replace with your actual profile name
    # profile_name = os.getenv('AWS_PROFILE', 'your-profile-name')
    # session = boto3.Session(profile_name=profile_name)
    #
    # llm = ChatBedrock(
    #     model_id="amazon.titan-text-express-v1",
    #     model_kwargs={
    #         "temperature": 1,
    #         "topP": 0.5,
    #         "maxTokenCount": 100,
    #     },
    #     client=session.client('bedrock-runtime', region_name='us-east-1')
    # )

    # Method 2: Explicit credentials (uncomment to use)
    # import boto3
    # session = boto3.Session(
    #     aws_access_key_id='YOUR_ACCESS_KEY',
    #     aws_secret_access_key='YOUR_SECRET_KEY',
    #     region_name='us-east-1'
    # )
    # llm = ChatBedrock(
    #     model_id="amazon.titan-text-express-v1",
    #     model_kwargs={
    #         "temperature": 1,
    #         "topP": 0.5,
    #         "maxTokenCount": 100,
    #     },
    #     client=session.client('bedrock-runtime')
    # )

    # Method 3: Using AWS profile (uncomment to use)
    # import boto3
    # session = boto3.Session(profile_name='your-profile-name')
    # llm = ChatBedrock(
    #     model_id="amazon.titan-text-express-v1",
    #     model_kwargs={
    #         "temperature": 1,
    #         "topP": 0.5,
    #         "maxTokenCount": 100,
    #     },
    #     client=session.client('bedrock-runtime')
    # )

    return llm


def create_memory():
    return SimpleConversationMemory()  # Maintains conversation history


def get_chat_response(input_text, memory):
    llm = get_llm()

    # 메모리에서 이전 대화 내역 가져오기
    messages = memory.get_messages()
    # 현재 사용자 입력 추가
    messages.append(HumanMessage(content=input_text))

    try:
        response = llm.invoke(messages)
        response_text = response.content

        memory.save_context(input_text, response_text)

        return response_text

    except Exception as e:
        error_msg = str(e)

        # Check for specific AWS authentication errors
        if "ExpiredTokenException" in error_msg or "ExpiredToken" in error_msg:
            return "⚠️ AWS credentials have expired. Please run 'aws configure' or 'aws sso login' to refresh your credentials, then try again."
        elif "UnauthorizedOperation" in error_msg or "AccessDenied" in error_msg:
            return "⚠️ AWS access denied. Please check your AWS permissions for Bedrock access."
        else:
            return "I'm sorry, I'm having trouble connecting to AWS Bedrock. Please check your AWS credentials and try again."


if __name__ == "__main__":
    # 세션별 메모리 생성
    chat_memory = create_memory()

    while True:
        user_input = input("User: ")
        if user_input.lower() in ["exit", "quit", "종료"]:
            break

        answer = get_chat_response(user_input, chat_memory)
        print(f"Assistant: {answer}\n")
