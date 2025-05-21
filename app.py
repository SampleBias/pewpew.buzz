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
import datetime
import shutil
from workflow_builder import N8nWorkflowBuilder
from werkzeug.utils import secure_filename
import uuid
import base64
import io
from PIL import Image
import google.generativeai as genai
# Import the workflow sync function for immediate synchronization
from workflow_sync import get_workflow_from_filesystem, sync_workflow_to_database, get_supabase_client
from functools import wraps
import traceback

load_dotenv()

# Get API keys from environment
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')

# Create automation directory if it doesn't exist
automation_dir = os.path.join(os.path.dirname(__file__), 'automation')
os.makedirs(automation_dir, exist_ok=True)
print(f"Automation directory path: {automation_dir}")
if os.path.exists(automation_dir):
    print(f"Automation directory exists and contains {len(os.listdir(automation_dir))} items")
else:
    print("Warning: Automation directory does not exist!")

# Authentication decorator
def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user' not in session:
            # Save the URL the user was trying to access
            session['next_url'] = request.url
            # Redirect to login
            return redirect('/login')
        return f(*args, **kwargs)
    return decorated

# Admin auth decorator
def requires_admin(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get('admin_authenticated'):
            # Redirect to admin login
            return redirect('/admin')
        return f(*args, **kwargs)
    return decorated

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
SUPABASE_SECRET_KEY = os.environ.get('SUPABASE_SECRET_KEY')

# Use service role key if available, otherwise use anon key
supabase_key_to_use = SUPABASE_SECRET_KEY if SUPABASE_SECRET_KEY else SUPABASE_KEY
supabase: Client = create_client(SUPABASE_URL, supabase_key_to_use)

if SUPABASE_SECRET_KEY:
    print("Using service role key for Supabase connection in app.py")
else:
    print("Using anon key for Supabase connection in app.py")

# Create the workflow_ratings table if it doesn't exist
try:
    # Check if the workflow_ratings table exists by making a small query
    supabase.table('workflow_ratings').select('id').limit(1).execute()
    print("workflow_ratings table exists")
except Exception as e:
    if '42P01' in str(e):  # Table does not exist error code
        print("workflow_ratings table doesn't exist. Please create it manually with the following SQL:")
        with open('create_workflow_ratings_table.sql', 'r') as f:
            sql = f.read()
            print(sql)
            
        # Instead of trying to execute SQL directly, we'll initialize with empty ratings
        # for each workflow to prevent errors when users interact with the site
        base_path = os.path.join(os.path.dirname(__file__), 'automation')
        if os.path.exists(base_path):
            print("Pre-initializing ratings for existing workflows...")
            try:
                existing_dirs = [d for d in os.listdir(base_path) if os.path.isdir(os.path.join(base_path, d))]
                for workflow_folder in existing_dirs:
                    if os.path.exists(os.path.join(base_path, workflow_folder, 'workflow.json')):
                        print(f"Found workflow: {workflow_folder}")
            except Exception as dir_error:
                print(f"Error scanning automation directory: {str(dir_error)}")
    else:
        print(f"Warning: Error checking workflow_ratings table: {str(e)}")

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
        'response_type': 'code',
    },
    server_metadata_url=f'https://{app.config["AUTH0_DOMAIN"]}/.well-known/openid-configuration'
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
    selected_category = request.args.get('category')
    search_query = request.args.get('search', '').lower()
    
    # Start by loading automations from the filesystem
    base_path = os.path.join(os.path.dirname(__file__), 'automation')
    
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
        # Continue without ratings rather than failing completely
    
    # Get all folders and try to sort them numerically if possible
    print(f"Looking in filesystem path: {base_path}")
    try:
        folders = os.listdir(base_path)
        print(f"Found {len(folders)} folders in automation directory")
    except Exception as e:
        print(f"Error accessing automation directory: {str(e)}")
        folders = []
    
    filesystem_automations = []
    max_folder_id = 0
    
    try:
        # Extract numeric part from folder names (handles both '3-name' and '2653' formats)
        def extract_numeric(folder_name):
            match = re.match(r'^(\d+)', folder_name)
            return int(match.group(1)) if match else float('inf')
            
        # Sort folders in ascending order (smallest to largest)
        folders = sorted(folders, key=extract_numeric)
        
        # Find the maximum numeric ID in the filesystem
        for folder in folders:
            folder_num = extract_numeric(folder)
            if folder_num != float('inf') and folder_num > max_folder_id:
                max_folder_id = folder_num
    except (ValueError, TypeError) as e:
        print(f"Error sorting folders: {str(e)}")
        # Fall back to normal sorting if conversion fails
        folders = sorted(folders)
        
    # Process each folder to extract workflow information
    for folder in folders:
        folder_path = os.path.join(base_path, folder)
        
        if not os.path.isdir(folder_path):
            continue
            
        try:
            readme_path = os.path.join(folder_path, 'README.md')
            meta_path = os.path.join(folder_path, 'meta.json')
            workflow_path = os.path.join(folder_path, 'workflow.json')
            
            # Skip if essential files are missing
            if not os.path.exists(workflow_path):
                print(f"Skipping {folder}: Missing workflow.json")
                continue
                
            categories = []
            author = 'James Utley PhD'  # Default author
            
            # 1. Try meta.json for categories and author
            if os.path.exists(meta_path):
                try:
                    with open(meta_path, 'r') as mf:
                        meta = json.load(mf)
                        categories = meta.get('categories', [])
                        author = meta.get('author', author)
                except Exception as e:
                    print(f"Error reading meta.json for {folder}: {str(e)}")
            
            # 2. Try README.md 'Categories:' line if no categories yet
            if not categories and os.path.exists(readme_path):
                try:
                    with open(readme_path, 'r') as f:
                        lines = f.readlines()
                        for line in lines:
                            if line.lower().startswith('categories:'):
                                categories = [c.strip() for c in line.split(':', 1)[1].split(',')]
                                break
                except Exception as e:
                    print(f"Error reading README.md for categories in {folder}: {str(e)}")
            
            # 3. If still no category, try to infer from README content
            if not categories and os.path.exists(readme_path):
                try:
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
                except Exception as e:
                    print(f"Error inferring categories from README.md in {folder}: {str(e)}")
                    categories = [DEFAULT_CATEGORY]
            elif not categories:
                categories = [DEFAULT_CATEGORY]
            
            # Extract title and description from README if it exists
            title = folder
            description = ""
            if os.path.exists(readme_path):
                try:
                    with open(readme_path, 'r') as f:
                        lines = f.readlines()
                        if lines:
                            # First line is typically the title (with # prefix)
                            title = lines[0].replace('#', '').strip() if lines else folder
                            # Next non-empty, non-header line is the description
                            description = next((l.strip() for l in lines[1:] if l.strip() and not l.startswith('#')), '')
                except Exception as e:
                    print(f"Error reading README.md for title/description in {folder}: {str(e)}")
                    # Fallback to folder name based title
                    if '-' in folder:
                        title_part = folder.split('-', 1)[1]
                        title = title_part.replace('-', ' ').title()
            
            # Create download and readme URLs
            download_url = f'/download_workflow/{folder}'
            readme_url = f'/readme/{folder}'
            
            # Get ratings data for this workflow, defaults to 0 if not rated
            rating = ratings_data.get(folder, {'upvotes': 0, 'downvotes': 0})
            
            # Create the automation entry
            automation = {
                'id': folder,
                'title': title,
                'description': description,
                'download_url': download_url,
                'readme_url': readme_url,
                'author': author,
                'categories': categories,
                'upvotes': rating['upvotes'] or 0,  # Ensure we have 0 instead of None
                'downvotes': rating['downvotes'] or 0  # Ensure we have 0 instead of None
            }
            
            # Store the workflow in our list
            filesystem_automations.append(automation)
            
            # Update category counts for sidebar
            for cat in categories:
                categories_count[cat] = categories_count.get(cat, 0) + 1
                
        except Exception as e:
            print(f"Error processing folder {folder}: {str(e)}")
            continue
    
    print(f"Loaded {len(filesystem_automations)} workflows from filesystem")
    
    # Now try to fetch additional (newer) entries from the database
    try:
        print(f"Looking for workflows with ID greater than {max_folder_id}")
        # Only fetch workflows with ID greater than the max we found in the filesystem
        workflows_query = supabase.table('workflows').select(
            'id, slug, title, description, author_name, is_generated, is_submitted, is_extracted, published_date, published'
        ).eq('published', True)
        
        # Add numeric ID comparison - only fetch newer entries
        if max_folder_id > 0:
            # Try to get workflow IDs that are greater than our max filesystem ID
            workflows_query = workflows_query.gte('id', str(max_folder_id + 1))
            
        # Execute the query
        workflows_response = workflows_query.execute()
        
        if workflows_response.data:
            print(f"Found {len(workflows_response.data)} additional workflows in database")
            
            # Get all categories for newer workflows
            workflow_ids = [workflow['id'] for workflow in workflows_response.data]
            wf_categories_query = supabase.table('workflow_categories') \
                .select('category, workflow_id') \
                .in_('workflow_id', workflow_ids) \
                .execute()
            
            # Group categories by workflow ID
            workflow_categories = {}
            if wf_categories_query.data:
                for cat_item in wf_categories_query.data:
                    workflow_id = cat_item['workflow_id']
                    cat = cat_item['category']
                    if workflow_id not in workflow_categories:
                        workflow_categories[workflow_id] = []
                    workflow_categories[workflow_id].append(cat)
                    categories_count[cat] = categories_count.get(cat, 0) + 1
            
            # Process workflows from database
            for workflow in workflows_response.data:
                slug = workflow['slug']
                
                # Skip if we already have this workflow from filesystem
                if any(a['id'] == slug for a in filesystem_automations):
                    continue
                
                # Get categories for this workflow
                categories = workflow_categories.get(workflow['id'], [DEFAULT_CATEGORY])
                
                # Get ratings data for this workflow
                rating = ratings_data.get(slug, {'upvotes': 0, 'downvotes': 0})
                
                automation = {
                    'id': slug,
                    'title': workflow['title'],
                    'description': workflow['description'],
                    'download_url': f'/download_workflow/{slug}',
                    'readme_url': f'/readme/{slug}',
                    'author': workflow['author_name'],
                    'categories': categories,
                    'upvotes': rating['upvotes'] or 0,
                    'downvotes': rating['downvotes'] or 0
                }
                
                filesystem_automations.append(automation)
        
    except Exception as e:
        print(f"Error loading additional workflows from database: {str(e)}")
        # Continue with just filesystem automations
    
    # Apply filtering to automations
    automations = []
    for automation in filesystem_automations:
        # Apply category filter if specified
        if selected_category and selected_category not in automation['categories']:
            continue
            
        # Apply search filter if specified
        if search_query and search_query not in automation['title'].lower() and search_query not in automation['description'].lower():
            continue
            
        automations.append(automation)
    
    print(f"Final count after filtering: {len(automations)} workflows")
    
    # Sort workflows by the numeric part of the slug (to maintain the same order as before)
    def extract_numeric(automation):
        match = re.match(r'^(\d+)', automation['id'])
        return int(match.group(1)) if match else float('inf')
        
    automations = sorted(automations, key=extract_numeric)
    
    # Create the categories list for the sidebar
    categories_list = [(cat, categories_count.get(cat, 0)) for cat in COMMON_CATEGORIES if categories_count.get(cat, 0) > 0]
    
    # Ensure Uncategorized is always in the list
    if DEFAULT_CATEGORY not in [cat for cat, _ in categories_list]:
        categories_list.append((DEFAULT_CATEGORY, 0))
        
    categories_list = sorted(categories_list, key=lambda x: (-x[1], x[0]))
    
    return render_template('dashboard.html', 
        automations=automations, 
        categories=categories_list, 
        selected_category=selected_category,
        search_query=search_query)

