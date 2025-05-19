# pewpew.buzz

A futuristic, neon-themed Flask web app for sharing and downloading N8n AI automations, featuring the iconic pewpew cat meme.

## Features
- Auth0 authentication for all users
- Supabase backend for automation metadata and file storage
- Neon, minimalist UI with TailwindCSS
- Meme branding: static and animated pewpew cat
- Dashboard: browse, search, and download automations
- Add new automations (all logged-in users)
- "How to Use" instructions

## Tech Stack
- Flask (Python)
- Jinja2 templates
- TailwindCSS
- Supabase (PostgreSQL + Storage)
- Auth0

## Setup
1. Clone the repo
2. Install dependencies: `pip install -r requirements.txt`
3. Configure Auth0 and Supabase credentials in `.env`:
   - `SUPABASE_URL=https://zqaahjrxjwakucakdaoc.supabase.co`
   - `SUPABASE_KEY=your_supabase_service_role_or_anon_key`
4. Run the app: `flask run`

## Supabase Integration
- The backend uses the official `supabase-py` Python client:
  ```python
  from supabase import create_client
  supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
  ```
- If you want to use Supabase from the frontend (JavaScript), use:
  ```js
  import { createClient } from '@supabase/supabase-js'
  const supabaseUrl = 'https://zqaahjrxjwakucakdaoc.supabase.co'
  const supabaseKey = process.env.SUPABASE_KEY
  const supabase = createClient(supabaseUrl, supabaseKey)
  ```
- All backend database access is handled via Python.

## Meme Integration
- Place the provided pewpew cat image in `static/images/`
- Animation handled via CSS/JS in the hero section

---

For detailed setup, see the comments in `app.py` and the templates.
