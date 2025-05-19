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
        # Try the requested model
        model_name = "gemini-2.5-pro-preview-03-25"
        
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
                
            # Test generating a workflow
            print("\nTesting workflow generation:")
            workflow_prompt = """
Generate an n8n workflow JSON that sends a daily email with weather updates.
The workflow should include proper node structure, connections, and parameters.
Respond with just the valid JSON workflow.
"""
            workflow_response = await model.generate_content_async(workflow_prompt)
            
            if hasattr(workflow_response, 'text'):
                print(f"✅ Workflow response received (first 200 chars):\n{workflow_response.text[:200]}...")
            elif hasattr(workflow_response, 'parts') and len(workflow_response.parts) > 0:
                print(f"✅ Workflow response received (via parts, first 200 chars):\n{workflow_response.parts[0].text[:200]}...")
            else:
                print(f"❓ Unexpected workflow response format")
                
        except Exception as e:
            print(f"❌ Error with {model_name}: {e}")
    
    except Exception as e:
        print(f"❌ General error: {e}")

if __name__ == "__main__":
    asyncio.run(test_api()) 