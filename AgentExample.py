import streamlit as st
from langchain.tools import Tool
from langchain.agents import initialize_agent
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate


st.title("LLM String Operations Agent")
openai_api_key = st.sidebar.text_input('OpenAI API Key', type='password')

def reverse_string(text: str) -> str:
    return text[::-1]

def to_uppercase(text: str) -> str:
    return text.upper()

def get_length(text: str) -> str:
    return str(len(text))

tools = [
    Tool(name="reverse", func=reverse_string, description="Reverses the input string."),
    Tool(name="uppercase", func=to_uppercase, description="Converts the input string to uppercase."),
    Tool(name="length", func=get_length, description="Returns the length of the input string.")
]

if not openai_api_key.startswith('sk-'):
    st.warning('Please enter your OpenAI API key!', icon='⚠')
if openai_api_key.startswith('sk-'):
    user_input = st.text_input("Enter your command (reverse, uppercase, length) followed by the string:")
    if st.button("Execute"):
        if user_input:
            with st.spinner("Processing..."):
                try:
                    llm = ChatOpenAI(api_key=openai_api_key,temperature=0.4,model='gpt-3.5-turbo-1106')
                    prompt_template = ChatPromptTemplate.from_template("""
                            You are a helpful assistant that can perform various string operations.
                            You have access to the following tools:
                            - reverse: Reverses the input string.
                            - uppercase: Converts the input string to uppercase.
                            - length: Returns the length of the input string.
                            The user will provide you with a command, and you will use the appropriate tool to perform the operation.
                            Command: {user_input}
                            """)
                    st.write(prompt_template)
                    agent = initialize_agent(
                            llm=llm,
                            tools=tools,
                            prompt=prompt_template)
                    # Run the agent with the user input
                    response = agent({"input": user_input})
                    st.write("### Result")
                    st.write(response)
                except KeyError as e:
                    st.error(f"An error occurred: {e}")
                except Exception as e:
                    st.error(f"An error occurred: {e}")
        else:
            st.error("Please enter a command and a string.")

