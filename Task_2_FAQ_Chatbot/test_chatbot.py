#!/usr/bin/env python3
"""
Test script for CodeAlpha FAQ Chatbot
"""

import requests
import json

def test_chatbot():
    """Test the FAQ chatbot with various questions"""
    base_url = "http://localhost:5000"
    
    test_questions = [
        "What is CodeAlpha?",
        "How long is the internship program?",
        "What are the requirements?",
        "Is it paid or unpaid?",
        "Can I work remotely?",
        "What is machine learning?",
        "How do I apply?",
        "What is the weather today?",  # Should not match
        "Tell me about pizza",  # Should not match
    ]
    
    print("🤖 Testing CodeAlpha FAQ Chatbot")
    print("=" * 50)
    
    for i, question in enumerate(test_questions, 1):
        try:
            response = requests.post(
                f"{base_url}/chat",
                json={"message": question},
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                data = response.json()
                confidence = data.get('confidence', 0)
                answer = data.get('response', 'No response')
                
                print(f"\n{i}. Question: {question}")
                print(f"   Confidence: {confidence:.2f}")
                print(f"   Answer: {answer[:100]}{'...' if len(answer) > 100 else ''}")
                
            else:
                print(f"\n{i}. Question: {question}")
                print(f"   Error: HTTP {response.status_code}")
                
        except requests.exceptions.ConnectionError:
            print(f"\n{i}. Question: {question}")
            print("   Error: Could not connect to server. Make sure Flask app is running.")
            break
        except Exception as e:
            print(f"\n{i}. Question: {question}")
            print(f"   Error: {str(e)}")
    
    print("\n" + "=" * 50)
    print("✅ Test completed!")

if __name__ == "__main__":
    test_chatbot()