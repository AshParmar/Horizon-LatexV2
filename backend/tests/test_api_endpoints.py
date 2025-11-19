"""
Test API Endpoints
Tests all Gmail integration API endpoints
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

import requests
import json


BASE_URL = "http://localhost:8000/api/v1"


def test_check_status(user_id: str = "test_user_001"):
    """Test the Gmail status check endpoint"""
    print(f"\n{'='*60}")
    print(f"TEST: Check Gmail Status")
    print(f"{'='*60}")
    
    url = f"{BASE_URL}/integrations/gmail/status/{user_id}"
    print(f"GET {url}")
    
    try:
        response = requests.get(url)
        data = response.json()
        
        print(f"\nStatus Code: {response.status_code}")
        print(f"Response:")
        print(json.dumps(data, indent=2))
        
        if data.get('connected'):
            print(f"\n✅ Gmail is connected for {user_id}")
        else:
            print(f"\n❌ Gmail NOT connected for {user_id}")
        
        return data
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return None


def test_get_connect_url():
    """Test the Gmail connection URL endpoint"""
    print(f"\n{'='*60}")
    print(f"TEST: Get Connection URL")
    print(f"{'='*60}")
    
    url = f"{BASE_URL}/integrations/gmail/connect-url"
    print(f"GET {url}")
    
    try:
        response = requests.get(url)
        data = response.json()
        
        print(f"\nStatus Code: {response.status_code}")
        print(f"Response:")
        print(json.dumps(data, indent=2))
        
        print(f"\n📌 Connection Instructions:")
        print(f"   {data.get('instructions', '').split('To connect Gmail:')[1] if 'To connect Gmail:' in data.get('instructions', '') else data.get('instructions', '')}")
        
        return data
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return None


def test_process_resumes(user_id: str = "test_user_001", use_mock: bool = False):
    """Test the process resumes endpoint"""
    print(f"\n{'='*60}")
    print(f"TEST: Process Gmail Resumes")
    print(f"{'='*60}")
    
    url = f"{BASE_URL}/integrations/gmail/process-resumes"
    payload = {
        "user_id": user_id,
        "use_mock": use_mock
    }
    
    print(f"POST {url}")
    print(f"Payload: {json.dumps(payload, indent=2)}")
    
    try:
        response = requests.post(url, json=payload)
        data = response.json()
        
        print(f"\nStatus Code: {response.status_code}")
        
        if response.status_code == 400:
            print(f"\n❌ Error: {data.get('detail', {}).get('message', 'Unknown error')}")
            print(f"   {data.get('detail', {}).get('error', '')}")
            return None
        
        print(f"Response:")
        print(json.dumps(data, indent=2))
        
        candidates_found = data.get('candidates_found', 0)
        print(f"\n✅ Processed successfully!")
        print(f"   Candidates found: {candidates_found}")
        
        if candidates_found > 0:
            print(f"\n📋 Candidates:")
            for i, candidate in enumerate(data.get('candidates', []), 1):
                print(f"   {i}. {candidate.get('name', 'Unknown')}")
                print(f"      Email: {candidate.get('email', 'N/A')}")
        
        return data
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return None


def test_all_endpoints(user_id: str = "test_user_001"):
    """Test all Gmail API endpoints"""
    print(f"\n{'#'*60}")
    print(f"# GMAIL API ENDPOINTS TEST")
    print(f"{'#'*60}")
    
    # Check if server is running
    try:
        response = requests.get("http://localhost:8000")
        print(f"\n✅ Server is running at http://localhost:8000")
    except:
        print(f"\n❌ Server is NOT running!")
        print(f"   Please start the server first:")
        print(f"   uvicorn main:app --reload")
        return
    
    # Test 1: Check Status
    print(f"\n[TEST 1] Check Gmail Status")
    status = test_check_status(user_id)
    
    # Test 2: Get Connection URL
    print(f"\n[TEST 2] Get Connection URL")
    connect_url = test_get_connect_url()
    
    # Test 3: Process Resumes (only if connected)
    if status and status.get('connected'):
        print(f"\n[TEST 3] Process Resumes (Real Gmail)")
        result = test_process_resumes(user_id, use_mock=False)
    else:
        print(f"\n[TEST 3] Process Resumes (Mock Data - user not connected)")
        result = test_process_resumes(user_id, use_mock=True)
    
    # Summary
    print(f"\n{'='*60}")
    print(f"TEST SUMMARY")
    print(f"{'='*60}")
    print(f"✅ Status Check: {'Working' if status else 'Failed'}")
    print(f"✅ Get Connect URL: {'Working' if connect_url else 'Failed'}")
    print(f"✅ Process Resumes: {'Working' if result else 'Failed'}")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    import sys
    
    # Get user_id from command line or use default
    user_id = "test_user_001"
    if len(sys.argv) > 1:
        user_id = sys.argv[1]
    
    # Run all tests
    test_all_endpoints(user_id)
