import os
import sys
import traceback
from typing import Dict, Any
from agent_controler import AgentController


def main(inputs: Dict[str, Any]) -> Dict[str, Any]:
    """
    Main function for Hugging Face API deployment.
    
    Args:
        inputs: Dictionary containing the input data from Hugging Face API
                Expected format: {"input": {"messages": [{"role": "user", "content": "message"}]}}
    
    Returns:
        Dictionary with the response in Hugging Face expected format
    """
    try:
        # Initialize the agent controller
        agent_controller = AgentController()
        
        # Validate input format
        if not isinstance(inputs, dict):
            return {
                "error": "Invalid input format. Expected dictionary.",
                "status": "error"
            }
        
        if "input" not in inputs:
            return {
                "error": "Missing 'input' key in request data.",
                "status": "error"
            }
        
        if "messages" not in inputs["input"]:
            return {
                "error": "Missing 'messages' key in input data.",
                "status": "error"
            }
        
        # Validate messages format
        messages = inputs["input"]["messages"]
        if not isinstance(messages, list) or len(messages) == 0:
            return {
                "error": "Messages must be a non-empty list.",
                "status": "error"
            }
        
        # Validate message structure
        for i, message in enumerate(messages):
            if not isinstance(message, dict):
                return {
                    "error": f"Message {i} must be a dictionary.",
                    "status": "error"
                }
            if "role" not in message or "content" not in message:
                return {
                    "error": f"Message {i} must have 'role' and 'content' keys.",
                    "status": "error"
                }
            if message["role"] not in ["user", "assistant"]:
                return {
                    "error": f"Message {i} role must be 'user' or 'assistant'.",
                    "status": "error"
                }
        
        # Get response from agent controller
        response = agent_controller.get_response(inputs)
        
        # Validate response format
        if not isinstance(response, dict):
            return {
                "error": "Agent controller returned invalid response format.",
                "status": "error"
            }
        
        # Ensure response has required fields
        if "role" not in response or "content" not in response:
            return {
                "error": "Agent response missing required fields.",
                "status": "error"
            }
        
        # Return in Hugging Face expected format
        return {
            "generated_text": response["content"],
            "role": response["role"],
            "memory": response.get("memory", {}),
            "status": "success"
        }
        
    except FileNotFoundError as e:
        error_msg = f"Required file not found: {str(e)}"
        print(f"ERROR: {error_msg}")
        return {
            "error": error_msg,
            "status": "error",
            "suggestion": "Check if recommendation files exist in the correct path"
        }
        
    except ValueError as e:
        error_msg = f"Configuration error: {str(e)}"
        print(f"ERROR: {error_msg}")
        return {
            "error": error_msg,
            "status": "error",
            "suggestion": "Check environment variables (BASE_URL, HF_TOKEN, MODEL_NAME, PINECONE_API_KEY, etc.)"
        }
        
    except Exception as e:
        error_msg = f"Unexpected error: {str(e)}"
        print(f"ERROR: {error_msg}")
        print("TRACEBACK:")
        traceback.print_exc()
        
        return {
            "error": error_msg,
            "status": "error",
            "traceback": traceback.format_exc()
        }





if __name__ == "__main__":
    # Test the main function with sample data when run directly
    print("Testing main function...")
    
    sample_inputs = [
        {
            "input": {
                "messages": [
                    {"role": "user", "content": "I would like one Latte please"}
                ]
            }
        },
        {
            "input": {
                "messages": [
                    {"role": "user", "content": "What are your working hours?"}
                ]
            }
        },
        {
            "input": {
                "messages": [
                    {"role": "user", "content": "Can you recommend something?"}
                ]
            }
        }
    ]
    
    


       
    sample_inputs1=[{"input": {"messages": [{"role":"user","content": "I would like one Latte please"}]}}]
    
    print("\n=== TESTING SAMPLE INPUTS ===")
    for i, sample_input in enumerate(sample_inputs, 1):
        print(f"\n--- Test {i} ---")
        print(f"Input: {sample_input}")
        
        result = main(sample_input)
        print(f"Output: {result}")
        
        if result.get("status") == "success":
            print(f"✅ Test {i} passed")
        else:
            print(f"❌ Test {i} failed: {result.get('error', 'Unknown error')}")