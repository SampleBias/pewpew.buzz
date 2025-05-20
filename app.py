import os
from flask import Flask, render_template, redirect, url_for, session, request, send_file, jsonify
from authlib.integrations.flask_client import OAuth
from dotenv import load_dotenv
from supabase import create_client, Client
import glob
import markdown
import json
import re
import asyncio
from workflow_builder import N8nWorkflowBuilder
from werkzeug.utils import secure_filename
import uuid
import base64
import io
from PIL import Image
import google.generativeai as genai

load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_SECRET_KEY', 'supersecret')

# Auth0 config
app.config['AUTH0_CLIENT_ID'] = os.environ.get('AUTH0_CLIENT_ID')
app.config['AUTH0_CLIENT_SECRET'] = os.environ.get('AUTH0_CLIENT_SECRET')
app.config['AUTH0_DOMAIN'] = os.environ.get('AUTH0_DOMAIN')
app.config['AUTH0_CALLBACK_URL'] = os.environ.get('AUTH0_CALLBACK_URL')

# Supabase config
SUPABASE_URL = os.environ.get('SUPABASE_URL')
SUPABASE_KEY = os.environ.get('SUPABASE_KEY')
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

oauth = OAuth(app)
auth0 = oauth.register(
    'auth0',
    client_id=app.config['AUTH0_CLIENT_ID'],
    client_secret=app.config['AUTH0_CLIENT_SECRET'],
    api_base_url=f'https://{app.config["AUTH0_DOMAIN"]}',
    access_token_url=f'https://{app.config["AUTH0_DOMAIN"]}/oauth/token',
    authorize_url=f'https://{app.config["AUTH0_DOMAIN"]}/authorize',
    client_kwargs={
        'scope': 'openid profile email',
    },
)

DEFAULT_CATEGORY = 'Uncategorized'
COMMON_CATEGORIES = [
    'AI', 'Analytics', 'Marketing', 'Data Management', 'Email', 'Content Creation', 'Customer Support',
    'Dev Ops', 'Ecommerce', 'Education', 'Engineering', 'Finance', 'HR', 'IT', 'Project Management',
    'Social Media', 'Webhooks', DEFAULT_CATEGORY
]

