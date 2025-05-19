#!/usr/bin/env python3
import os
import sys
import json
import asyncio
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

# Configure the Gemini API
API_KEY = os.environ.get('GEMINI_API_KEY')
if not API_KEY:
    print("Error: GEMINI_API_KEY not found in environment variables")
    sys.exit(1)

genai.configure(api_key=API_KEY)

async def test_api():
    print("Testing Gemini API connection...")
    
    # List available models
    print("\nAvailable models:")
    try:
        models = genai.list_models()
        for model in models:
            print(f"- {model.name}")
    except Exception as e:
        print(f"Error listing models: {e}")
    
    # Test the API with a simple prompt
    print("\nTesting model generation:")
    try:
        # Try different model versions
        model_versions = [
            "gemini-1.5-pro", 
            "gemini-1.5-flash",
            "gemini-pro", 
            "gemini-pro-vision"
        ]
        
        for model_name in model_versions:
            try:
                print(f"\nTesting model: {model_name}")
                model = genai.GenerativeModel(model_name)
                response = await model.generate_content_async("Say hello world")
                
                if hasattr(response, 'text'):
                    print(f"✅ Response: {response.text[:100]}...")
                elif hasattr(response, 'parts') and len(response.parts) > 0:
                    print(f"✅ Response (via parts): {response.parts[0].text[:100]}...")
                else:
                    print(f"❓ Unexpected response format: {response}")
            except Exception as e:
                print(f"❌ Error with {model_name}: {e}")
    
    except Exception as e:
        print(f"❌ General error: {e}")

if __name__ == "__main__":
    asyncio.run(test_api()) 