"""
Test Mock Data
Tests the system with mock data (no Gmail connection required)
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from modules.resume.gmail_monitor import GmailMonitor


def test_with_mock_data():
    """Test the complete flow with mock data"""
    print(f"\n{'='*60}")
    print(f"TESTING WITH MOCK DATA (No Gmail Required)")
    print(f"{'='*60}\n")
    
    # Create test data directory
    data_dir = "./data/users/mock_test_user"
    Path(data_dir).mkdir(parents=True, exist_ok=True)
    
    # Initialize monitor
    monitor = GmailMonitor(data_dir=data_dir)
    
    # Process with mock data
    print("📧 Processing mock resume emails...")
    candidates = monitor.process_new_emails(
        user_id="mock_test_user",
        use_mock=True
    )
    
    # Display results
    print(f"\n✅ Processing Complete!")
    print(f"   Mock emails processed: {len(candidates)}")
    print(f"   Candidates created: {len(candidates)}")
    
    if candidates:
        print(f"\n📋 Mock Candidates:")
        for i, candidate in enumerate(candidates, 1):
            name = candidate.get('name', 'Unknown')
            email = candidate.get('email', 'N/A')
            skills = candidate.get('extracted_data', {}).get('skills', [])
            enriched_skills = candidate.get('enriched_data', {}).get('ai_inferred_skills', [])
            
            print(f"\n   {i}. {name}")
            print(f"      Email: {email}")
            print(f"      Extracted Skills: {len(skills)}")
            print(f"      Enriched Skills: {len(enriched_skills)}")
            
            if skills:
                print(f"      Top Skills: {', '.join(skills[:5])}")
    
    print(f"\n{'='*60}")
    print(f"Mock data test completed successfully!")
    print(f"{'='*60}\n")
    
    return candidates


if __name__ == "__main__":
    test_with_mock_data()