workflow_builder = N8nWorkflowBuilder()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    automations = []
    categories_count = {}
    base_path = os.path.join(os.path.dirname(__file__), 'automation')
    selected_category = request.args.get('category')
    search_query = request.args.get('search', '').lower()
    
    # Fetch all workflow ratings at once for efficiency
    ratings_data = {}
    try:
        ratings_response = supabase.table('workflow_ratings').select('workflow_id, upvotes, downvotes').execute()
        if ratings_response.data:
            for rating in ratings_response.data:
                ratings_data[rating['workflow_id']] = {
                    'upvotes': rating['upvotes'], 
                    'downvotes': rating['downvotes']
                }
    except Exception as e:
        print(f"Error fetching ratings: {str(e)}")
    
    # Get all folders and try to sort them numerically if possible
    folders = os.listdir(base_path)
    try:
        # Extract numeric part from folder names (handles both '3-name' and '2653' formats)
        def extract_numeric(folder_name):
            match = re.match(r'^(\d+)', folder_name)
            return int(match.group(1)) if match else float('inf')
            
        # Sort folders in ascending order (smallest to largest)
        folders = sorted(folders, key=extract_numeric)
    except (ValueError, TypeError):
        # Fall back to normal sorting if conversion fails
        folders = sorted(folders)
        
    for folder in folders:
        folder_path = os.path.join(base_path, folder)
        if os.path.isdir(folder_path):
            readme_path = os.path.join(folder_path, 'README.md')
            meta_path = os.path.join(folder_path, 'meta.json')
            workflow_path = os.path.join(folder_path, 'workflow.json')
            categories = []
            # 1. Try meta.json
            if os.path.exists(meta_path):
                with open(meta_path, 'r') as mf:
                    meta = json.load(mf)
                    categories = meta.get('categories', [])
            # 2. Try README.md 'Categories:' line
            elif os.path.exists(readme_path):
                with open(readme_path, 'r') as f:
                    lines = f.readlines()
                    for line in lines:
                        if line.lower().startswith('categories:'):
                            categories = [c.strip() for c in line.split(':', 1)[1].split(',')]
                            break
            # 3. If still no category, try to infer from README content
            if not categories and os.path.exists(readme_path):
                with open(readme_path, 'r') as f:
                    readme_content = f.read().lower()
                    found = False
                    for cat in COMMON_CATEGORIES:
                        if cat.lower() in readme_content:
                            categories = [cat]
                            found = True
                            break
                    if not found:
                        categories = [DEFAULT_CATEGORY]
            elif not categories:
                categories = [DEFAULT_CATEGORY]
            if os.path.exists(readme_path) and os.path.exists(workflow_path):
                with open(readme_path, 'r') as f:
                    lines = f.readlines()
                    title = lines[0].replace('#', '').strip() if lines else folder
                    description = next((l.strip() for l in lines[1:] if l.strip() and not l.startswith('#')), '')
                download_url = f'/download_workflow/{folder}'
                readme_url = f'/readme/{folder}'
                
                # Get ratings data for this workflow, defaults to 0 if not rated
                rating = ratings_data.get(folder, {'upvotes': 0, 'downvotes': 0})
                
                automation = {
                    'id': folder,
                    'title': title,
                    'description': description,
                    'download_url': download_url,
                    'readme_url': readme_url,
                    'author': 'James Utley PhD',
                    'categories': categories,
                    'upvotes': rating['upvotes'],
                    'downvotes': rating['downvotes']
                }
                # Filter by category
                if selected_category and selected_category not in categories:
                    continue
                # Filter by search
                if search_query and (search_query not in title.lower() and search_query not in description.lower()):
                    continue
                automations.append(automation)
                for cat in categories:
                    categories_count[cat] = categories_count.get(cat, 0) + 1
    categories_list = [(cat, categories_count.get(cat, 0)) for cat in COMMON_CATEGORIES if categories_count.get(cat, 0) > 0]
    
    # Ensure Uncategorized is always in the list
    if DEFAULT_CATEGORY not in [cat for cat, _ in categories_list]:
        categories_list.append((DEFAULT_CATEGORY, 0))
        
    categories_list = sorted(categories_list, key=lambda x: (-x[1], x[0]))
    return render_template('dashboard.html', automations=automations, categories=categories_list, selected_category=selected_category, search_query=search_query)

@app.route('/download_workflow/<workflow_folder>')
def download_workflow(workflow_folder):
    base_path = os.path.join(os.path.dirname(__file__), 'automation')
    workflow_path = os.path.join(base_path, workflow_folder, 'workflow.json')
    if os.path.exists(workflow_path):
        return send_file(workflow_path, as_attachment=True)
    return 'Workflow not found', 404

@app.route('/add', methods=['GET', 'POST'])
def add_automation():
    if request.method == 'POST':
        # Handle file upload and metadata
        # TODO: Save to Supabase
        pass
    return render_template('add_automation.html')

@app.route('/howto')
def howto():
    return render_template('howto.html')

@app.route('/login')
def login():
    return auth0.authorize_redirect(redirect_uri=app.config['AUTH0_CALLBACK_URL'])

@app.route('/callback')
def callback():
    token = auth0.authorize_access_token()
    session['user'] = token['userinfo']
    return redirect('/dashboard')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(
        f'https://{app.config["AUTH0_DOMAIN"]}/v2/logout?returnTo={url_for("index", _external=True)}&client_id={app.config["AUTH0_CLIENT_ID"]}'
    )

@app.route('/readme/<workflow_folder>')
def readme(workflow_folder):
    base_path = os.path.join(os.path.dirname(__file__), 'automation')
    readme_path = os.path.join(base_path, workflow_folder, 'README.md')
    if os.path.exists(readme_path):
        with open(readme_path, 'r') as f:
            content = f.read()
        return content, 200, {'Content-Type': 'text/plain; charset=utf-8'}
    return 'README not found', 404

@app.route('/builder', methods=['GET'])
def workflow_builder_page():
    return render_template('workflow_builder.html')

