import streamlit as st
import requests

# Show title and description.
st.title("💬 Chatbot")
st.write(
    "This is a simple chatbot that uses the Gemini API to generate responses. "
    "To use this app, you need to provide a Gemini API key, which you can get from the Gemini platform."
)

# Ask user for their Gemini API key via `st.text_input`.
gemini_api_key = st.text_input("Gemini API Key", type="password")
if not gemini_api_key:
    st.info("Please add your Gemini API key to continue.", icon="🗝️")
else:

    # Create a session state variable to store the chat messages. This ensures that the
    # messages persist across reruns.
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display the existing chat messages via `st.chat_message`.
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Create a chat input field to allow the user to enter a message. This will display
    # automatically at the bottom of the page.
    if prompt := st.chat_input("What is up?"):

        # Store and display the current prompt.
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Generate a response using the Gemini API.
        headers = {
            "Authorization": f"Bearer {gemini_api_key}",
            "Content-Type": "application/json",
        }
        payload = {
            "model": "gemini-free",  # Replace with the appropriate model name for Gemini
            "messages": [
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
        }
        response = requests.post(
            "https://api.gemini-platform.com/v1/chat/completions",  # Replace with the correct Gemini API endpoint
            headers=headers,
            json=payload,
        )

        if response.status_code == 200:
            response_data = response.json()
            assistant_message = response_data.get("choices", [{}])[0].get("message", {}).get("content", "")
            
            # Stream the response to the chat and store it in session state.
            with st.chat_message("assistant"):
                st.markdown(assistant_message)
            st.session_state.messages.append({"role": "assistant", "content": assistant_message})
        else:
            st.error(f"Error: {response.status_code} - {response.text}")