@app.route('/download_workflow/<workflow_folder>')
def download_workflow(workflow_folder):
    """Download a workflow JSON file"""
    try:
        # Sanitize the workflow_folder to prevent path traversal attacks
        workflow_folder = secure_filename(workflow_folder)
        
        # Always try filesystem first for better performance
        base_path = os.path.join(os.path.dirname(__file__), 'automation')
        workflow_path = os.path.join(base_path, workflow_folder, 'workflow.json')
        
        if os.path.exists(workflow_path):
            try:
                print(f"Serving workflow from filesystem: {workflow_folder}")
                return send_file(workflow_path, 
                                 as_attachment=True, 
                                 download_name=f"{workflow_folder}.json",
                                 mimetype='application/json')
            except Exception as file_error:
                print(f"Error sending workflow file: {str(file_error)}")
                return jsonify({
                    "success": False,
                    "error": f"Error sending workflow file: {str(file_error)}"
                }), 500
                
        # Fallback to database if not found in filesystem
        try:
            print(f"Workflow not found in filesystem, checking database: {workflow_folder}")
            # Try to get workflow from database
            workflow_response = supabase.table('workflows') \
                .select('json_content') \
                .eq('slug', workflow_folder) \
                .single() \
                .execute()
            
            if workflow_response.data and 'json_content' in workflow_response.data:
                # Get workflow from database
                workflow_json = workflow_response.data['json_content']
                
                # Update download count
                try:
                    supabase.table('workflows') \
                        .update({'downloads': supabase.table('workflows').select('downloads').eq('slug', workflow_folder).single().execute().data['downloads'] + 1}) \
                        .eq('slug', workflow_folder) \
                        .execute()
                except Exception as update_error:
                    print(f"Error updating download count: {str(update_error)}")
                    # Continue without failing if download count update fails
                    
                # Create a temporary in-memory file
                try:
                    json_str = json.dumps(workflow_json, indent=2)
                    
                    return send_file(
                        io.BytesIO(json_str.encode('utf-8')),
                        mimetype='application/json',
                        as_attachment=True,
                        download_name=f"{workflow_folder}.json"
                    )
                except Exception as json_error:
                    print(f"Error creating workflow JSON download: {str(json_error)}")
                    return jsonify({
                        "success": False,
                        "error": f"Error creating workflow download: {str(json_error)}"
                    }), 500
                
            # If we get here, the workflow was not found in either location
            print(f"Workflow not found in database either: {workflow_folder}")
            return jsonify({
                "success": False,
                "error": "Workflow not found"
            }), 404
        except Exception as db_error:
            print(f"Error fetching workflow from database: {str(db_error)}")
            return jsonify({
                "success": False,
                "error": f"Error retrieving workflow from database: {str(db_error)}"
            }), 500
    except Exception as general_error:
        print(f"Unexpected error in download_workflow: {str(general_error)}")
        traceback.print_exc()
        return jsonify({
            "success": False,
            "error": f"Unexpected error: {str(general_error)}"
        }), 500

