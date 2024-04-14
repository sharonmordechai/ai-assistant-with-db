# AI Assistant

**The Streamlit app for the AI Assistant can be found [here](https://ai-assistant-with-db.streamlit.app/). You're welcome to give it a try!**

This is a [Streamlit](https://streamlit.io)-based AI assistant powered by [OpenAI](https://openai.com). The assistant is designed to answer questions based on its training knowledge and also supports uploading a CSV file to address further questions using [Langchain](https://www.langchain.com) for enhanced data processing.

## Features

- **OpenAI Integration**: Use GPT-4 or GPT-3.5-turbo models from OpenAI for conversational responses.
- **SQL Capabilities**: Support for SQL queries using an uploaded CSV file.
- **Interactive Chat Interface**: Real-time interactive chat experience.
- **Clear Chat History**: Option to clear chat history.

---

## How to Run the Application

To run the application, follow the steps below:

1. Install Required Packages:

    ```bash
    # Install packages
    python -m pip install -r requirements.txt
    ```
   
    This command will install all the necessary dependencies listed in the requirements.txt file.


2. Run the Application:

    ```bash
    # Run application
    streamlit run main.py
    ```
   
    This command will start the application and execute the main.py script, allowing you to interact with the application.

---

## How to Use

### OpenAI API Key

1. Enter your [OpenAI API key](https://platform.openai.com/account/api-keys) in the sidebar.
   
### Choose OpenAI Model

- **Model**: Choose between `gpt-4` or `gpt-3.5-turbo`.
- **Temperature**: Adjust the temperature slider (disabled for now).

### Upload a File

1. Click on the "Upload a file" section.
2. Upload a CSV file to enable SQL capabilities.

### Clear Chat History

- Click on the "Clear History" button to clear the chat history.

---

## About

This AI assistant is built using Streamlit and integrates the powerful capabilities of OpenAI's GPT-4 and GPT-3.5-turbo models. It is further enhanced with Langchain for efficient data processing and querying. The assistant is designed to answer questions based on its training knowledge and allows for uploading a CSV file to address questions through SQL queries.

Please note that this is a beta tool, and any feedback is appreciated to enhance its performance.

## Credits

[Sharon Mordechai](https://www.linkedin.com/in/sharon-mordechai-a294b6129/)
