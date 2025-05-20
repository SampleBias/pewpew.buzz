-- workflow_synchronization.sql
-- This script creates functions and triggers to synchronize file-based workflows with the database

-- Create a function that will be used to log synchronization events
CREATE TABLE IF NOT EXISTS workflow_sync_log (
    id SERIAL PRIMARY KEY,
    operation TEXT NOT NULL,
    workflow_slug TEXT NOT NULL,
    details JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Function to add a new workflow to the database
CREATE OR REPLACE FUNCTION sync_workflow_to_database(
    p_slug TEXT,
    p_title TEXT,
    p_description TEXT,
    p_author_name TEXT,
    p_json_content JSONB,
    p_readme_content TEXT,
    p_categories TEXT[],
    p_is_generated BOOLEAN DEFAULT FALSE,
    p_is_submitted BOOLEAN DEFAULT FALSE,
    p_is_extracted BOOLEAN DEFAULT FALSE
) RETURNS JSONB AS $$
DECLARE
    v_workflow_id INTEGER;
    v_category TEXT;
    v_result JSONB;
BEGIN
    -- Check if workflow with this slug already exists
    SELECT id INTO v_workflow_id FROM workflows WHERE slug = p_slug;
    
    IF v_workflow_id IS NULL THEN
        -- Insert new workflow
        INSERT INTO workflows (
            slug, 
            title, 
            description, 
            author_name, 
            json_content, 
            readme_content, 
            is_generated, 
            is_submitted, 
            is_extracted,
            published,
            published_date
        ) VALUES (
            p_slug,
            p_title,
            p_description,
            p_author_name,
            p_json_content,
            p_readme_content,
            p_is_generated,
            p_is_submitted,
            p_is_extracted,
            TRUE,
            CURRENT_TIMESTAMP
        ) RETURNING id INTO v_workflow_id;
        
        -- Add to sync log
        INSERT INTO workflow_sync_log (operation, workflow_slug, details)
        VALUES ('INSERT', p_slug, jsonb_build_object('workflow_id', v_workflow_id));
        
        -- Add categories
        FOREACH v_category IN ARRAY p_categories
        LOOP
            INSERT INTO workflow_categories (workflow_id, category)
            VALUES (v_workflow_id, v_category);
        END LOOP;
        
        -- Create initial ratings
        INSERT INTO workflow_ratings (workflow_id, upvotes, downvotes)
        VALUES (p_slug, 0, 0)
        ON CONFLICT (workflow_id) DO NOTHING;
        
        v_result = jsonb_build_object(
            'success', true,
            'operation', 'INSERT',
            'workflow_id', v_workflow_id,
            'message', 'Workflow successfully added to database'
        );
    ELSE
        -- Update existing workflow
        UPDATE workflows SET
            title = p_title,
            description = p_description,
            author_name = p_author_name,
            json_content = p_json_content,
            readme_content = p_readme_content,
            is_generated = p_is_generated,
            is_submitted = p_is_submitted,
            is_extracted = p_is_extracted,
            updated_at = CURRENT_TIMESTAMP
        WHERE id = v_workflow_id;
        
        -- Add to sync log
        INSERT INTO workflow_sync_log (operation, workflow_slug, details)
        VALUES ('UPDATE', p_slug, jsonb_build_object('workflow_id', v_workflow_id));
        
        -- Update categories: first delete existing ones
        DELETE FROM workflow_categories WHERE workflow_id = v_workflow_id;
        
        -- Add new categories
        FOREACH v_category IN ARRAY p_categories
        LOOP
            INSERT INTO workflow_categories (workflow_id, category)
            VALUES (v_workflow_id, v_category);
        END LOOP;
        
        v_result = jsonb_build_object(
            'success', true,
            'operation', 'UPDATE',
            'workflow_id', v_workflow_id,
            'message', 'Workflow successfully updated in database'
        );
    END IF;
    
    RETURN v_result;
EXCEPTION
    WHEN OTHERS THEN
        RETURN jsonb_build_object(
            'success', false,
            'error', SQLERRM,
            'slug', p_slug
        );
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Function to mark a workflow as deleted
CREATE OR REPLACE FUNCTION mark_workflow_deleted(p_slug TEXT) RETURNS JSONB AS $$
DECLARE
    v_workflow_id INTEGER;
BEGIN
    -- Check if workflow exists
    SELECT id INTO v_workflow_id FROM workflows WHERE slug = p_slug;
    
    IF v_workflow_id IS NULL THEN
        RETURN jsonb_build_object(
            'success', false,
            'error', 'Workflow not found',
            'slug', p_slug
        );
    END IF;
    
    -- Add to sync log
    INSERT INTO workflow_sync_log (operation, workflow_slug, details)
    VALUES ('DELETE', p_slug, jsonb_build_object('workflow_id', v_workflow_id));
    
    -- We don't actually delete the workflow, just mark it as unpublished
    UPDATE workflows SET
        published = FALSE,
        updated_at = CURRENT_TIMESTAMP
    WHERE id = v_workflow_id;
    
    RETURN jsonb_build_object(
        'success', true,
        'operation', 'DELETE',
        'workflow_id', v_workflow_id,
        'message', 'Workflow marked as deleted/unpublished'
    );
EXCEPTION
    WHEN OTHERS THEN
        RETURN jsonb_build_object(
            'success', false,
            'error', SQLERRM,
            'slug', p_slug
        );
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Grant necessary permissions to authenticated users
GRANT EXECUTE ON FUNCTION sync_workflow_to_database TO authenticated;
GRANT EXECUTE ON FUNCTION mark_workflow_deleted TO authenticated; 