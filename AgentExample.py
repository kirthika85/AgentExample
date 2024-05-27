import streamlit as st
from langchain import OpenAI, AgentExecutor, Tool
from langchain.prompts import ChatPromptTemplate

# Define string operations as tools
def reverse_string(s):
    return s[::-1]

def to_uppercase(s):
    return s.upper()

def get_length(s):
    return len(s)

# Create Tool instances for each operation
reverse_tool = Tool(name="reverse", func=reverse_string, description="Reverses a string")
uppercase_tool = Tool(name="uppercase", func=to_uppercase, description="Converts a string to uppercase")
length_tool = Tool(name="length", func=get_length, description="Returns the length of a string")

# Initialize OpenAI LLM
openai_api_key = st.sidebar.text_input('OpenAI API Key', type='password')
openai_llm = None
if openai_api_key:
    openai_llm = OpenAI(api_key=openai_api_key, model='gpt-3.5-turbo')

tools = [reverse_tool, uppercase_tool, length_tool]

# Define a simple function to handle input and call the appropriate tool
def agent_respond(input_text, tools):
    command, _, args = input_text.partition(' ')
    for tool in tools:
        if command == tool.name:
            return tool.func(args)
    return f"Unknown command: {command}"

st.title("String Operations with LLM Agent")
user_input = st.text_input("Enter your command:")

if st.button("Submit"):
    if openai_api_key and user_input:
        try:
            response = agent_respond(user_input, tools)
            st.write(f"Result: {response}")
        except Exception as e:
            st.error(f"An error occurred: {e}")
    elif not openai_api_key:
        st.warning("Please enter your OpenAI API key.")
    else:
        st.warning("Please enter a command.")