@app.route('/add', methods=['GET', 'POST'])
@requires_auth
def add_automation():
    if request.method == 'POST':
        # This is now handled by the API endpoint
        return redirect(url_for('dashboard'))
    return render_template('add_automation.html')

@app.route('/howto')
def howto():
    return render_template('howto.html')

@app.route('/login')
def login():
    return auth0.authorize_redirect(
        redirect_uri=app.config['AUTH0_CALLBACK_URL'],
        audience=f'https://{app.config["AUTH0_DOMAIN"]}/userinfo',
        scope='openid profile email'
    )

@app.route('/callback')
def callback():
    try:
        token = auth0.authorize_access_token()
        session['user'] = token['userinfo']
        
        # If this is a first login, you could add them to your database here
        print(f"User logged in: {session['user'].get('email')}")
        
        # Redirect to profile page on first login, or to the page they were trying to access
        return redirect(session.pop('next_url', '/profile'))
    except Exception as e:
        print(f"Error during Auth0 callback: {str(e)}")
        return redirect('/')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(
        f'https://{app.config["AUTH0_DOMAIN"]}/v2/logout?returnTo={url_for("index", _external=True)}&client_id={app.config["AUTH0_CLIENT_ID"]}'
    )

@app.route('/readme/<workflow_folder>')
def readme(workflow_folder):
    # Always try filesystem first for better performance
    base_path = os.path.join(os.path.dirname(__file__), 'automation')
    readme_path = os.path.join(base_path, workflow_folder, 'README.md')
    
    if os.path.exists(readme_path):
        print(f"Serving README from filesystem: {workflow_folder}")
        try:
            with open(readme_path, 'r') as f:
                content = f.read()
            return content, 200, {'Content-Type': 'text/plain; charset=utf-8'}
        except Exception as e:
            print(f"Error reading README file: {str(e)}")
    
    # Fallback to database if not found in filesystem
    try:
        print(f"README not found in filesystem, checking database: {workflow_folder}")
        
        # Try to get readme from database
        readme_response = supabase.table('workflows') \
            .select('readme_content, title') \
            .eq('slug', workflow_folder) \
            .single() \
            .execute()
        
        if readme_response.data:
            # Get readme from database
            readme_content = readme_response.data['readme_content']
            
            # Update view count
            try:
                supabase.table('workflows') \
                    .update({'views': supabase.table('workflows').select('views').eq('slug', workflow_folder).single().execute().data['views'] + 1}) \
                    .eq('slug', workflow_folder) \
                    .execute()
            except Exception as e:
                print(f"Error updating view count: {str(e)}")
                
            # Return content as markdown
            return readme_content, 200, {'Content-Type': 'text/plain; charset=utf-8'}
            
        # If we get here, the README was not found in either location
        print(f"README not found in database either: {workflow_folder}")
        return 'README not found', 404
    except Exception as e:
        print(f"Error fetching README from database: {str(e)}")
        return 'Error retrieving README', 500

@app.route('/builder', methods=['GET'])
@requires_auth
def workflow_builder_page():
    return render_template('workflow_builder.html')

