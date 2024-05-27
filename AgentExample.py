import streamlit as st
import openai

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
tools = {
    "reverse": reverse_string,
    "uppercase": to_uppercase,
    "length": get_length
}

# Check if API key is valid
if not openai_api_key.startswith('sk-'):
    st.warning('Please enter your OpenAI API key!', icon='⚠')
else:
    user_input = st.text_input("Enter your command (reverse, uppercase, length) followed by the string:")
    if st.button("Execute"):
        if user_input:
            with st.spinner("Processing..."):
                try:
                    # Initialize the OpenAI API client
                    openai.api_key = openai_api_key

                    # Define the prompt
                    prompt = f"You are a helpful assistant that can perform various string operations.\n" \
                             f"You have access to the following tools:\n" \
                             f"- reverse: Reverses the input string.\n" \
                             f"- uppercase: Converts the input string to uppercase.\n" \
                             f"- length: Returns the length of the input string.\n" \
                             f"The user will provide you with a command, and you will use the appropriate tool to perform the operation.\n" \
                             f"Command: {user_input}\n"

                    # Generate response using OpenAI API
                    response = openai.Completion.create(
                        engine="text-davinci-003",
                        prompt=prompt,
                        max_tokens=150
                    )

                    st.write("### Result")
                    st.write(response.choices[0].text.strip())

                except Exception as e:
                    st.error(f"An error occurred: {e}")
        else:
            st.error("Please enter a command and a string.")
