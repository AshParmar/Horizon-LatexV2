# ✅ Gmail Pipeline - Quick Reference

## 🎯 What You Have Now

### **Complete Working System:**

```
Gmail Inbox
    ↓
  📧 Resume emails detected
    ↓
  📥 PDF/DOCX downloaded → ./data/resumes/
    ↓
  🔍 Extract: name, email, skills, experience
    ↓
  🤖 AI Enrich: Google Gemini adds more skills
    ↓
  📝 Format: Standard JSON structure
    ↓
  💾 Save → ./data/candidates/{email}.json
    ↓
  ✅ Ready for scoring!
```

---

## 🚀 Quick Start

### **1. Activate Environment**
```bash
zon\Scripts\activate
cd backend
```

### **2. Start Server (Automatic Processing)**
```bash
uvicorn main:app --reload
```
✅ Cron job runs every 15 minutes automatically!

### **3. Manual Test**
```bash
# Test with real Gmail
python tests/test_gmail_integration.py

# Test with mock data (no Gmail needed)
python tests/test_mock_data.py
```

---

## 📡 API Endpoints

### **Check Gmail Status**
```bash
GET /api/v1/integrations/gmail/status/{user_id}
```

### **Process Resumes Manually**
```bash
POST /api/v1/integrations/gmail/process-resumes
Body: {"user_id": "test_user_001", "use_mock": false}
```

### **Get Connection Instructions**
```bash
GET /api/v1/integrations/gmail/connect-url
```

---

## 📊 Latest Test Results

```
✅ Gmail Connection: Working
✅ Resume Processing: Working
📊 Candidates Found: 1

Test Candidate:
- Name: Ashish Kumar
- Email: ashparmar08@gmail.com
- Source: Real Gmail (ashparmar08@gmail.com)
- File: Ashish_Kumar_team_IGNIITTE.pdf
- Status: ✅ Processed Successfully
```

---

## 🔧 Key Files

```
backend/
├── modules/
│   ├── integrations/
│   │   └── gmail.py                    # Gmail API integration
│   └── resume/
│       ├── gmail_monitor.py            # Pipeline orchestrator
│       ├── extractor.py                # Extract resume data
│       ├── enricher.py                 # AI enrichment
│       └── formatter.py                # Format JSON output
├── api/
│   └── integrations.py                 # REST API endpoints
├── tasks/
│   └── scheduler.py                    # Cron job (every 15 min)
└── tests/
    ├── test_gmail_integration.py       # Main integration test
    ├── test_api_endpoints.py           # API tests
    └── test_mock_data.py               # Mock data test
```

---

## 📈 What Works

| Feature | Status | Notes |
|---------|--------|-------|
| Gmail Connection | ✅ | Via Composio OAuth |
| Email Fetching | ✅ | Last 7 days, with attachments |
| File Download | ✅ | PDF, DOCX, TXT supported |
| Data Extraction | ✅ | Name, email, phone, skills, etc. |
| AI Enrichment | ✅ | Google Gemini API |
| JSON Formatting | ✅ | Standard structure |
| Multi-User | ✅ | Different Gmail accounts |
| REST API | ✅ | 3 endpoints ready |
| Cron Job | ✅ | Auto-runs every 15 min |
| Error Handling | ✅ | Graceful fallbacks |

---

## 🎓 How It Works

### **Step 1: Gmail Fetch**
```python
# Composio connects to Gmail
# Searches: "has:attachment newer_than:7d"
# Downloads: PDF, DOCX, TXT files
```

### **Step 2: Extraction**
```python
# Reads file content (PyPDF2/python-docx)
# Parses with regex + patterns
# Extracts: name, email, phone, skills, experience, education
```

### **Step 3: AI Enrichment**
```python
# Sends skills to Google Gemini
# Prompt: "Infer additional skills based on these..."
# Returns: More skills, categories, proficiency levels
```

### **Step 4: Save**
```python
# Merges extracted + enriched data
# Formats as standard JSON
# Saves to ./data/candidates/
```

---

## 🧪 Testing

