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
        self.model = genai.GenerativeModel('gemini-pro')
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

    async def generate_workflow(self, goal):
        try:
            prompt = self.prompt_template.format(goal=goal)
            response = await self.model.generate_content_async(prompt)
            
            # Extract JSON from response
            workflow_json_text = response.text
            
            # Clean up response - sometimes the API returns with markdown code blocks or has leading/trailing whitespace
            workflow_json_text = workflow_json_text.strip()
            workflow_json_text = re.sub(r'^```json\s*', '', workflow_json_text)
            workflow_json_text = re.sub(r'^```\s*', '', workflow_json_text)
            workflow_json_text = re.sub(r'\s*```$', '', workflow_json_text)
            
            # Additional cleanup for common issues
            if workflow_json_text.startswith('"') and not workflow_json_text.startswith('{"'):
                # Sometimes Gemini returns JSON with extraneous quotes or newlines at the beginning
                workflow_json_text = '{' + workflow_json_text.split('{', 1)[1]
            
            # Handle extraneous text before/after the JSON
            try:
                # Find the first { and last } to extract just the JSON object
                start_idx = workflow_json_text.find('{')
                end_idx = workflow_json_text.rfind('}')
                
                if start_idx >= 0 and end_idx >= 0:
                    workflow_json_text = workflow_json_text[start_idx:end_idx+1]
                
                workflow_json = json.loads(workflow_json_text)
                return {"success": True, "workflow": workflow_json}
            except json.JSONDecodeError as e:
                print(f"Raw text from API: {workflow_json_text}")
                print(f"JSON error: {e}")
                
                # Attempt to create a basic valid workflow if parsing fails
                fallback_workflow = {
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
                
                return {
                    "success": True, 
                    "workflow": fallback_workflow,
                    "warning": "Used fallback workflow due to API response parsing issue",
                    "raw_text": workflow_json_text
                }
                
        except Exception as e:
            print(f"Exception in generate_workflow: {str(e)}")
            print(f"Exception type: {type(e)}")
            return {"success": False, "error": f"Error generating workflow: {str(e)}"}
            
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