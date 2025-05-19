import os
import json
import re
import google.generativeai as genai
from dotenv import load_dotenv
import traceback

load_dotenv()

# Configure the Gemini API
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
else:
    print("Warning: GEMINI_API_KEY not found in environment variables")

class N8nWorkflowBuilder:
    def __init__(self):
        # Use the specified model requested by user
        self.model = genai.GenerativeModel('gemini-2.5-pro-preview-03-25')
        print(f"Using Gemini model: gemini-2.5-pro-preview-03-25")
        
        # Remove model listing to keep logs cleaner
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
- Set the "name" field to a concise, descriptive title based on the automation's purpose

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

        self.name_generation_template = """
Create a concise, descriptive name for an n8n workflow based on the following description:

"{goal}"

The name should be brief (3-6 words), professional, and clearly indicate the workflow's purpose.
Respond with ONLY the name, nothing else.
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

    async def generate_workflow_name(self, goal):
        """Generate a descriptive name for the workflow based on the goal"""
        try:
            prompt = self.name_generation_template.format(goal=goal)
            response = await self.model.generate_content_async(prompt)
            
            # Extract text from response
            name = None
            try:
                if hasattr(response, 'text'):
                    name = response.text
                elif hasattr(response, 'parts') and response.parts:
                    name = response.parts[0].text
                # Add other extraction methods as needed
            except Exception as e:
                print(f"Error extracting name: {e}")
            
            # Clean up the name
            if name:
                name = name.strip().strip('"\'').strip()
                # Limit length
                if len(name) > 60:
                    name = name[:57] + "..."
                return name
            
            return f"Workflow: {goal[:40]}"
        except Exception as e:
            print(f"Error generating workflow name: {e}")
            return f"Workflow: {goal[:40]}"

    async def generate_workflow(self, goal):
        try:
            # First generate a descriptive name
            workflow_name = await self.generate_workflow_name(goal)
            print(f"Generated workflow name: {workflow_name}")
            
            # First check the API connection
            api_test = await self.test_api_connection()
            if not api_test["success"]:
                return {
                    "success": True,
                    "workflow": self._create_fallback_workflow(goal, workflow_name),
                    "warning": f"API connection issue: {api_test['error']}"
                }
            
            # Generate the workflow
            prompt = self.prompt_template.format(goal=goal)
            
            try:
                response = await self.model.generate_content_async(prompt)
                print(f"Response type: {type(response)}")
                print(f"Response attributes: {dir(response)}")
                
                # Extract text from response based on response structure
                workflow_json_text = None
                
                # Try all possible ways to access the content
                try:
                    if hasattr(response, 'text'):
                        workflow_json_text = response.text
                    elif hasattr(response, 'parts') and response.parts:
                        workflow_json_text = response.parts[0].text
                    elif hasattr(response, 'candidates') and response.candidates:
                        if hasattr(response.candidates[0], 'content'):
                            if hasattr(response.candidates[0].content, 'parts'):
                                workflow_json_text = response.candidates[0].content.parts[0].text
                            elif hasattr(response.candidates[0].content, 'text'):
                                workflow_json_text = response.candidates[0].content.text
                    
                    # Direct attribute access as a last resort
                    if workflow_json_text is None:
                        try:
                            # Try to access it as a dictionary
                            if isinstance(response, dict):
                                if 'text' in response:
                                    workflow_json_text = response['text']
                                elif 'candidates' in response:
                                    workflow_json_text = response['candidates'][0]['content']['parts'][0]['text']
                        except (KeyError, TypeError, IndexError) as e:
                            print(f"Dictionary access failed: {e}")
                            
                except Exception as e:
                    print(f"Error extracting text: {e}")
                    
                if workflow_json_text is None:
                    print(f"Could not extract text from response: {response}")
                    # Try serializing the entire response
                    try:
                        if hasattr(response, '__dict__'):
                            print(f"Response dict: {response.__dict__}")
                    except:
                        pass
                        
                    return {
                        "success": True,
                        "workflow": self._create_fallback_workflow(goal, workflow_name),
                        "warning": "Could not extract content from API response"
                    }
                    
                # Clean up and process the response
                workflow_json_text = workflow_json_text.strip()
                workflow_json_text = re.sub(r'^```json\s*', '', workflow_json_text)
                workflow_json_text = re.sub(r'^```\s*', '', workflow_json_text)
                workflow_json_text = re.sub(r'\s*```$', '', workflow_json_text)
                
                print(f"Extracted text: {workflow_json_text[:200]}...")
                
                # Find JSON object in the text
                start_idx = workflow_json_text.find('{')
                end_idx = workflow_json_text.rfind('}')
                
                if start_idx >= 0 and end_idx >= 0:
                    workflow_json_text = workflow_json_text[start_idx:end_idx+1]
                    
                    try:
                        workflow_json = json.loads(workflow_json_text)
                        
                        # Ensure the workflow has a name, using our generated one if missing
                        if "name" not in workflow_json or not workflow_json["name"]:
                            workflow_json["name"] = workflow_name
                            
                        return {"success": True, "workflow": workflow_json}
                    except json.JSONDecodeError as e:
                        print(f"JSON parsing error: {e}")
                        print(f"Raw text: {workflow_json_text}")
                        
                        # Try to do more aggressive cleanup
                        clean_text = re.sub(r'[\n\r\t]', ' ', workflow_json_text)
                        clean_text = re.sub(r'\s+', ' ', clean_text)
                        
                        try:
                            workflow_json = json.loads(clean_text)
                            
                            # Ensure the workflow has a name, using our generated one if missing
                            if "name" not in workflow_json or not workflow_json["name"]:
                                workflow_json["name"] = workflow_name
                                
                            return {"success": True, "workflow": workflow_json}
                        except:
                            pass
                else:
                    print(f"No JSON object found in: {workflow_json_text}")
                
                # If we get here, use fallback workflow
                return {
                    "success": True,
                    "workflow": self._create_fallback_workflow(goal, workflow_name),
                    "warning": "Could not extract valid JSON from the API response",
                    "raw_response": workflow_json_text[:500] if len(workflow_json_text) > 500 else workflow_json_text
                }
                    
            except Exception as e:
                print(f"Error calling Gemini API: {e}")
                print(f"Exception type: {type(e)}")
                traceback.print_exc()
                return {
                    "success": True,
                    "workflow": self._create_fallback_workflow(goal, workflow_name),
                    "warning": f"Error calling Gemini API: {str(e)}"
                }
                
        except Exception as e:
            print(f"Exception in generate_workflow: {str(e)}")
            print(f"Exception type: {type(e)}")
            traceback.print_exc()
            return {
                "success": True,
                "workflow": self._create_fallback_workflow(goal),
                "warning": f"Error generating workflow: {str(e)}"
            }
    
    def _create_fallback_workflow(self, goal, name=None):
        """Create a basic valid workflow as a fallback"""
        if name is None:
            name = f"Workflow for: {goal[:50]}"
            
        return {
            "name": name,
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
        
        # Extract the original goal from the folder name
        goal = folder_name.split('-', 1)[1] if '-' in folder_name else folder_name
        goal = goal.replace('-', ' ').title()
        
        readme_content = f"# {workflow_name}\n\n"
        readme_content += f"## Purpose\n\n"
        readme_content += f"This workflow automates the following task: {goal}\n\n"
        readme_content += f"## Overview\n\n"
        
        # Count nodes by type to give an overview
        node_types = {}
        for node in workflow.get('nodes', []):
            node_type = node.get('type', '').replace('n8n-nodes-base.', '')
            node_types[node_type] = node_types.get(node_type, 0) + 1
        
        if node_types:
            readme_content += "This workflow uses the following node types:\n\n"
            for node_type, count in node_types.items():
                readme_content += f"- {node_type}: {count}\n"
            readme_content += "\n"
        
        readme_content += "This workflow was generated by the n8n workflow builder.\n\n"
        readme_content += "Categories: AI, Engineering\n"
        
        with open(readme_path, 'w') as f:
            f.write(readme_content)
            
        # Create meta.json
        meta_path = os.path.join(base_path, 'meta.json')
        meta = {
            "categories": ["AI", "Engineering"],
            "generated": True,
            "summary": f"Automated workflow for: {goal}"
        }
        
        with open(meta_path, 'w') as f:
            json.dump(meta, f, indent=2)
            
        return base_path 