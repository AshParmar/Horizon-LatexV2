# Backend Tests

This folder contains test scripts for the Gmail integration system.

## Test Files

### 1. `test_gmail_integration.py`
**Purpose:** Test complete Gmail integration flow
- Check Gmail connection status
- Process real Gmail resumes
- Display candidate results

**Usage:**
```bash
# Test with default user (test_user_001)
python tests/test_gmail_integration.py

# Test with specific user
python tests/test_gmail_integration.py your_user_id
```

**Requirements:** Gmail must be connected for the user

---

### 2. `test_api_endpoints.py`
**Purpose:** Test all REST API endpoints
- GET /gmail/status/{user_id}
- GET /gmail/connect-url
- POST /gmail/process-resumes

**Usage:**
```bash
# Make sure server is running first
uvicorn main:app --reload

# Then in another terminal:
python tests/test_api_endpoints.py

# Test specific user
python tests/test_api_endpoints.py your_user_id
```

**Requirements:** FastAPI server must be running

---

### 3. `test_mock_data.py`
**Purpose:** Test system with mock data (no Gmail needed)
- Tests with sample resume data
- No Gmail connection required
- Good for initial testing

**Usage:**
```bash
python tests/test_mock_data.py
```

**Requirements:** None - works without Gmail

---

## Quick Test Commands

```bash
# Activate environment
zon\Scripts\activate

# Test 1: Mock data (easiest, no setup needed)
python tests/test_mock_data.py

# Test 2: Gmail integration (requires Gmail connection)
python tests/test_gmail_integration.py

# Test 3: API endpoints (requires running server)
# Terminal 1:
uvicorn main:app --reload

# Terminal 2:
python tests/test_api_endpoints.py
```

---

## Expected Output Examples

### Mock Data Test:
```
✅ Processing Complete!
   Mock emails processed: 3
   Candidates created: 3

📋 Mock Candidates:
   1. Alice Johnson
      Email: alice@example.com
      Extracted Skills: 12
      Enriched Skills: 8
```

### Gmail Integration Test:
```
✅ Gmail is connected for test_user_001
   Fetched 1 email(s)

✅ Processing Complete!
   Emails processed: 1
   New candidates found: 1

📋 Candidates Found:
   1. Ashish Kumar
      Email: ashparmar08@gmail.com
      Skills Extracted: 17
```

### API Endpoints Test:
```
✅ Server is running at http://localhost:8000

[TEST 1] Check Gmail Status
Status Code: 200
✅ Gmail is connected for test_user_001

[TEST 2] Get Connection URL
Status Code: 200

[TEST 3] Process Resumes
✅ Processed successfully!
   Candidates found: 1
```

---

## Troubleshooting

### Gmail Not Connected Error
```
❌ Gmail NOT connected for test_user_001

📌 To connect Gmail:
   1. Go to: https://app.composio.dev
   2. Navigate to 'Connected Accounts'
   3. Click 'Add Connection'
   4. Select 'Gmail' and connect
   5. Use entity_id: user_test_user_001
```

**Solution:** Follow the instructions to connect Gmail

### Server Not Running Error
```
❌ Server is NOT running!
   Please start the server first:
   uvicorn main:app --reload
```

**Solution:** Start the FastAPI server in a separate terminal

### Import Errors
**Solution:** Make sure you're in the backend directory and environment is activated
```bash
cd backend
zon\Scripts\activate
```

---

## Adding New Tests

To add a new test file:

1. Create file in `tests/` folder
2. Add path setup at top:
```python
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
```

3. Import modules you need to test
4. Create test functions with clear output
5. Update this README with usage instructions
