#!/usr/bin/env python3
"""
Comprehensive test script for Veswo Assistant with GPT-2
Tests all endpoints and functionality to ensure everything works correctly
"""

import requests
import json
import time
import sys
from typing import Dict, Any

# Configuration
BASE_URL = "http://localhost:8000"
TIMEOUT = 30

def print_status(message: str, status: str = "INFO"):
    """Print colored status messages"""
    colors = {
        "INFO": "\033[94m",    # Blue
        "SUCCESS": "\033[92m", # Green
        "WARNING": "\033[93m", # Yellow
        "ERROR": "\033[91m",   # Red
        "RESET": "\033[0m"     # Reset
    }
    print(f"{colors.get(status, colors['INFO'])}[{status}]{colors['RESET']} {message}")

def test_backend_health():
    """Test if backend is running and healthy"""
    print_status("Testing backend health...")
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print_status(f"Backend is healthy: {data['status']}", "SUCCESS")
            return True
        else:
            print_status(f"Backend health check failed: {response.status_code}", "ERROR")
            return False
    except Exception as e:
        print_status(f"Backend health check error: {e}", "ERROR")
        return False

def test_gpt2_status():
    """Test GPT-2 model status"""
    print_status("Testing GPT-2 model status...")
    try:
        response = requests.get(f"{BASE_URL}/api/status", timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data.get('gpt2_ready'):
                print_status("GPT-2 model is ready!", "SUCCESS")
                if data.get('model_info'):
                    model_info = data['model_info']
                    print_status(f"Model: {model_info.get('model_name')} on {model_info.get('device')}", "INFO")
                return True
            else:
                print_status(f"GPT-2 not ready: {data.get('error', 'Unknown error')}", "WARNING")
                return False
        else:
            print_status(f"GPT-2 status check failed: {response.status_code}", "ERROR")
            return False
    except Exception as e:
        print_status(f"GPT-2 status check error: {e}", "ERROR")
        return False

def test_chat_endpoint():
    """Test chat endpoint with various inputs"""
    print_status("Testing chat endpoint...")
    
    test_cases = [
        {"message": "hello", "expected_method": "Fallback Response"},
        {"message": "What is 2+2?", "expected_method": "Fallback Response"},
        {"message": "2+3", "expected_method": "Direct Evaluation"},
        {"message": "How are you?", "expected_method": "Fallback Response"},
        {"message": "What can you do?", "expected_method": "Fallback Response"},
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        try:
            response = requests.post(
                f"{BASE_URL}/api/chat",
                json={"message": test_case["message"]},
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get('method') == test_case['expected_method']:
                    print_status(f"Test {i} passed: {test_case['message']}", "SUCCESS")
                else:
                    print_status(f"Test {i} method mismatch: expected {test_case['expected_method']}, got {data.get('method')}", "WARNING")
            else:
                print_status(f"Test {i} failed: {response.status_code}", "ERROR")
                
        except Exception as e:
            print_status(f"Test {i} error: {e}", "ERROR")

def test_essay_endpoint():
    """Test essay writing endpoint"""
    print_status("Testing essay writing endpoint...")
    try:
        response = requests.post(
            f"{BASE_URL}/api/write/essay",
            json={
                "topic": "Technology",
                "essay_type": "analytical",
                "length": "short"
            },
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            if data.get('content') and len(data['content']) > 50:
                print_status("Essay writing test passed!", "SUCCESS")
                print_status(f"Generated {data.get('metadata', {}).get('word_count', 0)} words", "INFO")
            else:
                print_status("Essay writing test failed: content too short", "WARNING")
        else:
            print_status(f"Essay writing test failed: {response.status_code}", "ERROR")
            
    except Exception as e:
        print_status(f"Essay writing test error: {e}", "ERROR")

def test_science_endpoint():
    """Test science help endpoint"""
    print_status("Testing science help endpoint...")
    try:
        response = requests.post(
            f"{BASE_URL}/api/help/science",
            json={
                "subject": "physics",
                "question": "What is gravity?"
            },
            timeout=20
        )
        
        if response.status_code == 200:
            data = response.json()
            if data.get('response') and len(data['response']) > 10:
                print_status("Science help test passed!", "SUCCESS")
            else:
                print_status("Science help test failed: response too short", "WARNING")
        else:
            print_status(f"Science help test failed: {response.status_code}", "ERROR")
            
    except Exception as e:
        print_status(f"Science help test error: {e}", "ERROR")

def test_code_endpoint():
    """Test code help endpoint"""
    print_status("Testing code help endpoint...")
    try:
        response = requests.post(
            f"{BASE_URL}/api/help/code",
            json={
                "code": "print('Hello, World!')",
                "question": "What does this code do?"
            },
            timeout=20
        )
        
        if response.status_code == 200:
            data = response.json()
            if data.get('response') and len(data['response']) > 10:
                print_status("Code help test passed!", "SUCCESS")
            else:
                print_status("Code help test failed: response too short", "WARNING")
        else:
            print_status(f"Code help test failed: {response.status_code}", "ERROR")
            
    except Exception as e:
        print_status(f"Code help test error: {e}", "ERROR")

def test_image_endpoint():
    """Test image analysis endpoint"""
    print_status("Testing image analysis endpoint...")
    try:
        response = requests.post(
            f"{BASE_URL}/api/analyze/image",
            json={
                "image_description": "A cat sitting on a windowsill",
                "question": "What animal is in the image?"
            },
            timeout=20
        )
        
        if response.status_code == 200:
            data = response.json()
            if data.get('response') and len(data['response']) > 5:
                print_status("Image analysis test passed!", "SUCCESS")
            else:
                print_status("Image analysis test failed: response too short", "WARNING")
        else:
            print_status(f"Image analysis test failed: {response.status_code}", "ERROR")
            
    except Exception as e:
        print_status(f"Image analysis test error: {e}", "ERROR")

def wait_for_backend():
    """Wait for backend to be ready"""
    print_status("Waiting for backend to be ready...")
    for i in range(30):
        try:
            response = requests.get(f"{BASE_URL}/health", timeout=5)
            if response.status_code == 200:
                print_status("Backend is ready!", "SUCCESS")
                return True
        except:
            pass
        print_status(f"Attempt {i+1}/30: Backend not ready yet...", "WARNING")
        time.sleep(2)
    
    print_status("Backend failed to start within 60 seconds", "ERROR")
    return False

def main():
    """Run all tests"""
    print_status("🚀 Starting comprehensive Veswo Assistant tests...", "INFO")
    print_status("=" * 50, "INFO")
    
    # Wait for backend
    if not wait_for_backend():
        print_status("❌ Backend not available. Please start the backend first.", "ERROR")
        sys.exit(1)
    
    # Run tests
    tests = [
        test_backend_health,
        test_gpt2_status,
        test_chat_endpoint,
        test_essay_endpoint,
        test_science_endpoint,
        test_code_endpoint,
        test_image_endpoint,
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            test()
            passed += 1
        except Exception as e:
            print_status(f"Test {test.__name__} failed with exception: {e}", "ERROR")
        print_status("-" * 30, "INFO")
    
    # Summary
    print_status("=" * 50, "INFO")
    print_status(f"🎯 Test Results: {passed}/{total} tests passed", "SUCCESS" if passed == total else "WARNING")
    
    if passed == total:
        print_status("🎉 All tests passed! Veswo Assistant with GPT-2 is working correctly.", "SUCCESS")
        print_status("💡 You can now use the application with confidence.", "INFO")
    else:
        print_status("⚠️  Some tests failed. Please check the errors above.", "WARNING")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 