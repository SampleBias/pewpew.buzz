import os
import json
import re
import google.generativeai as genai
from dotenv import load_dotenv
import traceback
import html
import asyncio

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
        self.model = genai.GenerativeModel('gemini-2.0-flash')
        print(f"Using Gemini model: gemini-2.0-flash")
        
        # Remove model listing to keep logs cleaner
        self.prompt_template = """
You are an expert n8n workflow builder. Generate complete, valid n8n workflow JSON files.

# System Prompt for n8n Website Summary Workflow Generator

You are a specialized n8n workflow assistant. Your purpose is to help users create, modify, and optimize n8n automation workflows. When presented with workflow JSON, you will:

1. Clean and validate the JSON format by:
   - Replacing HTML entities (`&quot;`) with their proper characters (`"`)
   - Ensuring proper quote formatting throughout
   - Checking for and fixing any malformed JSON syntax

2. Provide an enhanced workflow with:
   - Clear documentation explaining each node's purpose
   - Improved error handling where applicable
   - Proper parameterization for maximum flexibility
   - Security considerations like credential handling

3. Describe the workflow's functionality in simple terms:
   - What triggers the workflow
   - What each step accomplishes
   - What the final output will be
   - How to modify it for different use cases

4. Offer customization suggestions:
   - How to handle different website structures
   - How to modify the OpenAI prompt for different summary styles
   - How to extend the workflow with additional functionality

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
- Clean and validate the JSON format, replacing any HTML entities with proper characters
- Add proper documentation in the workflow description
- Include error handling nodes where appropriate

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

        # Add a new system prompt for image extraction
        self.image_extraction_prompt = """
# System Prompt for n8n Workflow Image Extraction

You are a specialized n8n workflow assistant focused on extracting workflows from images. Your purpose is to analyze screenshots of n8n workflows and convert them into valid JSON configurations. When analyzing a workflow image, you will:

1. Clean and validate the JSON format by:
   - Replacing HTML entities (`&quot;`) with their proper characters (`"`)
   - Ensuring proper quote formatting throughout
   - Checking for and fixing any malformed JSON syntax

2. Provide an enhanced workflow with:
   - Clear documentation explaining each node's purpose
   - Improved error handling where applicable
   - Proper parameterization for maximum flexibility
   - Security considerations like credential handling

3. Describe the workflow's functionality in simple terms:
   - What triggers the workflow
   - What each step accomplishes
   - What the final output will be
   - How to modify it for different use cases

4. Offer customization suggestions:
   - How to handle different input scenarios
   - How to modify the workflow for different use cases
   - How to extend the workflow with additional functionality

When analyzing an image:
1. Identify all visible nodes and their positions
2. Determine the node types and configurations
3. Map the connections between nodes
4. Create a valid, executable n8n workflow JSON

