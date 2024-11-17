import streamlit as st
import requests
from time import sleep


#############  llm 

if "chat" not in st.session_state:
    st.session_state["chat"] = []

API_URL = "https://brookcisyp.pythonanywhere.com/api/chat"  # Flask API endpoint

def get_ollama_response(user_input):
    try:
        response = requests.post(API_URL, json={"input": user_input})
        if response.status_code == 200:
            return response.json()["response"]
        else:
            st.error(f"Error: {response.status_code}, {response.text}")
            sleep(10)
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        return f"DevNavigator APi is not connecting... : {str(e)}"
###################

st.title("AI Chat")
st.write("Chat with our AI assistant!")
st.divider() 

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []


chat_container = st.container(height=500, border=True)

for chat in st.session_state.chat_history:
    avatar = "🤖" if chat["role"] == "user" else "😎"
    if chat["role"] == "user":
        with chat_container.chat_message(chat["role"], avatar=avatar):
            st.markdown(f"**You:** {chat['message']}")
    else:
        with chat_container.chat_message(chat["role"], avatar=avatar):
            st.markdown(f"**Bot:** {chat['message']}")


with st.container():
    with st.form(key="user_input_form", clear_on_submit=True):
        user_input = st.text_input("Type your message:", placeholder="Type here...", key="user_input")
        submit_button = st.form_submit_button("Send")

if submit_button and user_input:
    st.session_state.chat_history.append({"role": "user", "message": user_input})
    chat_container.chat_message("user", avatar="😎").markdown(user_input)
    with st.spinner("model working..."):
        bot_response = get_ollama_response(user_input)
    st.session_state.chat_history.append({"role": "bot", "message": bot_response})
    chat_container.chat_message("BOT", avatar="🤖").markdown(bot_response)
    
    st.rerun()
    
