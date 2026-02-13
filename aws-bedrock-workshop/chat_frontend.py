"""
Amazon Bedrock을 통한 Google Gemma 3 모델과의 채팅 기능을 제공한다.

주의 사항:
PyCharm에서 Streamlit 애플리케이션을 디버깅하려면, Streamlit이 일반적인 Python 스크립트 실행 방식(python main.py)이 아닌
전용 CLI(streamlit run main.py)로 구동된다는 점을 고려해야 한다.
가장 효율적인 방법은 Python Debug Configuration을 직접 설정하는 것이다.

PyCharm 상단 메뉴에서 Run > Edit Configurations... 클릭.
좌측 상단의 + (Add New Configuration) 버튼을 누르고 Python을 선택.설정을 다음과 같이 입력.
- Name: Streamlit Debug (임의 지정)
- Run kind: Module name 선택
- Module name: streamlit
- Parameters: run chat_frontend.py

그 다음 Debug 버튼 클릭.
"""

import streamlit as st
import chat_backend as glib  # reference to local lib script


# Here we are setting the page title on the actual page and the title shown in the browser tab.
st.set_page_config(page_title="Chatbot")  # HTML title
st.title("Chatbot")  # page title

if 'memory' not in st.session_state:
    st.session_state.memory = glib.create_memory()  # initialize the memory

if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []  # initialize the chat history

# Re-render the chat history (Streamlit re-runs this script, so need this to preserve previous chat messages)
for message in st.session_state.chat_history:  # loop through the chat history
    with st.chat_message(message["role"]):  # renders a chat line for the given role, containing everything in the with block
        st.markdown(message["text"])  # display the chat content

input_text = st.chat_input("Chat with your bot here")  # display a chat input box

if input_text:  # run the code in this if block after the user submits a chat message
    with st.chat_message("user"):  # display a user chat message
        st.markdown(input_text)  # renders the user's latest message

    st.session_state.chat_history.append({"role": "user",
                                          "text": input_text})  # append the user's latest message to the chat history

    chat_response = glib.get_chat_response(input_text=input_text,
                                           memory=st.session_state.memory)  # call the model through the supporting library

    with st.chat_message("assistant"):  # display a bot chat message
        st.markdown(chat_response)  # display bot's latest response

    st.session_state.chat_history.append({"role": "assistant",
                                          "text": chat_response})  # append the bot's latest message to the chat history