@app.route('/api/generate-workflow', methods=['POST'])
def generate_workflow():
    """Generate a workflow based on a user-provided goal"""
    try:
        data = request.json
        if not data:
            return jsonify({
                "success": False, 
                "error": "No JSON data received in request"
            }), 400
            
        goal = data.get('goal', '')
        publish_to_gallery = data.get('publish_to_gallery', False)
        
        if not goal:
            return jsonify({
                "success": False, 
                "error": "No workflow goal provided"
            }), 400
        
        try:
            # Generate the workflow using asyncio with a timeout to prevent Heroku H12 errors
            # Heroku has a 30-second timeout, so we set ours to 25 seconds to ensure we respond before that
            try:
                # Set a timeout to prevent Heroku H12 errors (30 second limit)
                result = asyncio.run(asyncio.wait_for(
                    workflow_builder.generate_workflow(goal), 
                    timeout=25.0
                ))
            except asyncio.TimeoutError:
                print(f"Workflow generation timed out for goal: {goal[:50]}...")
                # Return a fallback workflow with timeout message
                fallback_workflow = workflow_builder._create_fallback_workflow(
                    goal, 
                    f"Timeout Workflow for: {goal[:30]}"
                )
                return jsonify({
                    "success": True,
                    "workflow": fallback_workflow,
                    "warning": "The workflow generation timed out. A simple fallback workflow has been created. Please try again with a simpler request.",
                    "message": "Fallback workflow created due to timeout",
                    "error_details": "The request to the Gemini API timed out. This can happen due to high demand or complex workflows."
                })
            
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
                
                try:
                    # Save the workflow with proper JSON handling
                    workflow_path = workflow_builder.save_workflow(result["workflow"], dir_name)
                    
                    # Generate README content
                    readme_content = workflow_builder.generate_readme(result["workflow"], goal, dir_name)
                    
                    # Create a meta.json file that indicates whether the workflow is published
                    meta_path = os.path.join(base_path, dir_name, 'meta.json')
                    meta_data = {
                        "categories": ["AI", "Engineering"],  # Default categories
                        "generated": True,
                        "summary": f"Automated workflow for: {goal[:100]}",
                        "published": publish_to_gallery,
                        "published_date": datetime.datetime.now().isoformat() if publish_to_gallery else None,
                        "published_by": session.get('user', {}).get('email', 'anonymous') if publish_to_gallery else None
                    }
                    
                    with open(meta_path, 'w') as f:
                        json.dump(meta_data, f, indent=2)
                    
                    # Make sure we're handling potential HTML content in the response
                    # Check if the workflow JSON contains any potential HTML by looking for '<' character
                    workflow_json_str = json.dumps(result["workflow"])
                    if '<' in workflow_json_str:
                        print("Warning: Potential HTML content found in workflow JSON, sanitizing")
                        # Additional sanitization for HTML content
                        # This is already handled in workflow_builder.py, but just to be sure
                        workflow_json_str = workflow_json_str.replace('<', '&lt;').replace('>', '&gt;')
                        # Parse it back into a Python object
                        try:
                            sanitized_workflow = json.loads(workflow_json_str)
                            result["workflow"] = sanitized_workflow
                        except json.JSONDecodeError:
                            print("Warning: Couldn't parse sanitized JSON, returning original")
                    
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
                    
                    # Sync the workflow to the database
                    try:
                        def background_sync():
                            try:
                                # Create application context for the thread
                                with app.app_context():
                                    sync_workflow_immediately(dir_name)
                            except Exception as e:
                                print(f"Background sync error: {str(e)}")
                                
                        import threading
                        sync_thread = threading.Thread(target=background_sync)
                        sync_thread.daemon = True
                        sync_thread.start()
                    except Exception as sync_error:
                        print(f"Warning: Failed to start background sync: {str(sync_error)}")
                        # Continue even if sync fails
                    
                    return jsonify(response_data)
                except json.JSONDecodeError as e:
                    error_msg = f"Invalid JSON format in workflow: {str(e)}"
                    print(error_msg)
                    return jsonify({
                        "success": False, 
                        "error": error_msg
                    }), 400
                except Exception as e:
                    error_msg = f"Error saving workflow: {str(e)}"
                    print(error_msg)
                    return jsonify({
                        "success": False, 
                        "error": error_msg
                    }), 500
            except Exception as e:
                error_msg = f"Error creating workflow directory: {str(e)}"
                print(error_msg)
                return jsonify({
                    "success": False, 
                    "error": error_msg
                }), 500
        except Exception as e:
            error_msg = f"Error generating workflow: {str(e)}"
            print(error_msg)
            traceback.print_exc()
            return jsonify({
                "success": False, 
                "error": error_msg
            }), 500
    except Exception as e:
        error_msg = f"Unexpected server error: {str(e)}"
        print(error_msg)
        traceback.print_exc()
        return jsonify({
            "success": False, 
            "error": error_msg
        }), 500

