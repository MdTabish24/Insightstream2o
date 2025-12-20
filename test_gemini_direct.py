#!/usr/bin/env python
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv('GEMINI_API_KEY_1')
print(f"Testing API Key: {api_key[:10]}...{api_key[-4:]}")

try:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-2.0-flash-exp')
    
    print("\nSending test request...")
    response = model.generate_content("Say hello in 3 words")
    print(f"Success! Response: {response.text}")
    
except Exception as e:
    print(f"\nError: {str(e)}")
    print(f"Error type: {type(e).__name__}")
    
    # Try with older model
    try:
        print("\nTrying with gemini-pro model...")
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content("Say hello in 3 words")
        print(f"Success with gemini-pro! Response: {response.text}")
    except Exception as e2:
        print(f"Also failed: {str(e2)}")
