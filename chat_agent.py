import streamlit as st
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from persona_config import build_system_prompt, ensure_system_message
import os
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
load_dotenv()
MODEL = init_chat_model(
    model="deepseek-v4-flash",
    model_provider="openai",
    api_key="sk-68b6a5e0a7a7480d9104e1cd54abdd00",
    base_url="https://api.deepseek.com"
                        )
# ========== 基础配置 ==========
MAX_ROUNDS = 20

SYSTEM_PROMPT = build_system_prompt()

# ========== 初始化 ==========
if "messages" not in st.session_state:
    st.session_state.messages = []

st.session_state.messages = ensure_system_message(st.session_state.messages, SYSTEM_PROMPT)

# ========== 截断历史 ==========
def trim_messages(msgs):
    system_msg = msgs[0]
    history = msgs[1:]
    max_messages = MAX_ROUNDS * 2

    if len(history) > max_messages:
        history = history[-max_messages:]

    return [system_msg] + history


# ========== 页面配置 ==========
st.set_page_config(page_title="章子怡聊天", page_icon="💬", layout="centered")

st.title("💬 章子怡")

st.caption("微信风格虚拟聊天")

# ========== 微信气泡样式 ==========
st.markdown("""
<style>
.chat-container {
    display: flex;
    flex-direction: column;
    gap: 10px;
    margin-bottom: 100px;
}

.msg-user {
    align-self: flex-end;
    background-color: #95ec69;
    color: black;
    padding: 10px 14px;
    border-radius: 12px 12px 0 12px;
    max-width: 70%;
    font-size: 15px;
}

.msg-ai {
    align-self: flex-start;
    background-color: white;
    border: 1px solid #eee;
    padding: 10px 14px;
    border-radius: 12px 12px 12px 0;
    max-width: 70%;
    font-size: 15px;
}
</style>
""", unsafe_allow_html=True)


# ========== 显示聊天记录 ==========
st.markdown('<div class="chat-container">', unsafe_allow_html=True)

for msg in st.session_state.messages[1:]:
    if isinstance(msg, HumanMessage):
        st.markdown(f'<div class="msg-user">你：{msg.content}</div>', unsafe_allow_html=True)
    elif isinstance(msg, AIMessage):
        st.markdown(f'<div class="msg-ai">章子怡：{msg.content}</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# ========== 输入框 ==========
user_input = st.chat_input("输入消息...")

if user_input:
    # 用户消息
    st.session_state.messages.append(HumanMessage(content=user_input))

    # AI回复
    response = MODEL.invoke(st.session_state.messages)
    ai_text = response.content

    st.session_state.messages.append(AIMessage(content=ai_text))

    # 截断历史
    st.session_state.messages = trim_messages(st.session_state.messages)

    # 刷新页面
    st.rerun()