@app.route('/api/workflow-readme/<workflow_folder>', methods=['GET'])
def get_workflow_readme(workflow_folder):
    """Get README content for a workflow"""
    try:
        # Sanitize the workflow_folder to prevent path traversal attacks
        workflow_folder = secure_filename(workflow_folder)
        
        base_path = os.path.join(os.path.dirname(__file__), 'automation')
        readme_path = os.path.join(base_path, workflow_folder, 'README.md')
        
        if os.path.exists(readme_path):
            try:
                with open(readme_path, 'r') as f:
                    content = f.read()
                return jsonify({"success": True, "readme": content})
            except Exception as file_error:
                error_message = f"Error reading README file: {str(file_error)}"
                print(error_message)
                return jsonify({"success": False, "error": error_message}), 500
        
        # If not found in filesystem, try the database
        try:
            readme_response = supabase.table('workflows') \
                .select('readme_content') \
                .eq('slug', workflow_folder) \
                .single() \
                .execute()
            
            if readme_response.data and 'readme_content' in readme_response.data:
                return jsonify({"success": True, "readme": readme_response.data['readme_content']})
        except Exception as db_error:
            error_message = f"Error querying database for README: {str(db_error)}"
            print(error_message)
            # Continue to return the standard not found error
        
        return jsonify({"success": False, "error": "README not found"}), 404
    except Exception as general_error:
        error_message = f"Error retrieving README: {str(general_error)}"
        print(error_message)
        traceback.print_exc()
        return jsonify({"success": False, "error": error_message}), 500

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
        # Sanitize the workflow_folder input to prevent injection
        workflow_folder = secure_filename(workflow_folder)
        
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
        print(f"Error getting rating: {str(e)}")
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
        
        # Sync the workflow to the database
        sync_workflow_immediately(workflow_path)
        
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
        # Sanitize the workflow_folder input to prevent injection
        workflow_folder = secure_filename(workflow_folder)
        
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
            
            try:
                supabase.table('workflow_ratings').insert({
                    'workflow_id': workflow_folder,
                    'upvotes': upvotes,
                    'downvotes': downvotes
                }).execute()
                
                return jsonify({
                    "success": True,
                    "upvotes": upvotes,
                    "downvotes": downvotes,
                    "message": "Rating added successfully"
                })
            except Exception as insert_err:
                error_message = str(insert_err)
                if '42501' in error_message and 'row-level security policy' in error_message:
                    return jsonify({
                        "success": False,
                        "error": "Permission denied. RLS policy not configured correctly. Please contact the administrator.",
                        "details": "The database is missing an RLS policy that allows inserting ratings. Run the add_workflow_ratings_policy.sql script."
                    }), 403
                else:
                    raise insert_err
        else:
            # Update the existing record
            rating_id = response.data[0]['id']
            current_upvotes = response.data[0]['upvotes'] or 0  # Default to 0 if None
            current_downvotes = response.data[0]['downvotes'] or 0  # Default to 0 if None
            
            try:
                if vote_type == 'upvote':
                    supabase.table('workflow_ratings').update({
                        'upvotes': current_upvotes + 1
                    }).eq('id', rating_id).execute()
                    current_upvotes += 1
                else:
                    supabase.table('workflow_ratings').update({
                        'downvotes': current_downvotes + 1
                    }).eq('id', rating_id).execute()
                    current_downvotes += 1
                
                # Return the updated counts
                return jsonify({
                    "success": True,
                    "upvotes": current_upvotes,
                    "downvotes": current_downvotes,
                    "message": "Rating updated successfully"
                })
            except Exception as update_err:
                error_message = str(update_err)
                if '42501' in error_message and 'row-level security policy' in error_message:
                    return jsonify({
                        "success": False,
                        "error": "Permission denied. RLS policy not configured correctly. Please contact the administrator.",
                        "details": "The database is missing an RLS policy that allows updating ratings. Run the add_workflow_ratings_policy.sql script."
                    }), 403
                else:
                    raise update_err
    except Exception as e:
        print(f"Error rating workflow: {str(e)}")
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
        try:
            img = Image.open(screenshot_file)
            
            # Convert the image to RGB mode if it's not already
            if img.mode != 'RGB':
                img = img.convert('RGB')
                
            # Save image to buffer
            img_byte_arr = io.BytesIO()
            img.save(img_byte_arr, format='JPEG')
            img_byte_arr.seek(0)
        except Exception as img_error:
            return jsonify({
                "success": False,
                "error": f"Error processing image: {str(img_error)}",
                "error_type": "image_processing_error"
            }), 400
        
        # Convert to base64 for Gemini
        encoded_img = base64.b64encode(img_byte_arr.getvalue()).decode('ascii')
        mime_type = "image/jpeg"
        
        # Configure Gemini model for image analysis
        if GEMINI_API_KEY:
            try:
                genai.configure(api_key=GEMINI_API_KEY)
            except Exception as config_error:
                return jsonify({
                    "success": False,
                    "error": f"Error configuring Gemini API: {str(config_error)}",
                    "error_type": "api_config_error"
                }), 500
        else:
            return jsonify({
                "success": False,
                "error": "GEMINI_API_KEY not configured. Unable to process image.",
                "error_type": "api_key_missing"
            }), 500
        
        # Use Gemini Pro Vision to analyze the image
        try:
            model = genai.GenerativeModel('gemini-1.5-flash')
            
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
            
            # Extract workflow information using the new system prompt
            extraction_prompt = [
                workflow_builder.image_extraction_prompt,
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
        except Exception as api_error:
            return jsonify({
                "success": False,
                "error": f"Error calling Gemini API: {str(api_error)}",
                "error_type": "api_call_error"
            }), 500
        
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
                if "name" not in workflow_json or not workflow_json["name"] or workflow_json["name"] == "Extracted Workflow":
                    # Generate a more descriptive title based on nodes and workflow structure
                    nodes = workflow_json.get("nodes", [])
                    
                    # Collect node types to understand workflow purpose
                    node_types = {}
                    for node in nodes:
                        node_type = node.get('type', '').replace('n8n-nodes-base.', '')
                        if node_type not in node_types:
                            node_types[node_type] = []
                        node_types[node_type].append(node.get('name', node_type))
                    
                    # Try to generate a meaningful title
                    title_components = []
                    
                    # Look for trigger nodes (typically start the workflow)
                    triggers = []
                    for node_type, names in node_types.items():
                        if any(trigger_keyword in node_type.lower() for trigger_keyword in ['trigger', 'webhook', 'schedule', 'cron', 'poll']):
                            triggers.extend(names)
                    
                    # Look for important action nodes
                    actions = []
                    for node_type, names in node_types.items():
                        if any(action_keyword in node_type.lower() for action_keyword in ['http', 'email', 'slack', 'telegram', 'discord', 'database', 'google', 'api']):
                            actions.extend(names)
                    
                    # Construct the title
                    if triggers:
                        title_components.append(f"{triggers[0]}")
                    
                    if actions:
                        title_components.append(f"to {actions[0]}")
                        if len(actions) > 1:
                            title_components.append(f"and {actions[1]}")
                    
                    # Fallback if no specific triggers or actions found
                    if not title_components and node_types:
                        most_important_type = max(node_types.items(), key=lambda x: len(x[1]))[0]
                        title_components.append(f"{most_important_type} Workflow")
                    
                    # Create the final title
                    if title_components:
                        workflow_json["name"] = " ".join(title_components).title() + " Workflow"
                    else:
                        workflow_json["name"] = "Multi-Step Automation Workflow"
                
                # Sanitize JSON to remove any potential HTML content
                try:
                    workflow_json_str = json.dumps(workflow_json)
                    if '<' in workflow_json_str or '>' in workflow_json_str:
                        print("Potential HTML content found in extracted workflow, sanitizing")
                        # Additional sanitization for HTML content
                        workflow_json_str = workflow_json_str.replace('<', '&lt;').replace('>', '&gt;')
                        # Parse it back into a Python object
                        workflow_json = json.loads(workflow_json_str)
                except Exception as sanitize_error:
                    print(f"Warning during JSON sanitization: {str(sanitize_error)}")
                
                # Create a directory name for the workflow
                base_path = os.path.join(os.path.dirname(__file__), 'automation')
                
                # Ensure automation directory exists
                os.makedirs(base_path, exist_ok=True)
                
                # Generate a unique ID for this extraction
                try:
                    existing_dirs = [d for d in os.listdir(base_path) if os.path.isdir(os.path.join(base_path, d))]
                    highest_num = 0
                    for dir_name in existing_dirs:
                        match = re.match(r'^(\d+)', dir_name)
                        if match:
                            num = int(match.group(1))
                            highest_num = max(highest_num, num)
                    
                    new_num = highest_num + 1
                    dir_name = f"{new_num}-extracted-workflow-{uuid.uuid4().hex[:8]}"
                except Exception as dir_error:
                    return jsonify({
                        "success": False,
                        "error": f"Error creating directory name: {str(dir_error)}",
                        "error_type": "directory_error"
                    }), 500
                
                # Generate an informative README
                try:
                    workflow_name = workflow_json.get('name', 'Extracted Workflow')
                    readme_content = f"# {workflow_name}\n\n"
                    readme_content += f"Categories: AI, Extracted\n\n"
                    readme_content += f"This workflow was extracted from a screenshot using AI recognition technology. It provides an automation solution for {workflow_name.lower().replace(' workflow', '')}.\n\n"
                    
                    # Count nodes by type
                    node_types = {}
                    for node in workflow_json.get('nodes', []):
                        node_type = node.get('type', '').replace('n8n-nodes-base.', '')
                        if node_type not in node_types:
                            node_types[node_type] = []
                        node_types[node_type].append(node.get('name', node_type))
                    
                    if node_types:
                        readme_content += "## Technical Details\n\n"
                        readme_content += f"This workflow consists of {len(workflow_json.get('nodes', []))} nodes that work together to automate your process. Here's what it uses:\n\n"
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
                    readme_content += "This workflow was automatically extracted from a screenshot. While we've made every effort to accurately recreate it, some configuration details might need manual adjustment.\n"
                except Exception as readme_error:
                    print(f"Error generating README: {str(readme_error)}")
                    readme_content = f"# Extracted Workflow\n\nThis workflow was extracted from a screenshot using AI technology."
                
                # Save the files
                try:
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
                except Exception as save_error:
                    return jsonify({
                        "success": False,
                        "error": f"Error saving workflow files: {str(save_error)}",
                        "error_type": "file_save_error"
                    }), 500
                
                # Sync the workflow to the database
                try:
                    def background_sync():
                        try:
                            # Create application context for the thread
                            with app.app_context():
                                sync_workflow_immediately(dir_name)
                        except Exception as e:
                            print(f"Background sync error: {str(e)}")
                            
                    import threading
                    sync_thread = threading.Thread(target=background_sync)
                    sync_thread.daemon = True
                    sync_thread.start()
                except Exception as sync_error:
                    print(f"Warning: Failed to start background sync: {str(sync_error)}")
                    # Continue even if sync fails
                
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
        except json.JSONDecodeError as json_error:
            return jsonify({
                "success": False,
                "error": f"Invalid JSON format: {str(json_error)}",
                "error_type": "invalid_json"
            }), 400
        except Exception as processing_error:
            return jsonify({
                "success": False,
                "error": f"Error processing workflow: {str(processing_error)}",
                "error_type": "processing_error"
            }), 500
    except Exception as general_error:
        print(f"Error processing image extraction request: {str(general_error)}")
        traceback.print_exc()
        return jsonify({
            "success": False,
            "error": f"Error processing image: {str(general_error)}",
            "error_type": "general_error"
        }), 500

@app.route('/api/add-workflow', methods=['POST'])
def add_workflow():
    """Add a new workflow to the gallery from user submission"""
    try:
        data = request.json
        
        # Validate required fields
        required_fields = ['author_name', 'workflow_title', 'workflow_description', 'categories', 'workflow_json']
        for field in required_fields:
            if field not in data or not data[field]:
                return jsonify({
                    "success": False,
                    "error": f"Missing required field: {field}"
                }), 400
        
        # Validate categories
        categories = data['categories']
        if not categories or len(categories) == 0:
            return jsonify({
                "success": False,
                "error": "At least one category is required"
            }), 400
            
        if len(categories) > 3:
            categories = categories[:3]  # Limit to 3 categories
        
        # Validate workflow JSON
        workflow_json = data['workflow_json']
        
        if not isinstance(workflow_json, dict) or 'nodes' not in workflow_json or not isinstance(workflow_json['nodes'], list):
            return jsonify({
                "success": False,
                "error": "Invalid workflow JSON format"
            }), 400
        
        # Set workflow name if not already set
        if 'name' not in workflow_json or not workflow_json['name']:
            workflow_json['name'] = data['workflow_title']
        
        # Create a directory name for the workflow
        base_path = os.path.join(os.path.dirname(__file__), 'automation')
        
        # Ensure automation directory exists
        os.makedirs(base_path, exist_ok=True)
        
        # Find the highest number and increment by 1
        existing_dirs = [d for d in os.listdir(base_path) if os.path.isdir(os.path.join(base_path, d))]
        highest_num = 0
        for dir_name in existing_dirs:
            match = re.match(r'^(\d+)', dir_name)
            if match:
                num = int(match.group(1))
                highest_num = max(highest_num, num)
        
        new_num = highest_num + 1
        workflow_title_slug = data['workflow_title'].lower().replace(' ', '-')
        workflow_title_slug = re.sub(r'[^a-z0-9\-]', '', workflow_title_slug)
        dir_name = f"{new_num}-{workflow_title_slug[:30]}"
        
        # Create directory
        workflow_dir = os.path.join(base_path, dir_name)
        os.makedirs(workflow_dir, exist_ok=True)
        
        # Save workflow.json
        workflow_path = os.path.join(workflow_dir, 'workflow.json')
        with open(workflow_path, 'w') as f:
            json.dump(workflow_json, f, indent=2)
        
        # Generate README.md
        readme_content = f"# {data['workflow_title']}\n\n"
        readme_content += f"Categories: {', '.join(categories)}\n\n"
        readme_content += f"{data['workflow_description']}\n\n"
        
        # Add technical details based on nodes
        nodes = workflow_json.get('nodes', [])
        node_types = {}
        for node in nodes:
            node_type = node.get('type', '').replace('n8n-nodes-base.', '')
            if node_type not in node_types:
                node_types[node_type] = []
            node_types[node_type].append(node.get('name', node_type))
        
        if node_types:
            readme_content += "## Technical Details\n\n"
            readme_content += f"This workflow consists of {len(nodes)} nodes that work together to automate your process. Here's what it uses:\n\n"
            for node_type, node_names in node_types.items():
                node_name_list = ", ".join(node_names)
                readme_content += f"- {node_type}: {node_name_list}\n"
            readme_content += "\n"
        
        # Add usage instructions
        readme_content += "## Usage\n\n"
        readme_content += "1. Download the workflow JSON file\n"
        readme_content += "2. Import it into your n8n instance\n"
        readme_content += "3. Review and adjust the workflow as needed\n"
        readme_content += "4. Activate and test the workflow\n\n"
        
        # Save README.md
        readme_path = os.path.join(workflow_dir, 'README.md')
        with open(readme_path, 'w') as f:
            f.write(readme_content)
        
        # Create meta.json
        meta_path = os.path.join(workflow_dir, 'meta.json')
        meta_data = {
            "categories": categories,
            "generated": False,
            "submitted": True,
            "submission_date": datetime.datetime.now().isoformat(),
            "author": data['author_name'],
            "summary": data['workflow_description'][:100],
            "published": True,
            "published_date": datetime.datetime.now().isoformat(),
            "published_by": data['author_name']
        }
        
        with open(meta_path, 'w') as f:
            json.dump(meta_data, f, indent=2)
        
        # Create initial ratings in the database
        try:
            supabase.table('workflow_ratings').insert({
                'workflow_id': dir_name,
                'upvotes': 0,
                'downvotes': 0
            }).execute()
        except Exception as e:
            print(f"Warning: Unable to create initial ratings: {str(e)}")
        
        # Sync the workflow to the database
        sync_workflow_immediately(dir_name)
        
        return jsonify({
            "success": True,
            "message": "Workflow successfully added to the gallery!",
            "workflow_id": dir_name
        })
        
    except json.JSONDecodeError as e:
        return jsonify({
            "success": False,
            "error": f"Invalid JSON: {str(e)}"
        }), 400
    except Exception as e:
        print(f"Error adding workflow: {str(e)}")
        return jsonify({
            "success": False,
            "error": f"An unexpected error occurred: {str(e)}"
        }), 500

# Function to sync a workflow to the database immediately
def sync_workflow_immediately(workflow_dir):
    """Synchronize a workflow to the database immediately after creation or update"""
    try:
        # Check if we have Supabase configured
        if not supabase:
            print("Supabase not configured, skipping immediate sync")
            return
        
        # Ensure the workflow directory exists
        base_path = os.path.join(os.path.dirname(__file__), 'automation')
        workflow_path = os.path.join(base_path, workflow_dir)
        
        if not os.path.exists(workflow_path):
            print(f"Workflow directory not found: {workflow_path}")
            return
            
        # Check for workflow.json and README.md
        workflow_json_path = os.path.join(workflow_path, 'workflow.json')
        readme_path = os.path.join(workflow_path, 'README.md')
        meta_path = os.path.join(workflow_path, 'meta.json')
        
        if not os.path.exists(workflow_json_path) or not os.path.exists(readme_path):
            print(f"Workflow files not found in: {workflow_path}")
            return
            
        # Load workflow data
        with open(workflow_json_path, 'r') as f:
            workflow_data = json.load(f)
            
        # Load README content
        with open(readme_path, 'r') as f:
            readme_content = f.read()
            
        # Parse name from path (remove number prefix if exists)
        name_parts = workflow_dir.split('-', 1)
        workflow_name = name_parts[1] if len(name_parts) > 1 else name_parts[0]
        
        # Replace hyphens with spaces and capitalize
        workflow_name = workflow_name.replace('-', ' ').strip()
        workflow_name = ' '.join(word.capitalize() for word in workflow_name.split())
        
        # Load meta data if exists
        categories = ["AI", "Engineering"]  # Default categories
        is_published = False
        is_generated = True
        
        if os.path.exists(meta_path):
            try:
                with open(meta_path, 'r') as f:
                    meta_data = json.load(f)
                    categories = meta_data.get('categories', categories)
                    is_published = meta_data.get('published', False)
                    is_generated = meta_data.get('generated', True)
            except:
                print(f"Error loading meta data from: {meta_path}")
        
        # Try to extract the first paragraph from README as description
        description = ""
        readme_lines = readme_content.strip().split('\n')
        for line in readme_lines:
            line = line.strip()
            if line and not line.startswith('#'):
                description = line
                break
                
        if not description and len(readme_lines) > 1:
            # Fallback to the first line after the title
            for i in range(1, len(readme_lines)):
                if readme_lines[i].strip():
                    description = readme_lines[i].strip()
                    break
        
        # Trim description to max 150 chars
        if len(description) > 150:
            description = description[:147] + "..."
            
        # Get current user as author (if authenticated)
        author_name = session.get('user', {}).get('email', 'anonymous')
        
        # Sync to database using the sync_workflow_to_database function
        try:
            response = supabase.rpc('sync_workflow_to_database', {
                'p_slug': workflow_dir,
                'p_title': workflow_name,
                'p_description': description,
                'p_author_name': author_name,
                'p_json_content': workflow_data,
                'p_readme_content': readme_content,
                'p_categories': categories,
                'p_is_generated': is_generated,
                'p_is_submitted': is_published,
                'p_is_extracted': False
            }).execute()
            
            print(f"Synchronized workflow to database: {workflow_dir}, published: {is_published}")
            
            # Ensure meta file is updated with the correct published status
            if os.path.exists(meta_path):
                try:
                    with open(meta_path, 'r') as f:
                        meta_data = json.load(f)
                    
                    # Update is_published status to match what was sent to database
                    meta_data['published'] = is_published
                    
                    with open(meta_path, 'w') as f:
                        json.dump(meta_data, f, indent=2)
                except Exception as e:
                    print(f"Error updating meta file: {str(e)}")
                    
        except Exception as e:
            print(f"Error syncing workflow to database: {str(e)}")
            # Still proceed with the flow even if database sync fails
            
    except Exception as e:
        print(f"Error in immediate workflow sync: {str(e)}")

# TODO: Add download route, meme animation, and user upload logic

# Create Heroku-compatible app
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)

