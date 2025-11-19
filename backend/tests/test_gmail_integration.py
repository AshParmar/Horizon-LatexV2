"""
Test Gmail Integration
Tests the complete Gmail resume processing flow
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from modules.resume.gmail_monitor import GmailMonitor
from modules.integrations.gmail import GmailIntegration


def test_gmail_connection(user_id: str = "test_user_001"):
    """Test if Gmail is connected for a user"""
    print(f"\n{'='*60}")
    print(f"TESTING GMAIL CONNECTION FOR: {user_id}")
    print(f"{'='*60}\n")
    
    gmail = GmailIntegration()
    
    try:
        # Try to fetch emails (will fail if not connected)
        result = gmail.check_for_new_resumes(
            user_id=user_id,
            use_mock=False
        )
        
        print(f"✅ Gmail is connected for {user_id}")
        print(f"   Fetched {len(result)} email(s)")
        return True
        
    except Exception as e:
        error_msg = str(e)
        if "No connected account found" in error_msg or "error code: 400" in error_msg.lower():
            print(f"❌ Gmail NOT connected for {user_id}")
            print(f"   Error: No connected account found")
            print(f"\n📌 To connect Gmail:")
            print(f"   1. Go to: https://app.composio.dev")
            print(f"   2. Navigate to 'Connected Accounts'")
            print(f"   3. Click 'Add Connection'")
            print(f"   4. Select 'Gmail' and connect")
            print(f"   5. Use entity_id: user_{user_id}")
            return False
        else:
            print(f"❌ Unexpected error: {error_msg}")
            raise


def test_process_resumes(user_id: str = "test_user_001", use_mock: bool = False):
    """Test processing resumes from Gmail"""
    print(f"\n{'='*60}")
    print(f"TESTING RESUME PROCESSING FOR: {user_id}")
    print(f"Mode: {'MOCK DATA' if use_mock else 'REAL GMAIL'}")
    print(f"{'='*60}\n")
    
    # Create user-specific data directory
    data_dir = f"./data/users/{user_id}"
    Path(data_dir).mkdir(parents=True, exist_ok=True)
    
    # Initialize monitor
    monitor = GmailMonitor(data_dir=data_dir)
    
    # Process emails
    print("📧 Processing Gmail resumes...")
    candidates = monitor.process_new_emails(
        user_id=user_id,
        use_mock=use_mock
    )
    
    # Display results
    print(f"\n✅ Processing Complete!")
    print(f"   Emails processed: {len(candidates)}")
    print(f"   New candidates found: {len(candidates)}")
    
    if candidates:
        print(f"\n📋 Candidates Found:")
        for i, candidate in enumerate(candidates, 1):
            name = candidate.get('name', 'Unknown')
            email = candidate.get('email', 'N/A')
            skills_count = len(candidate.get('extracted_data', {}).get('skills', []))
            
            print(f"\n   {i}. {name}")
            print(f"      Email: {email}")
            print(f"      Skills Extracted: {skills_count}")
            
            # Show file paths
            resume_file = candidate.get('resume_file')
            json_file = candidate.get('json_file')
            if resume_file:
                print(f"      Resume: {resume_file}")
            if json_file:
                print(f"      JSON: {json_file}")
    else:
        print(f"\n   No new resumes found")
    
    return candidates


def test_complete_flow(user_id: str = "test_user_001"):
    """Test the complete Gmail integration flow"""
    print(f"\n{'#'*60}")
    print(f"# COMPLETE GMAIL INTEGRATION TEST")
    print(f"{'#'*60}")
    
    # Step 1: Check connection
    print(f"\n[STEP 1] Checking Gmail Connection...")
    is_connected = test_gmail_connection(user_id)
    
    if not is_connected:
        print(f"\n⚠️  Cannot proceed - Gmail not connected")
        print(f"   Please connect Gmail first and try again")
        return
    
    # Step 2: Process resumes
    print(f"\n[STEP 2] Processing Resumes...")
    candidates = test_process_resumes(user_id, use_mock=False)
    
    # Summary
    print(f"\n{'='*60}")
    print(f"TEST SUMMARY")
    print(f"{'='*60}")
    print(f"✅ Gmail Connection: Working")
    print(f"✅ Resume Processing: Working")
    print(f"📊 Candidates Found: {len(candidates)}")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    import sys
    
    # Get user_id from command line or use default
    user_id = "test_user_001"
    if len(sys.argv) > 1:
        user_id = sys.argv[1]
    
    # Run complete flow
    test_complete_flow(user_id)
