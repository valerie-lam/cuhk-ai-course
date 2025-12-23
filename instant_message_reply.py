import os
import streamlit as st
import openai
from dotenv import load_dotenv

# Page configuration
st.set_page_config(
    page_title="Message Reply Generator❄️",
    page_icon="💬",
    layout="wide"
)

st.title("Message Reply Generator❄️")
st.caption("Help you generate messages for different situations")

with st.form("message_form"):
    question1 = st.selectbox(
        "Who is your intended audience?",
        ["", "parent", "sibling", "friend", "client", "teacher", "classmate", "stranger", "relative", "colleague"],
        help="Who will receive your message?"
    )

    question2 = st.selectbox(
        "What style would you like your reply be in?",
        ["", "formal", "casual", "informative", "argumentative", "clear and concise", "encouraging", "professional", "funny", "sarcastic", "optimistic", "pessimistic", "playful", "cynical", "envious", "critical", "respectful"],
        help="What tone or style do you prefer?"
    )

    question3 = st.text_input(
        "Issue to address",
        placeholder="e.g. project deadline, meeting schedule, meal choices...",
        help="What issues or topics would you like your reply to include?)"
    )

    question4 = st.selectbox(
        "How long would you like your reply to be in?",
        ["", "phrase-long", "1 sentence only", "1-2 sentences", "short paragraph", "medium-length paragraphs", "Long paragraphs aiming for persuasion or explantion, etc."],
        help="What length do you prefer?"
    )

    st.form_submit_button("Create my response", use_container_width=True, type="primary")

st.write("Copy the message you received and paste it here:")

#Chat input
if prompt := st.chat_input("Your message:"):
    #Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

#Display user message
with st.chat_message("user"):
    st.write (prompt)

#Add assistant response
assistant_response = "This is where your AI response would appear"
st.session_state.messages.append({"role": "assistant", "content": assistant_response})

#Display assistant response
with st.chat_message("assistant"):
    st.write(assistant_response)


if "messages" not in st.session_state:
    st.session_state.messages = []  # 每項: {"role": "user"/"assistant", "content": ...}
if "form_values" not in st.session_state:
    st.session_state.form_values = {
        "question1": "",
        "question2": "",
        "question3": "",
        "question4": ""
    }

with st.form("message_form"):
    question1 = st.selectbox(
        "Who is your intended audience?",
        ["", "parent", "sibling", "friend", "client", "teacher", "classmate", "stranger", "relative", "colleague"],
        help="Who will receive your message?"
    )

    question2 = st.selectbox(
        "What style would you like your reply be in?",
        ["", "formal", "casual", "informative", "argumentative", "clear and concise", "encouraging", "professional", "funny", "sarcastic", "optimistic", "pessimistic", "playful", "cynical", "envious", "critical", "respectful"],
        help="What tone or style do you prefer?"
    )

    question3 = st.text_input(
        "Issue to address",
        placeholder="e.g. project deadline, meeting schedule, meal choices...",
        help="What issues or topics would you like your reply to include?"
    )

    question4 = st.selectbox(
        "How long would you like your reply to be?",
        ["", "phrase-long", "1 sentence only", "1-2 sentences", "short paragraph", "medium-length paragraphs", "long paragraph"],
        help="What length do you prefer?"
    )

    generate = st.form_submit_button("Save preferences")

    if generate:
        st.session_state.form_values = {
        "question1": question1,
        "question2": question2,
        "question3": question3,
        "question4": question4
    }
    st.success("偏好已儲存")

st.write("貼上你收到的訊息（或用下方輸入框）並送出以取得 AI 回覆：")

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

if prompt := st.chat_input("Your message:"):
    # 儲存使用者訊息
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

        pref = st.session_state.form_values
    system_prompt = (
        f"你係一個幫助撰寫短訊/回覆嘅助理。"
        f"收件人: {pref.get('question1') or '不指定'}；"
        f"風格: {pref.get('question2') or '中性'}；"
        f"主題/議題: {pref.get('question3') or '一般'}；"
        f"長度: {pref.get('question4') or '中等'}。"
        "請用簡潔、禮貌且實用嘅語氣回覆使用者訊息。"
    )

    ai_text = ""
    if not OPENAI_API_KEY:
        ai_text = "API 金鑰未設定，請在環境變數或 .env 中設定 OPENAI_API_KEY。"
    else:
        try:
            resp = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=300,
                temperature=0.7
            )

            ai_text = resp.choices[0].message["content"].strip()
        except Exception as e:
            ai_text = f"呼叫 AI 時發生錯誤：{e}"

st.session_state.message.append({"role": "assistant", "content": ai_text})
with st.chat("assistant"):
        st.write(ai_text)