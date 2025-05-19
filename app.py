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
                automation = {
                    'title': title,
                    'description': description,
                    'download_url': download_url,
                    'readme_url': readme_url,
                    'author': 'James Utley PhD',
                    'categories': categories
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
        existing_dirs = [d for d in os.listdir(base_path) if os.path.isdir(os.path.join(base_path, d))]
        highest_num = 0
        for dir_name in existing_dirs:
            match = re.match(r'^(\d+)', dir_name)
            if match:
                num = int(match.group(1))
                highest_num = max(highest_num, num)
        
        new_num = highest_num + 1
        dir_name = f"{new_num}-{goal[:30].lower().replace(' ', '-')}"
        
        # Save the workflow
        workflow_path = workflow_builder.save_workflow(result["workflow"], dir_name)
        
        return jsonify({
            "success": True, 
            "message": "Workflow generated successfully", 
            "workflow": result["workflow"],
            "path": dir_name
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

# TODO: Add download route, meme animation, and user upload logic

if __name__ == '__main__':
    app.run(debug=True) 