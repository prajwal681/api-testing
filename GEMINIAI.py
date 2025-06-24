import google.generativeai as genai
import os

# --- IMPORTANT: Configure your API Key ---
# Make sure to replace "PASTE_YOUR_ACTUAL_API_KEY_HERE" with your REAL API KEY!
# This is for testing. For production, ALWAYS use environment variables.

API_KEY_FROM_ENV = os.environ.get("GOOGLE_API_KEY")

# --- DEBUGGING LINE (Optional, you can remove after this works) ---
print(f"DEBUG: Retrieved API Key from Env (first 5 chars): {API_KEY_FROM_ENV[:5] if API_KEY_FROM_ENV else 'None'}")
# --- END DEBUGGING LINE ---

# Configure the API key. Try environment variable first, then hardcode for quick testing.
if API_KEY_FROM_ENV:
    genai.configure(api_key=API_KEY_FROM_ENV)
else:
    # >>> CHANGE THIS LINE: PASTE YOUR ACTUAL API KEY HERE <<<
    genai.configure(api_key="PASTE_YOUR_ACTUAL_API_KEY_HERE")
    print("WARNING: API Key directly pasted in code. Remember to use environment variable for production!")


# >>> REMOVE OR COMMENT OUT THIS ENTIRE BLOCK (LINES 17-21 in my original code) <<<
# if genai.get_default_api_key() is None:
#     print("Error: GOOGLE_API_KEY environment variable not set or API key not configured.")
#     print("Please set the GOOGLE_API_KEY environment variable or paste your key directly (temporarily).")
#     exit()
# >>> END REMOVAL/COMMENT OUT <<<


# Initialize the Generative Model
# 'gemini-pro' is good for general text. For faster, cheaper, use 'gemini-1.5-flash'.
model = genai.GenerativeModel('gemini-pro')

print("Hello, I am Gemini AI. How can I help you tonight? (Type 'exit' or 'quit' to end)")

while True:
    user_prompt = input("You: ")
    if user_prompt.lower() in ["exit", "quit"]:
        print("Gemini: Goodbye, for now! Keep building.")
        break

    try:
        # Send the user's prompt to the Gemini model
        response = model.generate_content(user_prompt)

        # Print the model's response
        print("Gemini:", response.text)

    except Exception as e:
        # Catch potential errors (like hitting rate limits or network issues)
        print(f"Gemini encountered an error: {e}")
        print("Please try again, or check your API key and internet connection.")