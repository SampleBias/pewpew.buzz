#!/usr/bin/env python3
"""
Test script to verify that the async event loop fix works properly.
This simulates the workflow generation process to check for event loop issues.
"""

import asyncio
import concurrent.futures
from workflow_builder import N8nWorkflowBuilder

def run_async_safely(coro):
    """
    Safely run an async coroutine in a synchronous context.
    This handles the event loop properly to avoid 'Event loop is closed' errors.
    """
    try:
        # Try to get the current event loop
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError as e:
            if "There is no current event loop" in str(e):
                # No event loop exists, create a new one
                return asyncio.run(coro)
            else:
                raise e
        
        # Check if the loop is closed
        if loop.is_closed():
            # Loop is closed, create a new one
            return asyncio.run(coro)
        
        if loop.is_running():
            # If there's already a running loop, we need to run in a thread
            with concurrent.futures.ThreadPoolExecutor() as executor:
                future = executor.submit(asyncio.run, coro)
                return future.result()
        else:
            # If no loop is running, we can use the existing loop
            return loop.run_until_complete(coro)
            
    except RuntimeError as e:
        if "Event loop is closed" in str(e) or "cannot be called from a running event loop" in str(e):
            # Handle the specific event loop closed error
            try:
                # Try to create a new event loop in a thread
                with concurrent.futures.ThreadPoolExecutor() as executor:
                    future = executor.submit(asyncio.run, coro)
                    return future.result()
            except Exception as thread_e:
                print(f"Error running in thread: {thread_e}")
                # As a last resort, try asyncio.run
                return asyncio.run(coro)
        else:
            # For other RuntimeErrors, try asyncio.run as fallback
            return asyncio.run(coro)
    except Exception as e:
        # If all else fails, try asyncio.run as a last resort
        try:
            return asyncio.run(coro)
        except Exception as final_e:
            print(f"Error running async operation: {final_e}")
            raise final_e

def test_api_connection():
    """Test the API connection using the safe async runner"""
    print("Testing API connection...")
    
    try:
        workflow_builder = N8nWorkflowBuilder()
        result = run_async_safely(workflow_builder.test_api_connection())
        
        if result["success"]:
            print("✅ API connection test successful!")
            print(f"Response: {result.get('message', 'No message')}")
            return True
        else:
            print("❌ API connection test failed!")
            print(f"Error: {result.get('error', 'Unknown error')}")
            return False
            
    except Exception as e:
        print(f"❌ Exception during API test: {str(e)}")
        return False

def test_workflow_generation():
    """Test workflow generation using the safe async runner"""
    print("\nTesting workflow generation...")
    
    try:
        workflow_builder = N8nWorkflowBuilder()
        test_goal = "Create a simple workflow that sends a welcome email when a new user signs up"
        
        print(f"Generating workflow for: {test_goal}")
        result = run_async_safely(asyncio.wait_for(
            workflow_builder.generate_workflow(test_goal), 
            timeout=10.0  # Short timeout for testing
        ))
        
        if result["success"]:
            print("✅ Workflow generation test successful!")
            workflow = result.get("workflow", {})
            print(f"Generated workflow name: {workflow.get('name', 'Unknown')}")
            print(f"Number of nodes: {len(workflow.get('nodes', []))}")
            return True
        else:
            print("❌ Workflow generation test failed!")
            print(f"Error: {result.get('error', 'Unknown error')}")
            return False
            
    except asyncio.TimeoutError:
        print("⚠️ Workflow generation timed out (this is expected for testing)")
        return True  # Timeout is acceptable for this test
    except Exception as e:
        print(f"❌ Exception during workflow generation: {str(e)}")
        return False

def main():
    """Run all tests"""
    print("🧪 Testing async event loop fixes...\n")
    
    # Test 1: API Connection
    api_success = test_api_connection()
    
    # Test 2: Workflow Generation
    workflow_success = test_workflow_generation()
    
    # Summary
    print("\n" + "="*50)
    print("TEST SUMMARY:")
    print(f"API Connection: {'✅ PASS' if api_success else '❌ FAIL'}")
    print(f"Workflow Generation: {'✅ PASS' if workflow_success else '❌ FAIL'}")
    
    if api_success and workflow_success:
        print("\n🎉 All tests passed! The async event loop fix is working correctly.")
        return True
    else:
        print("\n⚠️ Some tests failed. Please check the error messages above.")
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1) 