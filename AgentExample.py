import streamlit as st
from langchain.agents import initialize_agent, AgentType
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate, HumanMessagePromptTemplate, PromptTemplate
from langchain.tools import Tool

st.title("LLM String Operations Agent")
openai_api_key = st.sidebar.text_input('OpenAI API Key', type='password')

# Define string operation functions
def reverse_string(text: str) -> str:
    return text[::-1]

def to_uppercase(text: str) -> str:
    return text.upper()

def get_length(text: str) -> str:
    return str(len(text))

# Define tools for string operations
tools = [
    Tool(name="reverse", func=reverse_string, description="Reverses the input string."),
    Tool(name="uppercase", func=to_uppercase, description="Converts the input string to uppercase."),
    Tool(name="length", func=get_length, description="Returns the length of the input string.")
]

# Define the human message prompt template
human_message_template = HumanMessagePromptTemplate(
    prompt=PromptTemplate(
        input_variables=["input"],
        template="""
        You are a helpful assistant that can perform various string operations.
        You have access to the following tools:
        - reverse: Reverses the input string.
        - uppercase: Converts the input string to uppercase.
        - length: Returns the length of the input string.
        
        The user will provide you with a command and a string, and you will use the appropriate tool to perform the operation.
        
        Command: {{input.command}}
        Text: {{input.text}}
        """
    )
)

# Create the chat prompt template
chat_prompt_template = ChatPromptTemplate(
    input_variables=["input"],
    messages=[human_message_template]
)

# Check if API key is valid
if not openai_api_key.startswith('sk-'):
    st.warning('Please enter your OpenAI API key!', icon='⚠')
else:
    user_input = st.text_input("Enter your command (reverse, uppercase, length) followed by the string:")
    if st.button("Execute"):
        if user_input:
            with st.spinner("Processing..."):
                try:
                    # Parse the command and text from the user input
                    parts = user_input.split(maxsplit=1)
                    if len(parts) < 2:
                        st.error("Please enter both a command and a string.")
                        raise ValueError("Incomplete input")

                    command = parts[0]
                    text = parts[1]

                    if command not in ["reverse", "uppercase", "length"]:
                        st.error("Invalid command. Use 'reverse', 'uppercase', or 'length'.")
                        raise ValueError("Invalid command")

                    # Initialize the OpenAI LLM
                    llm = ChatOpenAI(api_key=openai_api_key, temperature=0.4, model='gpt-3.5-turbo')

                    # Initialize the agent with the tools and the prompt template
                    agent = initialize_agent(
                        agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
                        tools=tools,
                        llm=llm,
                        prompt=chat_prompt_template,
                        verbose=True
                    )

                    # Format the input data correctly
                    input_data = {"input": {"command": command, "text": text}}
                    st.write(f"Input Data: {input_data}")

                    # Run the agent with the formatted input data
                    response = agent(input_data)
                    st.write(f"Raw Response: {response}")

                    # Display the output from the response
                    output_text = response['output'] if 'output' in response else response['text']
                    st.write("### Result")
                    st.write(output_text)

                except ValueError as e:
                    st.error(f"ValueError: {e}")
                except Exception as e:
                    st.error(f"An error occurred: {e}")
        else:
            st.error("Please enter a command and a string.")
