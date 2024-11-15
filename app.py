import streamlit as st
from langchain_community.llms import Ollama
from langchain_core.messages import HumanMessage , AIMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder




#############  llm 

if "chat" not in st.session_state:
    st.session_state["chat"] = []

llm = Ollama(model="llama3.2")
    
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", 
            "You are an chat bot for my app Dev Navigator which is a platform where student get the specilized roadmap for there particular project or job, initially ask about what they want if they not specifiy then \
                ask them some question like time period in which this task want to complete and and what technologies want to use in this task and what past experence have in this technologies, then generates roadmap based on this for the given time period. ask question one by one, then generate roadmap."),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{input}"),
    ]
    )

chain = prompt | llm

def get_ollama_response(user_input):
    response = chain.invoke({"input":user_input, "chat_history": st.session_state["chat"]})
    st.session_state["chat"].append(HumanMessage(content=user_input))
    st.session_state["chat"].append(AIMessage(content=response))
    
    
    return response

###################



st.title("AI Chat")
st.write("Chat with our AI assistant!")


if "chat_history" not in st.session_state:
    st.session_state.chat_history = []


chat_container = st.container()
with chat_container:
    for chat in st.session_state.chat_history:
        if chat["role"] == "user":
            st.markdown(f"**You:** {chat['message']}")
        else:
            st.markdown(f"**Bot:** {chat['message']}")


st.divider() 
with st.container():
    with st.form(key="user_input_form", clear_on_submit=True):
        user_input = st.text_input("Type your message:", placeholder="Type here...", key="user_input")
        submit_button = st.form_submit_button("Send")

if submit_button and user_input:

    st.session_state.chat_history.append({"role": "user", "message": user_input})
    bot_response = get_ollama_response(user_input)
    st.session_state.chat_history.append({"role": "bot", "message": bot_response})
    st.rerun()