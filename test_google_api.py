import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

# Load environment variables
load_dotenv()

# Get the Google API key
api_key = os.getenv('GOOGLE_API_KEY')

if not api_key:
    print("Google API key not found in .env file.")
    exit(1)

# Test with Gemini API using LangChain
try:
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.0-flash-exp",  # Trying gemini-2.0-flash-exp
        temperature=0.1,
        max_output_tokens=512,
        google_api_key=api_key
    )

    # Simple test message
    response = llm.invoke("Say 'Hello, your Google API key is working!' in exactly those words.")
    print("Google Gemini API key is working!")
    print(f"Response: {response.content}")

except Exception as e:
    error_str = str(e)
    if "404" in error_str and "not found" in error_str.lower():
        print("Google Gemini API key is not valid or not authorized for Gemini API.")
        print("The model was not found. This could mean:")
        print("1. The API key is invalid")
        print("2. The API key is not enabled for Gemini API")
        print("3. You need to enable the Gemini API in your Google Cloud Console")
        print(f"Error details: {error_str}")
    else:
        print(f"Error testing Gemini API key: {e}")
        print("The API key may be invalid or not authorized for Gemini API.")