@app.route('/api/generate-workflow', methods=['POST'])
def generate_workflow():
    data = request.json
    goal = data.get('goal', '')
    publish_to_gallery = data.get('publish_to_gallery', False)
    
    if not goal:
        return jsonify({"success": False, "error": "No workflow goal provided"}), 400
    
    # Generate the workflow using asyncio to handle the async call
    result = asyncio.run(workflow_builder.generate_workflow(goal))
    
    if not result["success"]:
        return jsonify(result), 400
    
    # Create a directory name for the workflow
    # Find the highest number and increment by 1
    base_path = os.path.join(os.path.dirname(__file__), 'automation')
    try:
        # Ensure automation directory exists
        os.makedirs(base_path, exist_ok=True)
        
        existing_dirs = [d for d in os.listdir(base_path) if os.path.isdir(os.path.join(base_path, d))]
        highest_num = 0
        for dir_name in existing_dirs:
            match = re.match(r'^(\d+)', dir_name)
            if match:
                num = int(match.group(1))
                highest_num = max(highest_num, num)
        
        new_num = highest_num + 1
        dir_name = f"{new_num}-{goal[:30].lower().replace(' ', '-').replace('/', '-')}"
        
        # Save the workflow
        workflow_path = workflow_builder.save_workflow(result["workflow"], dir_name)
        
        # Generate README content
        readme_content = workflow_builder.generate_readme(result["workflow"], goal, dir_name)
        
        # Create a meta.json file that indicates whether the workflow is published
        meta_path = os.path.join(base_path, dir_name, 'meta.json')
        meta_data = {
            "categories": ["AI", "Engineering"],  # Default categories
            "generated": True,
            "summary": f"Automated workflow for: {goal[:100]}",
            "published": publish_to_gallery,  # Only set to true if explicitly published
            "published_date": datetime.datetime.now().isoformat() if publish_to_gallery else None,
            "published_by": session.get('user', {}).get('email', 'anonymous') if publish_to_gallery else None
        }
        
        with open(meta_path, 'w') as f:
            json.dump(meta_data, f, indent=2)
        
        response_data = {
            "success": True, 
            "message": "Workflow generated successfully", 
            "workflow": result["workflow"],
            "path": dir_name,
            "readme": readme_content
        }
        
        # Add warning if present in the result
        if "warning" in result:
            response_data["warning"] = result["warning"]
            
        return jsonify(response_data)
    except Exception as e:
        print(f"Error saving workflow: {str(e)}")
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/workflow-readme/<workflow_folder>', methods=['GET'])
def get_workflow_readme(workflow_folder):
    """Get README content for a workflow"""
    base_path = os.path.join(os.path.dirname(__file__), 'automation')
    readme_path = os.path.join(base_path, workflow_folder, 'README.md')
    
    if os.path.exists(readme_path):
        with open(readme_path, 'r') as f:
            content = f.read()
        return jsonify({"success": True, "readme": content})
    
    return jsonify({"success": False, "error": "README not found"}), 404

@app.route('/api/test-gemini', methods=['GET'])
def test_gemini_api():
    """Test endpoint to verify Gemini API connection"""
    try:
        # Run the async function in a synchronous context
        result = asyncio.run(workflow_builder.test_api_connection())
        return jsonify(result)
    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"Error testing API: {str(e)}",
            "error_type": str(type(e))
        })

# Workflow feedback system routes
@app.route('/api/workflow/rating/<workflow_folder>', methods=['GET'])
def get_workflow_rating(workflow_folder):
    """Get the current rating for a workflow"""
    try:
        # Get the current rating from Supabase
        response = supabase.table('workflow_ratings').select('upvotes, downvotes').eq('workflow_id', workflow_folder).execute()
        
        # If the workflow doesn't have any ratings yet, return zeros
        if not response.data:
            return jsonify({
                "success": True,
                "upvotes": 0,
                "downvotes": 0
            })
        
        # Return the current upvotes and downvotes
        return jsonify({
            "success": True,
            "upvotes": response.data[0]['upvotes'],
            "downvotes": response.data[0]['downvotes']
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"Error getting rating: {str(e)}"
        }), 500

