import os
import streamlit as st
import openai
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("API_KEY")
client = openai.OpenAI(
    api_key=API_KEY,
    base_url="https://api.poe.com/v1",
)


# Page configuration
st.set_page_config(
    page_title="Message Reply Generator❄️",
    page_icon="💬",
    layout="wide"
)

st.title("Message Reply Generator❄️")
st.caption("Help you generate messages for different situations")

def generate_ai_response(user_prompt):
    """Function to handle AI logic and update session state."""
    pref = st.session_state.form_values
    
    # Construct the system instruction based on form preferences
    system_prompt = (
        f"You are an assistant that helps people write messages. "
        f"You are writing ON BEHALF of the user. "
        f"Recipient: {pref.get('question1') or 'not specified'}; "
        f"Style: {pref.get('question2') or 'neutral'}; "
        f"Topic/Issue: {pref.get('question3') or 'general'}; "
        f"Length: {pref.get('question4') or 'medium'}. "
        "Please generate a response that is concise, polite, and fits the requested tone."
    )

    if not API_KEY:
        return "API key not set. Please set API_KEY in environment variables."
    
    try:
        resp = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            max_tokens=500,
            temperature=0.7
        )
        return resp.choices[0].message.content.strip()
    except Exception as e:
        return f"An error occurred: {e}"

with st.form("message_form"):
    question1 = st.selectbox(
        "Who is your intended audience?👤",
        ["", "parent", "sibling", "friend", "client", "teacher", "classmate", "stranger", "relative", "colleague"],
        help="Who will receive your message?"
    )

    question2 = st.selectbox(
        "What style would you like your reply be in?📑",
        ["", "formal", "casual", "informative", "argumentative", "clear and concise", "encouraging", "professional", "funny", "sarcastic", "optimistic", "pessimistic", "playful", "cynical", "envious", "critical", "respectful"],
        help="What tone or style do you prefer?"
    )

    question3 = st.text_input(
        "Issue to address📜",
        placeholder="e.g. project deadline, meeting schedule, meal choices...",
        help="What issues or topics would you like your reply to include?)"
    )

    question4 = st.selectbox(
        "How long would you like your reply to be in?📄",
        ["", "1 sentence only", " around 1-2 sentences", "short paragraph", "medium-length paragraphs", "long paragraphs aiming for persuasion or explantion, etc.", "a whole essay"],
        help="What length do you prefer?"
    )

    submit_button = st.form_submit_button("Create my response", use_container_width=True, type="primary")

    if submit_button:
        # 1. Save form values to session state
        st.session_state.form_values = {
            "question1": question1,
            "question2": question2,
            "question3": question3,
            "question4": question4
        }
        
        # 2. Create a prompt for the AI based on the "Issue"
        initial_prompt = f"Write a message about: {question3}" if question3 else "Write a general greeting message."
        
        # 3. Add user request to chat history (optional, shows what the AI is responding to)
        st.session_state.messages.append({"role": "user", "content": f"Generate a message for: {question3}"})

        # 4. Generate AI response
        with st.spinner("Drafting your message..."):
            ai_reply = generate_ai_response(initial_prompt)
            st.session_state.messages.append({"role": "assistant", "content": ai_reply})
        
        st.success("Response generated!")

st.write("Copy the message you received and paste it here:")


#for message in st.session_state.messages:
    #with st.chat_message(message["role"]):
        #st.write(message["content"])




if "messages" not in st.session_state:
    st.session_state.messages = []  # 每項: {"role": "user"/"assistant", "content": ...}
if "form_values" not in st.session_state:
    st.session_state.form_values = {
        "question1": "",
        "question2": "",
        "question3": "",
        "question4": ""
    }


   # if generate:
        #st.session_state.form_values = {
        # "question1": question1,
        # "question2": question2,
        # "question3": question3,
        # "question4": question4
    # }
    st.success("Preferences are saved.")


for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

if prompt := st.chat_input("Your message:"):
    "Save user's message"
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    pref = st.session_state.form_values
    system_prompt = (
        f"You are an assistant that helps people to write messages."
        f"Recipient: {pref.get('question1') or 'not specified'}；"
        f"Style: {pref.get('question2') or 'neutral'}；"
        f"Topic/Issue: {pref.get('question3') or 'general'}；"
        f"Length: {pref.get('question4') or 'medium'}。"
        "Please respond to the user's message in a concise, polite, and practical tone."
    )

    ai_text = ""
    if not API_KEY:
        ai_text = "API key not set. Please set API_KEY in environment variables or .env file."
    else:
        try:
            resp = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=300,
                temperature=0.7
            )

            ai_text = resp.choices[0].message.content.strip()
        except Exception as e:
            ai_text = f"Mistake happened when summoning AI：{e}"

    st.session_state.messages.append({"role": "assistant", "content": ai_text})
    with st.chat_message("assistant"):
        st.write(ai_text)