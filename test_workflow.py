import asyncio
import json
from workflow_builder import N8nWorkflowBuilder

async def test_workflow_generation():
    builder = N8nWorkflowBuilder()
    
    # Test with a workflow that has clear steps
    test_goal = """
    Create a workflow that:
    1. Monitors a Gmail account for new emails with PDF attachments
    2. Downloads and extracts the text from each PDF
    3. Summarizes the content using an AI service
    4. Sends the summary to a Slack channel
    5. Saves the summary and original PDF to Google Drive
    """
    
    print("Testing workflow generation with step-by-step goal...")
    
    # Test step extraction
    steps = builder.extract_workflow_steps(test_goal)
    print("\nExtracted steps:")
    for i, step in enumerate(steps, 1):
        print(f"{i}. {step}")
        
    # Generate a workflow
    result = await builder.generate_workflow(test_goal)
    
    # Check if successful
    if result["success"]:
        print("\nWorkflow generation successful!")
        workflow = result["workflow"]
        print(f"Workflow name: {workflow.get('name', 'Unnamed')}")
        print(f"Node count: {len(workflow.get('nodes', []))}")
        
        # Print warning if any
        if "warning" in result:
            print(f"Warning: {result['warning']}")
            
        # Save to file for inspection
        with open("test_workflow.json", "w") as f:
            json.dump(workflow, f, indent=2)
            print("Saved workflow to test_workflow.json")
    else:
        print(f"Error: {result.get('error', 'Unknown error')}")
        
    return result

if __name__ == "__main__":
    asyncio.run(test_workflow_generation()) 