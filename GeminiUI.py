import streamlit as st
import google.generativeai as genai
import os

# --- IMPORTANT: Configure your API Key ---
# We are hardcoding the API key here to ensure the app works on your system.
# For production or sharing, ALWAYS use environment variables for security!
# Example for setting environment variable in your terminal before running:
# Windows (PowerShell): $env:GOOGLE_API_KEY="AIzaSyA3V-gTQspbCs8dFc84jCMAsCIdEfa8sMk"
# Linux/macOS (Bash): export GOOGLE_API_KEY="AIzaSyA3V-gTQspbCs8dFc84jCMAsCIdEfa8sMk"

# >>> PASTE YOUR ACTUAL GEMINI API KEY HERE DIRECTLY <<<
# This is the key you provided: AIzaSyA3V-gTQspbCs8dFc84jCMAsCIdEfa8sMk
API_KEY = "AIzaSyA3V-gTQspbCs8dFc84jCMAsCIdEfa8sMk"

try:
    genai.configure(api_key=API_KEY)
    # st.success("Gemini API configured successfully!") # You can uncomment this if you want a temporary success message
except Exception as e:
    st.error(f"FATAL ERROR: Could not configure Gemini API. Please check your API key or internet connection. Details: {e}")
    st.stop() # Stop the Streamlit app if API key configuration fails immediately

# --- Customize Your AI Here ---
AI_NAME = "Chewmongo" # Your AI's chosen name
AI_ROLE_AND_TOPICS = f"""You are {AI_NAME}, a highly knowledgeable and friendly AI specializing exclusively in **animals**.
Your purpose is to provide information, facts, and engaging conversations about all types of animals, including their behavior, habitats, species, conservation, and fun facts.
You will NOT discuss topics outside of animals (e.g., politics, relationships, technology, general science unrelated to animals, personal opinions).
If the user asks about topics unrelated to animals, gently and politely redirect them back to your area of expertise by saying something like: "My apologies, but my expertise is solely focused on the fascinating world of animals! What animal would you like to learn about today?"
Maintain a curious, informative, and engaging tone."""


# --- Streamlit App Setup ---
# Set browser tab title and icon
st.set_page_config(page_title=f"{AI_NAME} - Your Animal AI Mentor", page_icon="🐾")

st.title(f"👋 Meet {AI_NAME}! Your Dedicated Animal AI Mentor")
# Display the AI's role, modified for conversational flow
st.write(AI_ROLE_AND_TOPICS.replace("You are", "I am"))


# Initialize chat history in Streamlit session state
# This stores messages so they persist across reruns of the app
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
# This loop redraws all past messages whenever the app updates
for message in st.session_state.messages:
    with st.chat_message(message["role"]): # Uses Streamlit's built-in chat message styling
        st.markdown(message["content"]) # Renders content, including Markdown


# --- Gemini Model Configuration ---
# Initialize the Generative Model with the specified system instruction.
# 'gemini-1.5-flash' is often a good and widely available model for text generation.
try:
    # Changed model from 'gemini-pro' to 'gemini-1.5-flash' based on previous error
    model = genai.GenerativeModel(
        'gemini-1.5-flash', # <<< THIS IS THE KEY CHANGE for model availability
        system_instruction=AI_ROLE_AND_TOPICS
    )
except Exception as e:
    st.error(f"FATAL ERROR: Could not load Gemini Generative Model. Details: {e}")
    st.stop()


# Accept user input via Streamlit's chat input widget
# The `:=` is the "walrus operator" for assignment expressions, available in Python 3.8+
if prompt := st.chat_input(f"Chat with {AI_NAME} about animals..."):
    # Add user message to chat history immediately
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Display the user's message in the chat interface
    with st.chat_message("user"):
        st.markdown(prompt)

    # Get response from Gemini in a new chat message container
    with st.chat_message("assistant"):
        with st.spinner("Chewmongo is thinking..."): # Show a spinner to indicate AI is working
            try:
                # Prepare conversation history for the Gemini model
                conversation_for_model = []
                for msg in st.session_state.messages:
                    if msg["role"] == "user":
                        conversation_for_model.append({"role": "user", "parts": [{"text": msg["content"]}]})
                    elif msg["role"] == "assistant":
                        conversation_for_model.append({"role": "model", "parts": [{"text": msg["content"]}]})

                # Start a new chat session with the accumulated history
                chat_session = model.start_chat(history=conversation_for_model[:-1])

                # Send the *current* prompt from the user
                response = chat_session.send_message(prompt)

                # Append assistant response to chat history
                st.session_state.messages.append({"role": "assistant", "content": response.text})

                # Display the AI's response using Streamlit Markdown
                st.markdown(response.text)

            except Exception as e:
                # Handle potential errors during API call (e.g., rate limits, network issues)
                st.error(f"Chewmongo encountered an error during response generation: {e}. Please try again.")
                # Optionally, remove the last user message from history if it caused an error
                # st.session_state.messages.pop()
