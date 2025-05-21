import os
import json
import re
import google.generativeai as genai
from dotenv import load_dotenv
import traceback
import html

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
- DO NOT include any HTML tags or characters that could be interpreted as markup

Example structure:
{{
  "name": "Workflow Name",
  "nodes": [
    {{
      "parameters": {{}},
      "id": "unique-id",
      "name": "Node Name", 
      "type": "n8n-nodes-base.manualTrigger",
      "position": [x, y]
    }}
  ],
  "connections": {{
    "Node Name": {{
      "main": [[["Next Node"]]]
    }}
  }}
}}

User wants to build a workflow that does the following: {goal}

Respond with ONLY the valid JSON workflow - no additional text, comments, or code blocks.
"""

        self.name_generation_template = """
Create a concise, descriptive name for an n8n workflow based on the following description:

Goal: {goal}

The name should be brief (3-6 words), professional, and clearly indicate the workflow's purpose.
Do not include any HTML tags, XML elements, or special characters.
Respond with ONLY the name text - no quotes, no additional explanations, comments, or formatting.
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
            # Default fallback name
            default_name = f"Workflow for {goal[:40]}"
            
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
                return default_name
            
            # Clean up the name
            if name:
                # Strip whitespace, quotes, and newlines
                name = name.strip().strip('"\'').strip()
                name = re.sub(r'[\n\r\t]+', ' ', name)
                # Escape any HTML-like content
                name = html.escape(name)
                # Remove any HTML tags that might have survived
                name = re.sub(r'<[^>]*>', '', name)
                # Remove any non-alphanumeric characters that might cause issues
                name = re.sub(r'[^\w\s\-:]', '', name)
                # Limit length
                if len(name) > 60:
                    name = name[:57] + "..."
                # Final verification - if empty or just whitespace, use default
                if not name or not name.strip():
                    return default_name
                return name
            
            return default_name
        except Exception as e:
            print(f"Error generating workflow name: {e}")
            traceback.print_exc()
            return f"Workflow for {goal[:40]}"

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
                    return {
                        "success": True,
                        "workflow": self._create_fallback_workflow(goal, workflow_name),
                        "warning": "Could not extract content from API response"
                    }
                    
                # Clean up and process the response
                workflow_json_text = workflow_json_text.strip()
                
                # Remove any markdown code blocks
                workflow_json_text = re.sub(r'^```(?:json)?\s*', '', workflow_json_text)
                workflow_json_text = re.sub(r'\s*```$', '', workflow_json_text)
                
                # Sanitize any HTML-like content
                workflow_json_text = html.escape(workflow_json_text)
                workflow_json_text = re.sub(r'&quot;', '"', workflow_json_text)  # Restore JSON quotes
                workflow_json_text = re.sub(r'&lt;', '<', workflow_json_text)   # Restore < for any comparison operators
                workflow_json_text = re.sub(r'&gt;', '>', workflow_json_text)   # Restore > for any comparison operators
                
                # Find JSON object in the text
                start_idx = workflow_json_text.find('{')
                end_idx = workflow_json_text.rfind('}')
                
                if start_idx >= 0 and end_idx >= 0 and start_idx < end_idx:
                    workflow_json_text = workflow_json_text[start_idx:end_idx+1]
                    
                    try:
                        workflow_json = json.loads(workflow_json_text)
                        
                        # Ensure the workflow has a name, using our generated one if missing
                        if "name" not in workflow_json or not workflow_json["name"]:
                            workflow_json["name"] = workflow_name
                            
                        # Make sure we have required fields
                        if "nodes" not in workflow_json:
                            workflow_json["nodes"] = []
                        if "connections" not in workflow_json:
                            workflow_json["connections"] = {}
                            
                        # Ensure we have at least a manual trigger node
                        if not workflow_json["nodes"]:
                            workflow_json["nodes"].append({
                                "parameters": {},
                                "id": "1",
                                "name": "Manual Trigger", 
                                "type": "n8n-nodes-base.manualTrigger",
                                "position": [100, 300]
                            })
                            
                        return {"success": True, "workflow": workflow_json}
                    except json.JSONDecodeError as e:
                        print(f"JSON parsing error: {e}")
                        print(f"Raw text: {workflow_json_text[:200]}...")
                        
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
                    print(f"No valid JSON object found in the response")
                
                # If we get here, use fallback workflow
                return {
                    "success": True,
                    "workflow": self._create_fallback_workflow(goal, workflow_name),
                    "warning": "Could not extract valid JSON from the API response"
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
            
        # Ensure name doesn't contain HTML tags
        name = html.escape(name)
        name = re.sub(r'<[^>]*>', '', name)
        
        # Sanitize the goal text as well
        safe_goal = html.escape(goal)
            
        return {
            "name": name,
            "nodes": [
                {
                    "parameters": {},
                    "id": "1",
                    "name": "Manual Trigger", 
                    "type": "n8n-nodes-base.manualTrigger",
                    "position": [100, 300]
                },
                {
                    "parameters": {
                        "mode": "manually",
                        "text": {
                            "value": f"# {name}\n\nThis is a starter workflow for: {safe_goal}\n\nPlease customize it according to your needs."
                        }
                    },
                    "id": "2",
                    "name": "Set", 
                    "type": "n8n-nodes-base.set",
                    "position": [300, 300]
                }
            ],
            "connections": {
                "Manual Trigger": {
                    "main": [[
                        {"node": "Set", "type": "main", "index": 0}
                    ]]
                }
            }
        }
            
    def extract_workflow_steps(self, goal):
        """Extract individual steps from a workflow goal description"""
        steps = []
        
        # Split by numbered items first (1., 2., etc.)
        numbered_pattern = re.compile(r'\b(\d+)[.):]\s+([^\d][^\n]+)')
        matches = numbered_pattern.findall(goal)
        
        if matches:
            steps = [match[1].strip() for match in matches]
        else:
            # Try bullet points
            bullet_pattern = re.compile(r'(?:•|-|\*)\s+([^\n]+)')
            matches = bullet_pattern.findall(goal)
            if matches:
                steps = [match.strip() for match in matches]
            else:
                # Split by sentences as a last resort
                sentences = re.split(r'(?<=[.!?])\s+', goal)
                steps = [s.strip() for s in sentences if len(s.strip()) > 10]
        
        # If still no steps identified, treat the whole goal as one step
        if not steps:
            steps = [goal]
            
        # Sanitize all steps
        steps = [html.escape(step) for step in steps]
            
        return steps
            
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
        readme_content = self.generate_readme(workflow, folder_name)
        
        with open(readme_path, 'w') as f:
            f.write(readme_content)
            
        return base_path
        
    def generate_readme(self, workflow, folder_name, goal=None):
        """Generate a README.md file for a workflow"""
        workflow_name = workflow.get('name', 'Generated Workflow')
        
        # Extract the original goal from the folder name if not provided
        if goal is None:
            goal = folder_name.split('-', 1)[1] if '-' in folder_name else folder_name
            goal = goal.replace('-', ' ').title()
        
        # Sanitize all text content
        workflow_name = html.escape(workflow_name)
        goal = html.escape(goal)
        
        readme_content = f"# {workflow_name}\n\n"
        readme_content += f"Categories: AI, Engineering\n\n"
        readme_content += f"This workflow automates the following task: {goal}\n\n"
        
        # Extract workflow description from workflow if available
        workflow_description = workflow.get('description', '')
        if workflow_description:
            workflow_description = html.escape(workflow_description)
            readme_content += f"{workflow_description}\n\n"
        
        # Add an example section
        readme_content += f"Example: This workflow can be used to {goal.lower()}. It automates the process and saves time by eliminating manual steps.\n\n"
        
        readme_content += f"## What You Can Do\n"
        
        # Extract and display steps
        steps = self.extract_workflow_steps(goal)
        for step in steps:
            readme_content += f"- {step}\n"
        readme_content += "\n"
            
        # Count nodes by type to give a technical overview
        node_types = {}
        for node in workflow.get('nodes', []):
            node_type = node.get('type', '').replace('n8n-nodes-base.', '')
            if node_type not in node_types:
                node_types[node_type] = []
            node_types[node_type].append(node.get('name', node_type))
        
        if node_types:
            readme_content += "## Technical Details\n\n"
            readme_content += "This workflow uses the following node types:\n\n"
            for node_type, nodes in node_types.items():
                # Sanitize node info
                node_type = html.escape(node_type)
                node_names = ", ".join([html.escape(name) for name in nodes])
                readme_content += f"- {node_type}: {node_names}\n"
            readme_content += "\n"
        
        # Add a quick start section
        readme_content += "## Quick Start\n"
        readme_content += "1. Import this workflow to n8n\n"
        readme_content += "2. Configure your settings\n"
        readme_content += "3. Start automating!\n\n"
        
        return readme_content 