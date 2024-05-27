import streamlit as st

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
                    # Parse the command and text from the user input
                    parts = user_input.split(maxsplit=1)
                    if len(parts) < 2:
                        st.error("Please enter both a command and a string.")
                        raise ValueError("Incomplete input")

                    command = parts[0]
                    text = parts[1]

                    if command not in tools:
                        st.error("Invalid command. Use 'reverse', 'uppercase', or 'length'.")
                        raise ValueError("Invalid command")

                    # Execute the tool directly
                    result = tools[command](text)
                    
                    st.write("### Result")
                    st.write(result)

                except ValueError:
                    pass  # Error already handled by st.error
                except Exception as e:
                    st.error(f"An error occurred: {e}")
        else:
            st.error("Please enter a command and a string.")
