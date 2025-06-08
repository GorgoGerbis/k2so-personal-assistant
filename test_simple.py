#!/usr/bin/env python3
"""
Simple test script for K2SO test models
This demonstrates how to use testLocal and testRemote without full setup
"""

import sys
import os
import time

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

# Import what we need
from components.local_model import LocalModel
from components.remote_model import RemoteModel
from test_conversations import TestConversations

def test_local_model():
    """Test the local model with predefined conversations"""
    print("=== Testing Local Model ===")
    print("This simulates running 'testLocal' model")
    print()
    
    # Create test local model (empty path triggers test mode)
    model = LocalModel("")
    
    # Simulate a conversation
    test_inputs = [
        "Hello K2SO",
        "What can you do?", 
        "Tell me a joke",
        "What's the weather like?",
        "Goodbye"
    ]
    
    for user_input in test_inputs:
        print(f"You: {user_input}")
        response = model.generate_response(user_input)
        print(f"K2SO: {response}")
        print()
        time.sleep(1)  # Pause between responses

def test_remote_model():
    """Test the remote model with predefined conversations"""
    print("=== Testing Remote Model ===")
    print("This simulates running 'testRemote' model")
    print()
    
    # Create test remote model
    test_config = {
        "url": "http://test-server/chat",  # Contains "test" so triggers test mode
        "api_key_env": None
    }
    model = RemoteModel(test_config)
    
    # Simulate a conversation
    test_inputs = [
        "Hello K2SO",
        "What are your capabilities?",
        "Tell me something funny", 
        "Check the weather",
        "Farewell"
    ]
    
    for user_input in test_inputs:
        print(f"You: {user_input}")
        response = model.generate_response(user_input)
        print(f"K2SO: {response}")
        print()
        time.sleep(1)  # Pause between responses

def main():
    print("K2SO Test Models Demo")
    print("=" * 40)
    print()
    print("This script shows how the testLocal and testRemote models work")
    print("with predefined conversations from test_conversations.py")
    print()
    
    while True:
        print("Choose a test:")
        print("1. Test Local Model (testLocal)")
        print("2. Test Remote Model (testRemote)")
        print("3. Exit")
        
        choice = input("\nEnter choice (1-3): ").strip()
        
        if choice == "1":
            test_local_model()
        elif choice == "2":
            test_remote_model()
        elif choice == "3":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")
        
        print("\n" + "="*40 + "\n")

if __name__ == "__main__":
    main() 