-- Supabase Schema for pewpew.buzz
-- This script creates all necessary tables, indexes, and RLS policies
-- Fixed version without IF NOT EXISTS for policies

-- Enable necessary extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- ==========================================
-- User Management Tables
-- ==========================================

-- User profiles table (extends Auth.users)
CREATE TABLE IF NOT EXISTS user_profiles (
    id UUID PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
    display_name TEXT,
    website TEXT,
    avatar_url TEXT,
    bio TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- User preferences table
CREATE TABLE IF NOT EXISTS user_preferences (
    user_id UUID PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
    theme TEXT DEFAULT 'dark',
    email_notifications BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- ==========================================
-- Workflow Management Tables
-- ==========================================

-- Workflows table (main table for automation workflows)
CREATE TABLE IF NOT EXISTS workflows (
    id SERIAL PRIMARY KEY,
    slug TEXT NOT NULL UNIQUE,
    title TEXT NOT NULL,
    description TEXT,
    author_id UUID REFERENCES auth.users(id) ON DELETE SET NULL,
    author_name TEXT NOT NULL, -- Store name even if user account is deleted
    json_content JSONB NOT NULL, -- The actual workflow JSON
    readme_content TEXT, -- Markdown content for README
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    published BOOLEAN DEFAULT TRUE,
    published_date TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    views INTEGER DEFAULT 0,
    downloads INTEGER DEFAULT 0,
    is_generated BOOLEAN DEFAULT FALSE, -- Whether created via AI
    is_submitted BOOLEAN DEFAULT FALSE, -- Whether submitted by a user
    is_extracted BOOLEAN DEFAULT FALSE -- Whether extracted from a screenshot
);

-- Create index for faster searching on common fields
CREATE INDEX IF NOT EXISTS idx_workflows_title ON workflows USING gin (to_tsvector('english', title));
CREATE INDEX IF NOT EXISTS idx_workflows_description ON workflows USING gin (to_tsvector('english', description));
CREATE INDEX IF NOT EXISTS idx_workflows_slug ON workflows (slug);

-- Workflow categories table
CREATE TABLE IF NOT EXISTS workflow_categories (
    workflow_id INTEGER REFERENCES workflows(id) ON DELETE CASCADE,
    category TEXT NOT NULL,
    PRIMARY KEY (workflow_id, category)
);

-- Create index for faster category filtering
CREATE INDEX IF NOT EXISTS idx_workflow_categories_category ON workflow_categories (category);

-- Workflow ratings table (thumbs up/down)
CREATE TABLE IF NOT EXISTS workflow_ratings (
    id SERIAL PRIMARY KEY,
    workflow_id TEXT NOT NULL UNIQUE, -- Using the folder ID for compatibility
    upvotes INTEGER DEFAULT 0,
    downvotes INTEGER DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- User ratings table (tracks individual user ratings to prevent duplicates)
CREATE TABLE IF NOT EXISTS user_ratings (
    id SERIAL PRIMARY KEY,
    user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE,
    workflow_id INTEGER REFERENCES workflows(id) ON DELETE CASCADE,
    rating_type TEXT CHECK (rating_type IN ('upvote', 'downvote')),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(user_id, workflow_id)
);

-- ==========================================
-- Analytics Tables
-- ==========================================

-- Workflow views tracking
CREATE TABLE IF NOT EXISTS workflow_views (
    id SERIAL PRIMARY KEY,
    workflow_id INTEGER REFERENCES workflows(id) ON DELETE CASCADE,
    user_id UUID REFERENCES auth.users(id) ON DELETE SET NULL,
    viewed_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    ip_address TEXT,
    user_agent TEXT
);

-- Workflow download tracking
CREATE TABLE IF NOT EXISTS workflow_downloads (
    id SERIAL PRIMARY KEY,
    workflow_id INTEGER REFERENCES workflows(id) ON DELETE CASCADE,
    user_id UUID REFERENCES auth.users(id) ON DELETE SET NULL,
    downloaded_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    ip_address TEXT,
    user_agent TEXT
);

-- ==========================================
-- Row Level Security Policies
-- ==========================================

-- Enable RLS on all tables
ALTER TABLE user_profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE user_preferences ENABLE ROW LEVEL SECURITY;
ALTER TABLE workflows ENABLE ROW LEVEL SECURITY;
ALTER TABLE workflow_categories ENABLE ROW LEVEL SECURITY;
ALTER TABLE workflow_ratings ENABLE ROW LEVEL SECURITY;
ALTER TABLE user_ratings ENABLE ROW LEVEL SECURITY;
ALTER TABLE workflow_views ENABLE ROW LEVEL SECURITY;
ALTER TABLE workflow_downloads ENABLE ROW LEVEL SECURITY;

-- User profile policies
DROP POLICY IF EXISTS "Users can view all profiles" ON user_profiles;
CREATE POLICY "Users can view all profiles"
ON user_profiles FOR SELECT
TO authenticated, anon
USING (true);

DROP POLICY IF EXISTS "Users can update their own profile" ON user_profiles;
CREATE POLICY "Users can update their own profile"
ON user_profiles FOR UPDATE
TO authenticated
USING (id = auth.uid());

-- User preferences policies
DROP POLICY IF EXISTS "Users can view their own preferences" ON user_preferences;
CREATE POLICY "Users can view their own preferences"
ON user_preferences FOR SELECT
TO authenticated
USING (user_id = auth.uid());

DROP POLICY IF EXISTS "Users can update their own preferences" ON user_preferences;
CREATE POLICY "Users can update their own preferences"
ON user_preferences FOR UPDATE
TO authenticated
USING (user_id = auth.uid());

-- Workflow policies
DROP POLICY IF EXISTS "Anyone can view published workflows" ON workflows;
CREATE POLICY "Anyone can view published workflows"
ON workflows FOR SELECT
TO authenticated, anon
USING (published = true);

DROP POLICY IF EXISTS "Users can view their own unpublished workflows" ON workflows;
CREATE POLICY "Users can view their own unpublished workflows"
ON workflows FOR SELECT
TO authenticated
USING (author_id = auth.uid());

DROP POLICY IF EXISTS "Users can update their own workflows" ON workflows;
CREATE POLICY "Users can update their own workflows"
ON workflows FOR UPDATE
TO authenticated
USING (author_id = auth.uid());

DROP POLICY IF EXISTS "Users can delete their own workflows" ON workflows;
CREATE POLICY "Users can delete their own workflows"
ON workflows FOR DELETE
TO authenticated
USING (author_id = auth.uid());

-- Workflow categories policies
DROP POLICY IF EXISTS "Anyone can view workflow categories" ON workflow_categories;
CREATE POLICY "Anyone can view workflow categories"
ON workflow_categories FOR SELECT
TO authenticated, anon
USING (true);

-- Workflow ratings policies
DROP POLICY IF EXISTS "Anyone can view workflow ratings" ON workflow_ratings;
CREATE POLICY "Anyone can view workflow ratings"
ON workflow_ratings FOR SELECT
TO authenticated, anon
USING (true);

-- User ratings policies
DROP POLICY IF EXISTS "Users can view their own ratings" ON user_ratings;
CREATE POLICY "Users can view their own ratings"
ON user_ratings FOR SELECT
TO authenticated
USING (user_id = auth.uid());

-- ==========================================
-- Functions and Triggers
-- ==========================================

-- Function to update the updated_at timestamp
CREATE OR REPLACE FUNCTION update_timestamp()
RETURNS TRIGGER AS $$
BEGIN
   NEW.updated_at = CURRENT_TIMESTAMP;
   RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Create triggers for updated_at on all tables
DROP TRIGGER IF EXISTS update_user_profiles_timestamp ON user_profiles;
CREATE TRIGGER update_user_profiles_timestamp
BEFORE UPDATE ON user_profiles
FOR EACH ROW EXECUTE PROCEDURE update_timestamp();

DROP TRIGGER IF EXISTS update_user_preferences_timestamp ON user_preferences;
CREATE TRIGGER update_user_preferences_timestamp
BEFORE UPDATE ON user_preferences
FOR EACH ROW EXECUTE PROCEDURE update_timestamp();

DROP TRIGGER IF EXISTS update_workflows_timestamp ON workflows;
CREATE TRIGGER update_workflows_timestamp
BEFORE UPDATE ON workflows
FOR EACH ROW EXECUTE PROCEDURE update_timestamp();

DROP TRIGGER IF EXISTS update_workflow_ratings_timestamp ON workflow_ratings;
CREATE TRIGGER update_workflow_ratings_timestamp
BEFORE UPDATE ON workflow_ratings
FOR EACH ROW EXECUTE PROCEDURE update_timestamp();

-- Function to handle upvoting/downvoting
CREATE OR REPLACE FUNCTION rate_workflow(p_workflow_id TEXT, p_user_id UUID, p_rating_type TEXT)
RETURNS JSONB AS $$
DECLARE
    v_upvotes INTEGER := 0;
    v_downvotes INTEGER := 0;
    v_existing_rating TEXT;
BEGIN
    -- Check for existing rating by this user
    SELECT rating_type INTO v_existing_rating
    FROM user_ratings ur
    JOIN workflows w ON ur.workflow_id = w.id
    WHERE w.slug = p_workflow_id AND ur.user_id = p_user_id;

    -- If user has already rated, don't allow duplicate ratings
    IF v_existing_rating IS NOT NULL AND v_existing_rating = p_rating_type THEN
        -- Get current counts
        SELECT upvotes, downvotes INTO v_upvotes, v_downvotes
        FROM workflow_ratings
        WHERE workflow_id = p_workflow_id;
        
        RETURN jsonb_build_object(
            'success', false,
            'error', 'You have already ' || p_rating_type || 'd this workflow',
            'upvotes', v_upvotes,
            'downvotes', v_downvotes
        );
    END IF;

    -- Update or insert the rating
    INSERT INTO workflow_ratings (workflow_id, upvotes, downvotes)
    VALUES (p_workflow_id, 
            CASE WHEN p_rating_type = 'upvote' THEN 1 ELSE 0 END, 
            CASE WHEN p_rating_type = 'downvote' THEN 1 ELSE 0 END)
    ON CONFLICT (workflow_id)
    DO UPDATE SET
        upvotes = CASE WHEN p_rating_type = 'upvote' 
                        THEN workflow_ratings.upvotes + 1 
                        ELSE workflow_ratings.upvotes END,
        downvotes = CASE WHEN p_rating_type = 'downvote' 
                          THEN workflow_ratings.downvotes + 1 
                          ELSE workflow_ratings.downvotes END;

    -- Record the user rating
    INSERT INTO user_ratings (user_id, workflow_id, rating_type)
    SELECT p_user_id, id, p_rating_type
    FROM workflows
    WHERE slug = p_workflow_id
    ON CONFLICT (user_id, workflow_id)
    DO UPDATE SET
        rating_type = p_rating_type;

    -- Get the updated counts
    SELECT upvotes, downvotes INTO v_upvotes, v_downvotes
    FROM workflow_ratings
    WHERE workflow_id = p_workflow_id;

    RETURN jsonb_build_object(
        'success', true,
        'upvotes', v_upvotes,
        'downvotes', v_downvotes
    );
END;
$$ LANGUAGE plpgsql SECURITY DEFINER; 