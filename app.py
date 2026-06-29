import streamlit as st
from chat_agent import ChatAgent

st.set_page_config(page_title="Chat Agent", page_icon="💬")

st.title("💬 Chat Agent")

# 初始化模型
if "agent" not in st.session_state:
    st.session_state.agent = ChatAgent()

# 初始化聊天记录
if "messages" not in st.session_state:
    st.session_state.messages = []

# 展示历史消息
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 用户输入
user_input = st.chat_input("请输入消息...")

if user_input:
    # 存用户消息
    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.chat_message("user"):
        st.markdown(user_input)

    # 生成回复
    response = st.session_state.agent.chat(user_input)

    # 存AI消息
    st.session_state.messages.append({"role": "assistant", "content": response})

    with st.chat_message("assistant"):
        st.markdown(response)