# Gunicorn configuration for Heroku - these are accessed when the app is run with Gunicorn
# The default worker timeout in Heroku is 30 seconds, which can lead to H12 errors
# Let's add some optimizations to better handle long-running API requests

# Increase the worker timeout to 60 seconds
timeout = 60

# Use 2-4 workers as recommended by Heroku for standard dynos
workers = int(os.environ.get('WEB_CONCURRENCY', 3))

# Use worker class designed for async operations to process more requests
worker_class = 'gevent'

# Increase max requests to reduce worker churn
max_requests = 1000
max_requests_jitter = 200

# Log to stdout, which Heroku captures
accesslog = '-'  # stdout
errorlog = '-'   # stderr
loglevel = 'info'

# This will be used by Heroku's Procfile "web: gunicorn app:app"

# Add a context processor to make user info available in all templates
@app.context_processor
def inject_user():
    return dict(
        user=session.get('user', None),
        year=datetime.datetime.now().year
    )

@app.route('/profile')
@requires_auth
def profile():
    return render_template('profile.html')

@app.route('/admin', methods=['GET', 'POST'])
def admin_panel():
    error = None
    # Admin authentication
    if request.method == 'POST':
        access_code = request.form.get('access_code')
        if access_code == '123456':  # Hard-coded access code
            session['admin_authenticated'] = True
            return redirect('/admin')
        else:
            error = "Invalid access code. Please try again."
    
    # If already authenticated or after successful authentication
    if session.get('admin_authenticated'):
        # Get all automations from both database and filesystem
        automations = []
        automations_ids = set()  # To track unique IDs
        
        # STEP 1: Fetch from database first (this ensures we get ALL workflows)
        try:
            workflows_response = supabase.table('workflows').select(
                'id, slug, title, description, author_name, is_generated, is_submitted, is_extracted, published_date, published'
            ).execute()
            
            if workflows_response.data:
                # Get all categories in one query for better performance
                all_categories = {}
                categories_response = supabase.table('workflow_categories').select('workflow_id, category').execute()
                if categories_response.data:
                    for cat_entry in categories_response.data:
                        wf_id = cat_entry['workflow_id']
                        category = cat_entry['category']
                        if wf_id not in all_categories:
                            all_categories[wf_id] = []
                        all_categories[wf_id].append(category)
                
                # Process workflows from the database
                for workflow in workflows_response.data:
                    workflow_id = workflow['slug']
                    
                    # Skip if we already have this workflow from filesystem
                    if any(a['id'] == workflow_id for a in automations):
                        continue
                    
                    # Get categories for this workflow
                    categories = all_categories.get(workflow['id'], [DEFAULT_CATEGORY])
                    
                    # Get ratings data for this workflow
                    rating = {'upvotes': 0, 'downvotes': 0}
                    
                    automation = {
                        'id': workflow_id,
                        'title': workflow['title'],
                        'description': workflow['description'],
                        'author': workflow['author_name'],
                        'categories': categories,
                        'from_database': True
                    }
                    automations.append(automation)
                    
                print(f"Found {len(automations)} workflows in the database")
        except Exception as e:
            print(f"Error fetching workflows from database: {str(e)}")
        
        # STEP 2: Check filesystem for any workflows not in the database
        base_path = os.path.join(os.path.dirname(__file__), 'automation')
        if os.path.exists(base_path):
            folders = os.listdir(base_path)
            folders.sort()  # Sort folders alphabetically
            
            for folder in folders:
                # Skip if we already have this from the database
                if folder in automations_ids:
                    continue
                    
                folder_path = os.path.join(base_path, folder)
                if os.path.isdir(folder_path):
                    readme_path = os.path.join(folder_path, 'README.md')
                    meta_path = os.path.join(folder_path, 'meta.json')
                    workflow_path = os.path.join(folder_path, 'workflow.json')
                    
                    # Skip if workflow.json doesn't exist
                    if not os.path.exists(workflow_path):
                        continue
                    
                    # Get title and description
                    title = folder.split('-', 1)[1] if '-' in folder else folder
                    title = title.replace('-', ' ').strip().title()
                    description = ""
                    author = "Unknown"
                    categories = []
                    
                    # Try meta.json
                    if os.path.exists(meta_path):
                        try:
                            with open(meta_path, 'r') as f:
                                meta_data = json.load(f)
                                author = meta_data.get('author', author)
                                categories = meta_data.get('categories', [])
                                if meta_data.get('summary'):
                                    description = meta_data.get('summary')
                        except:
                            pass
                    
                    # Try README.md if no description yet
                    if not description and os.path.exists(readme_path):
                        try:
                            with open(readme_path, 'r') as f:
                                readme_lines = f.readlines()
                                for line in readme_lines:
                                    if line.strip() and not line.startswith('#'):
                                        description = line.strip()
                                        break
                        except:
                            pass
                    
                    # Add to our list
                    automations_ids.add(folder)
                    automation = {
                        'id': folder,
                        'title': title,
                        'description': description,
                        'author': author,
                        'categories': categories,
                        'from_database': False
                    }
                    automations.append(automation)
            
            print(f"Total workflows after filesystem check: {len(automations)}")
        
        # Sort automations by ID (numerically)
        def extract_numeric(automation):
            match = re.match(r'^(\d+)', automation['id'])
            return int(match.group(1)) if match else float('inf')
            
        automations.sort(key=extract_numeric)
        
        return render_template('admin.html', automations=automations, authenticated=True)
    
    return render_template('admin.html', authenticated=False, error=error)

