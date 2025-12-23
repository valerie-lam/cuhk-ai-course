import streamlit as st

#Initialize chat history in session state if it doesn't exist
if "messages" not in st.session_state:
    st.session_state.messages = []

#Display chat messages
for message in st.session_state.messages:
    with st.chat_message (message["role"]):
        st.write (message["content"])

#Chat input
if prompt := st.chat_input("Copy the message you received and paste it here:"):
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