### **Test 1: Mock Data (No Gmail Needed)**
```bash
python tests/test_mock_data.py
```
✅ Creates 3 sample candidates  
✅ Tests full pipeline without Gmail

### **Test 2: Real Gmail**
```bash
python tests/test_gmail_integration.py
```
✅ Connects to Gmail  
✅ Processes real resumes  
✅ Shows results

### **Test 3: API Endpoints**
```bash
# Terminal 1: Start server
uvicorn main:app --reload

# Terminal 2: Test APIs
python tests/test_api_endpoints.py
```
✅ Tests all 3 endpoints  
✅ Verifies responses

---

## 🔄 Automatic Processing

When server is running, check logs every 15 minutes:

```
INFO: Checking Gmail for new resume emails...
INFO: Checking Gmail for user: test_user_001
INFO: Found 1 email(s) with attachments
INFO: ✅ Downloaded resume: candidate.pdf from candidate@email.com
INFO: Successfully downloaded 1 resume files
INFO: Processing resume email: Application for Software Engineer
INFO: Step 1: Extraction...
INFO: Step 2: Enrichment...
INFO: Step 3: Formatting...
INFO: Successfully processed candidate: John Doe (ID: john_doe_at_email_com)
INFO: Gmail check completed. Total new candidates: 1
```

---

## 📝 Output Format

```json
{
  "name": "Ashish Kumar",
  "email": "ashparmar08@gmail.com",
  "phone": "+91-XXXXXXXXXX",
  "extracted_data": {
    "skills": [
      "Python", "FastAPI", "React", "Docker", "AWS",
      "PostgreSQL", "Redis", "Git", "CI/CD", "REST API"
    ],
    "experience": [
      {
        "company": "TechCorp",
        "position": "Senior Software Engineer",
        "duration": "2020-Present",
        "description": "..."
      }
    ],
    "education": [
      {
        "degree": "BS Computer Science",
        "institution": "MIT",
        "year": "2019"
      }
    ]
  },
  "enriched_data": {
    "ai_inferred_skills": [
      "JavaScript", "TypeScript", "Node.js", "GraphQL",
      "Microservices", "Kubernetes", "DevOps"
    ],
    "skill_categories": {
      "technical": [...],
      "soft_skills": [...],
      "domain_knowledge": [...]
    }
  },
  "metadata": {
    "processed_at": "2025-11-18T10:30:00",
    "source": "gmail",
    "resume_file": "./data/resumes/ashish_resume.pdf",
    "source_email": "msg_12345",
    "sender": "ashparmar08@gmail.com"
  }
}
```

---

## 🎯 Next Steps

### **For Scoring (Person 5):**
- Read candidate JSON from `./data/candidates/`
- Compare against job descriptions
- Calculate match scores
- Rank candidates

### **For Frontend:**
- Use API endpoints to trigger processing
- Display candidate list
- Show processing status
- Download resume files

---

## 💡 Tips

**✅ Good:**
- Let cron job run automatically (every 15 min)
- Use mock data for initial testing
- Check logs for processing details

**❌ Avoid:**
- Don't run tests too frequently (Gmail API rate limits)
- Don't process same email twice (already handled)
- Don't forget to activate environment first

---

## 🆘 Troubleshooting

### Problem: Gmail not connected
```
❌ Gmail NOT connected for test_user_001
```
**Solution:** Go to https://app.composio.dev and connect Gmail with entity_id: user_test_user_001

### Problem: No resumes found
```
📧 Processing Gmail resumes...
✅ Processing Complete!
   Emails processed: 0
```
**Solution:** 
- Send test resume to connected Gmail
- Or use mock data: `use_mock=True`

### Problem: Import errors
```
ModuleNotFoundError: No module named 'composio'
```
**Solution:** 
```bash
zon\Scripts\activate
pip install -r requirements.txt
```

---

## 📞 Summary

**Status:** ✅ **FULLY WORKING**

**What's Ready:**
- Gmail integration via Composio
- Complete resume processing pipeline
- AI enrichment with Google Gemini
- Multi-user support
- REST API endpoints
- Automatic cron job (every 15 min)
- Comprehensive testing

**Next:** Person 5 implements scoring to rank candidates! 🚀