@app.route('/admin/delete', methods=['POST'])
@requires_admin
def delete_automation():
    automation_id = request.form.get('automation_id')
    if not automation_id:
        return redirect('/admin')
    
    # Path to the automation folder
    automation_path = os.path.join(os.path.dirname(__file__), 'automation', automation_id)
    
    # Delete from the database first
    db_deleted = False
    try:
        # Delete from workflow_ratings table
        ratings_result = supabase.table('workflow_ratings').delete().eq('workflow_id', automation_id).execute()
        
        # Delete from workflow_categories table
        categories_result = supabase.table('workflow_categories').delete().eq('workflow_id', automation_id).execute()
        
        # Delete from workflows table
        workflow_result = supabase.table('workflows').delete().eq('slug', automation_id).execute()
        
        # Check if we actually deleted anything from the workflows table
        if workflow_result.data and len(workflow_result.data) > 0:
            print(f"Successfully deleted automation {automation_id} from database")
            db_deleted = True
        else:
            print(f"No records found in database for automation {automation_id}")
    except Exception as e:
        print(f"Error deleting automation from database: {str(e)}")
    
    # Delete the folder from the filesystem if it exists
    fs_deleted = False
    if os.path.exists(automation_path):
        try:
            shutil.rmtree(automation_path)
            print(f"Deleted automation folder: {automation_path}")
            fs_deleted = True
        except Exception as e:
            print(f"Error deleting automation folder: {str(e)}")
    
    if db_deleted or fs_deleted:
        return redirect('/admin?status=success&message=Automation+successfully+deleted')
    else:
        return redirect('/admin?status=error&message=Failed+to+delete+automation') 