Follow these guidelines:
- Use proper n8n node structure with id, name, type, parameters
- Include connections between nodes based on the visible flow
- Set appropriate node positions for visual layout
- Use realistic node configurations based on visible settings
- Include a manual trigger node if the entry point is visible
- Ensure all required fields are present
- Set the "name" field to a concise, descriptive title based on the workflow's apparent purpose
- DO NOT include any HTML tags or characters that could be interpreted as markup
"""

    async def test_api_connection(self):
        """Test if the Gemini API is working properly"""
        try:
            # Simple test prompt
            try:
                # Set a 3-second timeout for the API test
                test_response = await asyncio.wait_for(
                    self.model.generate_content_async("Say hello world"),
                    timeout=3.0
                )
            except asyncio.TimeoutError:
                return {
                    "success": False,
                    "error": "API connection timed out",
                    "error_type": "timeout"
                }
            
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
            
            try:
                # Set a 5-second timeout for name generation - this is less critical than the workflow itself
                response = await asyncio.wait_for(
                    self.model.generate_content_async(prompt),
                    timeout=5.0
                )
            except asyncio.TimeoutError:
                print(f"Name generation timed out for goal: {goal[:30]}...")
                return default_name
            
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
                # Configure a timeout for the API call to avoid Heroku H12 errors
                # Using a 15-second timeout to leave more room for processing time
                try:
                    # Use asyncio.wait_for with a timeout
                    response = await asyncio.wait_for(
                        self.model.generate_content_async(prompt),
                        timeout=15.0
                    )
                except asyncio.TimeoutError:
                    print(f"API call timed out while generating workflow for goal: {goal[:50]}...")
                    return {
                        "success": True,
                        "workflow": self._create_fallback_workflow(goal, f"Timeout: {workflow_name}"),
                        "warning": "The API call timed out. A simple fallback workflow has been created. Please try again with a simpler request."
                    }
                
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
                        except:
                            pass
                            
                    if workflow_json_text:
                        # Clean up the response text to extract the JSON
                        # 1. Remove any markdown code blocks
                        workflow_json_text = re.sub(r'^```(?:json)?\s*', '', workflow_json_text)
                        workflow_json_text = re.sub(r'\s*```$', '', workflow_json_text)
                        
                        # 2. Find JSON object in the text - look for curly braces
                        start_idx = workflow_json_text.find('{')
                        end_idx = workflow_json_text.rfind('}')
                        
                        if start_idx >= 0 and end_idx >= 0 and start_idx < end_idx:
                            workflow_json_text = workflow_json_text[start_idx:end_idx+1]
                            
                            # 3. Clean the JSON text to replace HTML entities
                            workflow_json_text = self._clean_json_format(workflow_json_text)
                            
                            # 4. Try to parse as JSON
                            try:
                                workflow_json = json.loads(workflow_json_text)
                                
                                # 5. Sanitize and standardize the JSON structure
                                workflow_json = self._standardize_workflow_format(workflow_json, workflow_name)
                                    
                                return {"success": True, "workflow": workflow_json}
                            except json.JSONDecodeError as e:
                                print(f"JSON parsing error: {e}")
                                print(f"Raw text: {workflow_json_text[:200]}...")
                                
                                # Try to do more aggressive cleanup
                                clean_text = re.sub(r'[\n\r\t]', ' ', workflow_json_text)
                                clean_text = re.sub(r'\s+', ' ', clean_text)
                                clean_text = re.sub(r'<[^{}\[\]"\']*?>', '', clean_text)
                                clean_text = self._clean_json_format(clean_text)
                                
                                try:
                                    workflow_json = json.loads(clean_text)
                                    workflow_json = self._standardize_workflow_format(workflow_json, workflow_name)
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
                    print(f"Error extracting response content: {e}")
                    print(f"Exception type: {type(e)}")
                    traceback.print_exc()
                    return {
                        "success": True,
                        "workflow": self._create_fallback_workflow(goal, workflow_name),
                        "warning": f"Error extracting content from API response: {str(e)}"
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
    
    def _clean_json_format(self, json_text):
        """Clean JSON text by replacing HTML entities with proper characters"""
        # Replace common HTML entities
        replacements = {
            '&quot;': '"',
            '&amp;': '&',
            '&lt;': '<',
            '&gt;': '>',
            '&apos;': "'",
            '&#x27;': "'",
            '&#34;': '"',
            '&#39;': "'",
            '&#60;': '<',
            '&#62;': '>'
        }
        
        for entity, char in replacements.items():
            json_text = json_text.replace(entity, char)
            
        return json_text

    def _standardize_workflow_format(self, workflow_json, workflow_name):
        """Standardize the workflow JSON format to match n8n requirements"""
        # Ensure the workflow has a name
        if "name" not in workflow_json or not workflow_json["name"]:
            workflow_json["name"] = workflow_name
            
        # Ensure basic structure
        if "nodes" not in workflow_json:
            workflow_json["nodes"] = []
        if "connections" not in workflow_json:
            workflow_json["connections"] = {}
            
        # Remove description if present (it's not in the standard format)
        if "description" in workflow_json:
            # We could move important info from description to node notes
            # For now, just remove it to match the standard format
            del workflow_json["description"]
            
        # Add typeVersion to nodes if missing
        for node in workflow_json["nodes"]:
            if "typeVersion" not in node:
                node["typeVersion"] = 1
                
        # Ensure the workflow has at least a manual trigger node
        if not workflow_json["nodes"]:
            workflow_json["nodes"].append({
                "parameters": {},
                "id": "1",
                "name": "Manual Trigger", 
                "type": "n8n-nodes-base.manualTrigger",
                "position": [100, 300],
                "typeVersion": 1
            })
        
        # If no version field, add it
        if "version" not in workflow_json:
            workflow_json["version"] = 1
            
        return workflow_json
            
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
                    "position": [100, 300],
                    "typeVersion": 1
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
                    "position": [300, 300],
                    "typeVersion": 1
                }
            ],
            "connections": {
                "Manual Trigger": {
                    "main": [[
                        {"node": "Set", "type": "main", "index": 0}
                    ]]
                }
            },
            "version": 1
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
        
        # Clean any remaining HTML entities in the workflow
        workflow_json_str = json.dumps(workflow)
        workflow_json_str = html.unescape(workflow_json_str)
        workflow = json.loads(workflow_json_str)
        
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