import google.generativeai as genai
import os
import streamlit as st

# Try to get key from secrets or environment
api_key = None
try:
    # Mocking streamlit secrets access for standalone script if needed, 
    # but since we run this in the same env, we might need to read the file directly or rely on env vars.
    # For this script, let's try to read from the app.py logic or just ask the user? 
    # Actually, I can't ask the user. I'll try to find the key in the app.py process or just use a placeholder 
    # if I can't find it. 
    # Wait, the user enters the key in the UI or it's in secrets.
    # I will assume it's in secrets.toml if it exists.
    pass
except:
    pass

# Since I can't easily access the Streamlit secrets from a standalone script without the streamlit context 
# (unless I parse .streamlit/secrets.toml), I will try to use the `app.py` itself to debug or 
# just try `gemini-pro` which is the safest fallback.

# However, to be precise, I will try to read .streamlit/secrets.toml if it exists.
import toml
try:
    secrets = toml.load(".streamlit/secrets.toml")
    # Flatten secrets to find any API key
    def find_key(d):
        for k, v in d.items():
            if isinstance(v, dict):
                res = find_key(v)
                if res: return res
            elif "API_KEY" in k.upper() or "GOOGLE" in k.upper():
                return v
        return None
    
    api_key = find_key(secrets)
except Exception as e:
    print(f"Could not load secrets: {e}")

if not api_key:
    print("No API key found in secrets. Please ensure a key is set.")
else:
    print(f"Found API Key: {api_key[:5]}...")
    genai.configure(api_key=api_key)
    try:
        print("Listing models...")
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                print(m.name)
    except Exception as e:
        print(f"Error listing models: {e}")
