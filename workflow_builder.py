import os
import json
import re
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

# Configure the Gemini API
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
else:
    print("Warning: GEMINI_API_KEY not found in environment variables")

class N8nWorkflowBuilder:
    def __init__(self):
        self.model = genai.GenerativeModel('gemini-1.5-pro')
        
        # Print model availability for debugging
        print(f"Available Gemini models:")
        try:
            models = genai.list_models()
            for model in models:
                print(f"- {model.name}")
        except Exception as e:
            print(f"Error listing models: {e}")
            
        self.prompt_template = """
You are an expert n8n workflow builder. Generate complete, valid n8n workflow JSON files.

Input: User describes their automation goal
Output: Valid n8n workflow JSON that can be imported directly

Requirements:
- Use proper n8n node structure with id, name, type, parameters
- Include connections between nodes
- Set appropriate node positions for visual layout
- Use realistic node configurations
- Always include a manual trigger node as entry point
- Ensure all required fields are present

Example structure:
{
  "name": "Workflow Name",
  "nodes": [
    {
      "parameters": {},
      "id": "unique-id",
      "name": "Node Name", 
      "type": "n8n-nodes-base.manualTrigger",
      "position": [x, y]
    }
  ],
  "connections": {
    "Node Name": {
      "main": [["Next Node"]]
    }
  }
}

User's automation goal: {goal}

Respond only with the JSON workflow, no explanations.
"""

    async def test_api_connection(self):
        """Test if the Gemini API is working properly"""
        try:
            # Simple test prompt
            test_response = await self.model.generate_content_async("Say hello world")
            
            # Try to access the response content
            if hasattr(test_response, 'text'):
                return {
                    "success": True,
                    "message": "API connection successful",
                    "response": test_response.text[:100] + "..." if len(test_response.text) > 100 else test_response.text
                }
            else:
                # Try alternative access
                if hasattr(test_response, 'parts') and len(test_response.parts) > 0:
                    return {
                        "success": True,
                        "message": "API connection successful (using parts)",
                        "response": str(test_response.parts[0])[:100]
                    }
                else:
                    return {
                        "success": False,
                        "error": "API connected but returned an unexpected response format",
                        "response_type": str(type(test_response))
                    }
        except Exception as e:
            return {
                "success": False,
                "error": f"API connection failed: {str(e)}",
                "error_type": str(type(e))
            }

    async def generate_workflow(self, goal):
        try:
            # First check the API connection
            api_test = await self.test_api_connection()
            if not api_test["success"]:
                return {
                    "success": True,
                    "workflow": self._create_fallback_workflow(goal),
                    "warning": f"API connection issue: {api_test['error']}"
                }
            
            # Generate the workflow
            prompt = self.prompt_template.format(goal=goal)
            response = await self.model.generate_content_async(prompt)
            
            # Extract text from response based on response structure
            workflow_json_text = ""
            if hasattr(response, 'text'):
                workflow_json_text = response.text
            elif hasattr(response, 'parts') and len(response.parts) > 0:
                workflow_json_text = response.parts[0].text
            elif hasattr(response, 'candidates') and len(response.candidates) > 0:
                if hasattr(response.candidates[0], 'content') and hasattr(response.candidates[0].content, 'parts'):
                    workflow_json_text = response.candidates[0].content.parts[0].text
            
            if not workflow_json_text:
                print(f"Empty response from API: {response}")
                return {
                    "success": True,
                    "workflow": self._create_fallback_workflow(goal),
                    "warning": "Empty response from API"
                }
            
            # Clean up response
            workflow_json_text = workflow_json_text.strip()
            workflow_json_text = re.sub(r'^```json\s*', '', workflow_json_text)
            workflow_json_text = re.sub(r'^```\s*', '', workflow_json_text)
            workflow_json_text = re.sub(r'\s*```$', '', workflow_json_text)
            
            # Find JSON object in the text
            start_idx = workflow_json_text.find('{')
            end_idx = workflow_json_text.rfind('}')
            
            if start_idx >= 0 and end_idx >= 0:
                workflow_json_text = workflow_json_text[start_idx:end_idx+1]
                
                try:
                    workflow_json = json.loads(workflow_json_text)
                    return {"success": True, "workflow": workflow_json}
                except json.JSONDecodeError as e:
                    print(f"JSON parsing error: {e}")
                    print(f"Raw text: {workflow_json_text}")
            else:
                print(f"No JSON object found in: {workflow_json_text}")
            
            # If we get here, use fallback workflow
            return {
                "success": True,
                "workflow": self._create_fallback_workflow(goal),
                "warning": "Could not extract valid JSON from the API response",
                "raw_response": workflow_json_text[:500] if len(workflow_json_text) > 500 else workflow_json_text
            }
                
        except Exception as e:
            print(f"Exception in generate_workflow: {str(e)}")
            print(f"Exception type: {type(e)}")
            return {
                "success": True,
                "workflow": self._create_fallback_workflow(goal),
                "warning": f"Error generating workflow: {str(e)}"
            }
    
    def _create_fallback_workflow(self, goal):
        """Create a basic valid workflow as a fallback"""
        return {
            "name": f"Workflow for: {goal[:50]}",
            "nodes": [
                {
                    "parameters": {},
                    "id": "1",
                    "name": "Manual Trigger", 
                    "type": "n8n-nodes-base.manualTrigger",
                    "position": [100, 300]
                }
            ],
            "connections": {}
        }
            
    def save_workflow(self, workflow, folder_name):
        """Save a generated workflow to the automation directory"""
        base_path = os.path.join(os.path.dirname(__file__), 'automation', folder_name)
        
        # Create directory if it doesn't exist
        os.makedirs(base_path, exist_ok=True)
        
        # Save workflow.json
        workflow_path = os.path.join(base_path, 'workflow.json')
        with open(workflow_path, 'w') as f:
            json.dump(workflow, f, indent=2)
            
        # Create basic README.md
        readme_path = os.path.join(base_path, 'README.md')
        workflow_name = workflow.get('name', 'Generated Workflow')
        readme_content = f"# {workflow_name}\n\n"
        readme_content += "This workflow was generated by the n8n workflow builder.\n\n"
        readme_content += "Categories: AI, Engineering\n"
        
        with open(readme_path, 'w') as f:
            f.write(readme_content)
            
        # Create meta.json
        meta_path = os.path.join(base_path, 'meta.json')
        meta = {
            "categories": ["AI", "Engineering"],
            "generated": True
        }
        
        with open(meta_path, 'w') as f:
            json.dump(meta, f, indent=2)
            
        return base_path 