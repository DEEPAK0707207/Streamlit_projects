
import streamlit as st

st.title("Simple Chatbot")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# Get user input
prompt = st.chat_input("Type your message...")

if prompt:
    # Save user message
    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    # Generate reply
    if "python" in prompt.lower():
        reply = "Python is a popular language for AI and data science."

    elif "streamlit" in prompt.lower():
        reply = "Streamlit is a Python framework for interactive web apps."

    else:
        reply = f"You said: '{prompt}'. I'm a demo chatbot!"

    # Save chatbot reply
    st.session_state.messages.append({
        "role": "assistant",
        "content": reply
    })

    st.rerun()

# Clear chat button
if st.button("Clear Chat"):
    st.session_state.messages = []
    st.rerun()
