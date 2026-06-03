import os
import html
import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv


api_key = st.secrets["GOOGLE_API_KEY"]
genai.configure(api_key=api_key)

st.set_page_config(
    page_title="AI Chatbot",
    page_icon="🤖",
    layout="wide"
)

st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #f8fafc, #dbeafe, #e0e7ff);
    color: #111827;
}

.main-title {
    text-align: center;
    font-size: 42px;
    font-weight: 800;
    color: #111827;
    margin-top: 20px;
}

.sub-title {
    text-align: center;
    font-size: 18px;
    color: #374151;
    margin-bottom: 30px;
}

.chat-container {
    max-width: 900px;
    margin: auto;
}

.user-message {
    background-color: #dbeafe;
    color: #111827;
    padding: 16px;
    border-radius: 16px;
    margin: 12px 0 12px auto;
    max-width: 75%;
    font-size: 16px;
    line-height: 1.6;
    border: 1px solid #60a5fa;
}

.bot-message {
    background-color: #ffffff;
    color: #111827;
    padding: 16px;
    border-radius: 16px;
    margin: 12px auto 12px 0;
    max-width: 75%;
    font-size: 16px;
    line-height: 1.6;
    border: 1px solid #d1d5db;
    box-shadow: 0px 4px 12px rgba(0,0,0,0.08);
}

.sender {
    font-weight: 700;
    margin-bottom: 6px;
}

.stTextInput input {
    background-color: #ffffff;
    color: #111827;
    border-radius: 12px;
    border: 1px solid #9ca3af;
    padding: 12px;
}

.stButton button {
    background-color: #2563eb;
    color: white;
    border-radius: 10px;
    border: none;
    padding: 10px 22px;
    font-weight: 700;
}

.stButton button:hover {
    background-color: #1d4ed8;
    color: white;
}

section[data-testid="stSidebar"] {
    background-color: #111827;
}

section[data-testid="stSidebar"] * {
    color: white;
}
</style>
""", unsafe_allow_html=True)

if not api_key:
    st.error("Google API key not found. Add your API key in the .env file.")
    st.stop()

genai.configure(api_key=api_key)

model = genai.GenerativeModel("gemini-2.5-flash")

if "messages" not in st.session_state:
    st.session_state.messages = []

if "history" not in st.session_state:
    st.session_state.history = []

with st.sidebar:
    st.title("💬 Chat History")

    if st.button("🧹 Clear Chat"):
        st.session_state.messages = []
        st.session_state.history = []
        st.rerun()

    st.markdown("---")

    if st.session_state.history:
        for i, chat in enumerate(st.session_state.history, start=1):
            st.write(f"{i}. {chat}")
    else:
        st.write("No chat history yet.")

st.markdown('<div class="main-title">🤖 AI Chatbot</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">ChatGPT-like AI chatbot using Gemini API</div>', unsafe_allow_html=True)

st.markdown('<div class="chat-container">', unsafe_allow_html=True)

for msg in st.session_state.messages:
    safe_content = html.escape(msg["content"])

    if msg["role"] == "user":
        st.markdown(
            f"""
            <div class="user-message">
                <div class="sender">You</div>
                {safe_content}
            </div>
            """,
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            f"""
            <div class="bot-message">
                <div class="sender">AI Assistant</div>
                {safe_content}
            </div>
            """,
            unsafe_allow_html=True
        )

st.markdown("</div>", unsafe_allow_html=True)

with st.form("chat_form", clear_on_submit=True):
    user_input = st.text_input("Ask anything:", placeholder="Type your message and press Enter...")
    submitted = st.form_submit_button("Send")

if submitted and user_input.strip():
    user_message = user_input.strip()

    st.session_state.messages.append({
        "role": "user",
        "content": user_message
    })

    st.session_state.history.append(user_message)

    try:
        with st.spinner("AI is typing..."):
            response = model.generate_content(user_message)
            bot_reply = response.text

    except Exception as e:
        bot_reply = f"Error: {e}"

    st.session_state.messages.append({
        "role": "assistant",
        "content": bot_reply
    })

    st.rerun()