@app.route('/api/publish-workflow', methods=['POST'])
def publish_workflow():
    """Add a workflow to the public gallery"""
    try:
        data = request.json
        workflow_path = data.get('workflow_path', '')
        categories = data.get('categories', [])
        
        if not workflow_path:
            return jsonify({
                "success": False,
                "error": "No workflow path provided"
            }), 400
            
        if not categories:
            return jsonify({
                "success": False,
                "error": "No categories provided"
            }), 400
            
        # Limit to 3 categories max
        if len(categories) > 3:
            categories = categories[:3]
            
        # Validate that the workflow exists
        base_path = os.path.join(os.path.dirname(__file__), 'automation')
        full_path = os.path.join(base_path, workflow_path)
        
        if not os.path.isdir(full_path):
            return jsonify({
                "success": False,
                "error": "Workflow folder not found"
            }), 404
            
        workflow_json_path = os.path.join(full_path, 'workflow.json')
        readme_path = os.path.join(full_path, 'README.md')
        
        if not os.path.exists(workflow_json_path) or not os.path.exists(readme_path):
            return jsonify({
                "success": False,
                "error": "Workflow files not found"
            }), 404
            
        # Update the meta.json file with publication info
        meta_path = os.path.join(full_path, 'meta.json')
        
        # Create or update meta.json
        meta_data = {
            "categories": categories,
            "published": True,
            "published_date": datetime.datetime.now().isoformat(),
            "published_by": session.get('user', {}).get('email', 'anonymous')
        }
        
        # If meta.json already exists, read and update it
        if os.path.exists(meta_path):
            with open(meta_path, 'r') as f:
                existing_meta = json.load(f)
                # Merge the existing meta with the new publication data
                meta_data = {**existing_meta, **meta_data}
        
        # Write the updated meta.json
        with open(meta_path, 'w') as f:
            json.dump(meta_data, f, indent=2)
            
        # Update README with categories if they don't exist
        with open(readme_path, 'r') as f:
            readme_content = f.read()
            
        # Check if Categories line exists
        if 'Categories:' not in readme_content:
            # Add categories line after title
            lines = readme_content.split('\n')
            title_index = -1
            
            for i, line in enumerate(lines):
                if line.startswith('# '):
                    title_index = i
                    break
                    
            if title_index >= 0:
                categories_line = f"Categories: {', '.join(categories)}"
                lines.insert(title_index + 1, categories_line)
                
                # Write updated README
                with open(readme_path, 'w') as f:
                    f.write('\n'.join(lines))
        
        return jsonify({
            "success": True,
            "message": "Workflow published to gallery"
        })
            
    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"Error publishing workflow: {str(e)}"
        }), 500

@app.route('/api/workflow/rating/<workflow_folder>', methods=['POST'])
def rate_workflow(workflow_folder):
    """Rate a workflow with upvote or downvote"""
    try:
        data = request.json
        vote_type = data.get('vote_type')
        
        if vote_type not in ['upvote', 'downvote']:
            return jsonify({
                "success": False,
                "error": "Invalid vote type. Must be 'upvote' or 'downvote'."
            }), 400
        
        # Get the current rating
        response = supabase.table('workflow_ratings').select('*').eq('workflow_id', workflow_folder).execute()
        
        # If the workflow doesn't have any ratings yet, create a new record
        if not response.data:
            upvotes = 1 if vote_type == 'upvote' else 0
            downvotes = 1 if vote_type == 'downvote' else 0
            
            supabase.table('workflow_ratings').insert({
                'workflow_id': workflow_folder,
                'upvotes': upvotes,
                'downvotes': downvotes
            }).execute()
        else:
            # Update the existing record
            rating_id = response.data[0]['id']
            current_upvotes = response.data[0]['upvotes']
            current_downvotes = response.data[0]['downvotes']
            
            if vote_type == 'upvote':
                supabase.table('workflow_ratings').update({
                    'upvotes': current_upvotes + 1
                }).eq('id', rating_id).execute()
            else:
                supabase.table('workflow_ratings').update({
                    'downvotes': current_downvotes + 1
                }).eq('id', rating_id).execute()
        
        # Get the updated rating
        updated = supabase.table('workflow_ratings').select('upvotes, downvotes').eq('workflow_id', workflow_folder).execute()
        
        return jsonify({
            "success": True,
            "upvotes": updated.data[0]['upvotes'],
            "downvotes": updated.data[0]['downvotes']
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"Error rating workflow: {str(e)}"
        }), 500

