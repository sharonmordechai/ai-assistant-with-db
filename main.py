import os
import time
import tempfile

import pandas as pd
import streamlit as st
from langchain_community.agent_toolkits.sql.base import create_sql_agent

from sqlalchemy import create_engine

from langchain_openai import ChatOpenAI
from langchain.agents import initialize_agent
from langchain.memory import ConversationBufferWindowMemory
from langchain_community.chat_message_histories.streamlit import StreamlitChatMessageHistory
from langchain_community.utilities.sql_database import SQLDatabase
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit

# Set page title
st.set_page_config(page_title="AI Assistant")

# Streamlit UI setup
st.title("AI Assistant")
st.caption("A powerful AI assistant powered by OpenAI")

# Initial sidebar menu
with st.sidebar:
    st.markdown("# How to use\n Enter your [OpenAI API key](https://platform.openai.com/account/api-keys) below:")
    openai_api_key = st.text_input("OpenAI API Key", type="password")

    st.markdown("Choose OpenAI model:")
    model_name = st.selectbox("Model", options=["gpt-4", "gpt-3.5-turbo"])
    temperature = st.slider('Temperature', min_value=0.0, max_value=1.0, step=0.1, value=0.2, disabled=True)

    st.markdown("\n")
    st.markdown("Clear chat history:")
    clear_history = st.button("Clear History")

    st.markdown("---")
    st.markdown("# Upload a file")
    uploaded_file = st.file_uploader(label="Support SQL capabilities based on an uploaded file.", type=["csv"])

    st.markdown("---")
    st.markdown("# About")
    st.markdown("""
        This AI assistant is based on OpenAI and is designed to answer questions based on its training knowledge.

        Additionally, it allows for uploading a CSV file to address questions. 

        Please note that this is a beta tool, and any feedback is appreciated to enhance its performance.""")
    st.markdown("Made by [Sharon M.](https://www.linkedin.com/in/sharon-mordechai-a294b6129/)")

# Validate OpenAI API key
if not openai_api_key:
    st.error("Please input your OpenAI API key in the sidebar.")
    st.stop()

# Initialize OpenAI agent
llm = ChatOpenAI(model_name=model_name, openai_api_key=openai_api_key, temperature=temperature)

# Initialize chat history and memory
msgs = StreamlitChatMessageHistory()
memory = ConversationBufferWindowMemory(chat_memory=msgs, return_messages=True, memory_key="chat_history", output_key="output")

# Initial session state messages
if "messages" not in st.session_state:
    st.session_state.messages = []
if "file" not in st.session_state:
    st.session_state.file = None
if "on_change" not in st.session_state:
    st.session_state.on_change = False
if "engine" not in st.session_state:
    st.session_state.engine = create_engine("sqlite:///dev.db")
if "agent" not in st.session_state:
    st.session_state.agent = initialize_agent(
        llm=llm,
        tools=[],
        agent="conversational-react-description",
        memory=memory,
        handle_parsing_errors=lambda error: str(error)[:50])

# Handle chat history clearing
if clear_history:
    # clear session messages
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Handle uploaded CSV file
if uploaded_file != st.session_state.file:
    with st.spinner("Uploading files..."):
        if uploaded_file is None:
            # Remove embedded database
            os.remove("dev.db")
            del st.session_state.engine

            # In case of file removal, initialize agent with empty tools
            st.session_state.agent = initialize_agent(
                llm=llm,
                tools=[],
                agent="conversational-react-description",
                memory=memory,
                handle_parsing_errors=lambda error: str(error)[:50])

            st.session_state.file = None
        else:
            # Create temporary directory
            temp_dir = tempfile.TemporaryDirectory()

            # Create temporary file path
            temp_filepath = os.path.join(temp_dir.name, uploaded_file.name)

            # Save temporary file
            with open(temp_filepath, "wb") as f:
                f.write(uploaded_file.getvalue())

            # Initialize SQL tool
            df = pd.read_csv(temp_filepath)
            df.to_sql(os.path.splitext(os.path.basename(temp_filepath))[0], st.session_state.engine, index=False, if_exists="replace")
            db = SQLDatabase(engine=st.session_state.engine)
            toolkit = SQLDatabaseToolkit(db=db, llm=llm)

            # Initialize agent
            # st.session_state.agent = create_sql_agent(llm=llm, toolkit=toolkit, agent_type="openai-tools")

            st.session_state.agent = initialize_agent(
                llm=llm,
                tools=toolkit.get_tools(),
                agent="conversational-react-description",
                memory=memory,
                handle_parsing_errors=lambda error: str(error)[:50])

            st.session_state.file = uploaded_file
        st.toast("File was updated successfully.")


# Function to stream the response for a more interactive chat experience
def stream_response(res):
    for word in res.split(" "):
        yield word + " "
        time.sleep(0.02)


# Handle user input and generate response
if prompt := st.chat_input("Type your message here..."):
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        stream_res = stream_response(st.session_state.agent.invoke(prompt)["output"])
        response = st.write_stream(stream_res)

    st.session_state.messages.append({"role": "assistant", "content": response})