@app.route('/api/extract-workflow-from-image', methods=['POST'])
def extract_workflow_from_image():
    """Extract an n8n workflow configuration from an uploaded screenshot"""
    try:
        # Check if file is in the request
        if 'screenshot' not in request.files:
            return jsonify({
                "success": False,
                "error": "No screenshot provided",
                "error_type": "missing_file"
            }), 400
            
        screenshot_file = request.files['screenshot']
        
        # Check if filename is empty
        if screenshot_file.filename == '':
            return jsonify({
                "success": False,
                "error": "No screenshot selected",
                "error_type": "empty_filename"
            }), 400
            
        # Check file extension
        allowed_extensions = {'png', 'jpg', 'jpeg'}
        if not ('.' in screenshot_file.filename and \
                screenshot_file.filename.rsplit('.', 1)[1].lower() in allowed_extensions):
            return jsonify({
                "success": False,
                "error": "Invalid file type. Only PNG, JPG, and JPEG are allowed.",
                "error_type": "invalid_file_type"
            }), 400
            
        # Read the image file
        img = Image.open(screenshot_file)
        
        # Convert the image to RGB mode if it's not already
        if img.mode != 'RGB':
            img = img.convert('RGB')
            
        # Save image to buffer
        img_byte_arr = io.BytesIO()
        img.save(img_byte_arr, format='JPEG')
        img_byte_arr.seek(0)
        
        # Convert to base64 for Gemini
        encoded_img = base64.b64encode(img_byte_arr.getvalue()).decode('ascii')
        mime_type = "image/jpeg"
        
        # Configure Gemini model for image analysis
        if GEMINI_API_KEY:
            genai.configure(api_key=GEMINI_API_KEY)
        else:
            return jsonify({
                "success": False,
                "error": "GEMINI_API_KEY not configured. Unable to process image.",
                "error_type": "api_key_missing"
            }), 500
        
        # Use Gemini Pro Vision to analyze the image
        model = genai.GenerativeModel('gemini-pro-vision')
        
        # First, check if this is actually an n8n workflow
        validation_prompt = [
            "Analyze this image and determine if it contains an n8n workflow diagram.",
            "An n8n workflow typically has connected nodes with labels for different operations.",
            "Respond with ONLY 'YES' if it's an n8n workflow or 'NO' if it's not.",
            {"mime_type": mime_type, "data": encoded_img}
        ]
        
        validation_response = model.generate_content(validation_prompt)
        validation_text = validation_response.text.strip().upper()
        
        if validation_text != "YES":
            return jsonify({
                "success": False,
                "error": "The uploaded image does not appear to be an n8n workflow.",
                "error_type": "not_workflow"
            }), 400
        
        # Extract workflow information
        extraction_prompt = [
            "You are an expert in extracting n8n workflow configurations from screenshots.",
            "Analyze this screenshot of an n8n workflow and create a valid JSON workflow that matches it.",
            "Include all nodes visible in the workflow with their names, types, positions, and connections.",
            "For each node, identify the type (e.g., 'HTTP Request', 'Set', 'Function', etc.), position, and connections to other nodes.",
            "Follow the exact n8n format for workflow JSON:",
            "{\n  \"name\": \"Extracted Workflow\",\n  \"nodes\": [\n    {\"id\": \"1\", \"name\": \"Start\", \"type\": \"n8n-nodes-base.start\", \"position\": [x, y], ...},\n    ...\n  ],\n  \"connections\": {\"Node1\": {\"main\": [[{\"node\": \"Node2\", \"type\": \"main\", \"index\": 0}]]}}\n}",
            "Respond with ONLY the valid JSON. No explanations or markdown formatting.",
            {"mime_type": mime_type, "data": encoded_img}
        ]
        
        extraction_response = model.generate_content(extraction_prompt)
        extraction_text = extraction_response.text.strip()
        
        # Try to extract JSON from the response
        try:
            # Remove any markdown code blocks
            extraction_text = re.sub(r'^```(?:json)?\s*', '', extraction_text)
            extraction_text = re.sub(r'\s*```$', '', extraction_text)
            
            # Find JSON object in the text
            start_idx = extraction_text.find('{')
            end_idx = extraction_text.rfind('}')
            
            if start_idx >= 0 and end_idx >= 0 and start_idx < end_idx:
                extraction_text = extraction_text[start_idx:end_idx+1]
                
                # Parse the JSON
                workflow_json = json.loads(extraction_text)
                
                # Make sure the workflow has a proper name
                if "name" not in workflow_json or not workflow_json["name"]:
                    workflow_json["name"] = "Extracted from Screenshot"
                    
                # Create a directory name for the workflow
                base_path = os.path.join(os.path.dirname(__file__), 'automation')
                
                # Ensure automation directory exists
                os.makedirs(base_path, exist_ok=True)
                
                # Generate a unique ID for this extraction
                existing_dirs = [d for d in os.listdir(base_path) if os.path.isdir(os.path.join(base_path, d))]
                highest_num = 0
                for dir_name in existing_dirs:
                    match = re.match(r'^(\d+)', dir_name)
                    if match:
                        num = int(match.group(1))
                        highest_num = max(highest_num, num)
                
                new_num = highest_num + 1
                dir_name = f"{new_num}-extracted-workflow-{uuid.uuid4().hex[:8]}"
                
                # Generate an informative README
                workflow_name = workflow_json.get('name', 'Extracted Workflow')
                readme_content = f"# {workflow_name}\n\n"
                readme_content += f"Categories: AI, Extracted\n\n"
                readme_content += f"This workflow was extracted from a screenshot using AI recognition.\n\n"
                
                # Count nodes by type
                node_types = {}
                for node in workflow_json.get('nodes', []):
                    node_type = node.get('type', '').replace('n8n-nodes-base.', '')
                    if node_type not in node_types:
                        node_types[node_type] = []
                    node_types[node_type].append(node.get('name', node_type))
                
                if node_types:
                    readme_content += "## Technical Details\n\n"
                    readme_content += "This workflow uses the following node types:\n\n"
                    for node_type, nodes in node_types.items():
                        node_names = ", ".join(nodes)
                        readme_content += f"- {node_type}: {node_names}\n"
                    readme_content += "\n"
                
                # Add import instructions
                readme_content += "## Usage\n\n"
                readme_content += "1. Download the workflow JSON file\n"
                readme_content += "2. Import it into your n8n instance\n"
                readme_content += "3. Review and adjust the workflow as needed\n"
                readme_content += "4. Activate and test the workflow\n\n"
                
                # Add a note about extraction
                readme_content += "## Note\n\n"
                readme_content += "This workflow was automatically extracted from a screenshot. Some configuration details might need manual adjustment.\n"
                
                # Save the files
                folder_path = os.path.join(base_path, dir_name)
                os.makedirs(folder_path, exist_ok=True)
                
                # Save workflow.json
                workflow_path = os.path.join(folder_path, 'workflow.json')
                with open(workflow_path, 'w') as f:
                    json.dump(workflow_json, f, indent=2)
                
                # Save README.md
                readme_path = os.path.join(folder_path, 'README.md')
                with open(readme_path, 'w') as f:
                    f.write(readme_content)
                
                # Save meta.json
                meta_path = os.path.join(folder_path, 'meta.json')
                meta_data = {
                    "categories": ["AI", "Extracted"],
                    "generated": False,
                    "extracted": True,
                    "extraction_date": datetime.datetime.now().isoformat(),
                    "summary": "Workflow extracted from screenshot",
                    "published": False
                }
                
                with open(meta_path, 'w') as f:
                    json.dump(meta_data, f, indent=2)
                
                return jsonify({
                    "success": True,
                    "message": "Workflow successfully extracted from image",
                    "workflow": workflow_json,
                    "path": dir_name,
                    "readme": readme_content
                })
            else:
                return jsonify({
                    "success": False,
                    "error": "Could not extract valid workflow JSON from the image",
                    "error_type": "extraction_failed"
                }), 400
        except json.JSONDecodeError as e:
            return jsonify({
                "success": False,
                "error": f"Invalid JSON format: {str(e)}",
                "error_type": "invalid_json"
            }), 400
        except Exception as e:
            return jsonify({
                "success": False,
                "error": f"Error processing workflow: {str(e)}",
                "error_type": "processing_error"
            }), 500
    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"Error processing image: {str(e)}",
            "error_type": "general_error"
        }), 500

# TODO: Add download route, meme animation, and user upload logic

if __name__ == '__main__':
    app.run(debug=True) 