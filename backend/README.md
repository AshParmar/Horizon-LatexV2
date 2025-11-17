# AI Recruitment Platform - Backend

FastAPI backend for an AI-driven recruitment automation platform.

## 📁 Folder Structure

```
backend/
├── main.py                          # FastAPI application entry point
├── api/                             # API endpoints
│   ├── jd.py                       # Job description endpoints
│   ├── pipeline.py                 # Pipeline management
│   ├── scoring.py                  # Resume scoring
│   ├── analytics.py                # Analytics and insights
│   ├── actions.py                  # Automated actions
│   ├── integrations.py             # Integration management
│   ├── enricher.py                 # Resume enrichment
│   └── health.py                   # Health checks
├── core/                            # Core functionality
│   ├── config.py                   # Configuration management
│   ├── utils.py                    # Utility functions
│   └── logger.py                   # Logging setup
├── modules/                         # Business logic modules
│   ├── jd/
│   │   └── parser.py               # JD parsing logic
│   ├── resume/
│   │   ├── extractor.py            # Resume text extraction
│   │   ├── enricher.py             # External data enrichment
│   │   └── formatter.py            # Output formatting
│   ├── scoring/
│   │   ├── llm_score.py            # AI-based scoring
│   │   ├── keyword_score.py        # Keyword matching
│   │   └── final_score.py          # Score combination
│   ├── embeddings/
│   │   ├── embedder.py             # Vector embeddings
│   │   └── store.py                # Vector database
│   └── integrations/
│       ├── gmail.py                # Gmail integration
│       ├── calendar.py             # Google Calendar
│       ├── sheets.py               # Google Sheets
│       └── oauth.py                # OAuth management
└── data/                            # Data storage
    ├── raw/                        # Uploaded files
    ├── processed/                  # Processed data
    └── logs/                       # Application logs
```

## 🚀 Quick Start

### 1. Setup Environment

```powershell
# Create virtual environment
python -m venv venv

# Activate
.\venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure Environment Variables

```powershell
# Copy example env file
cp .env.example .env

# Edit .env with your credentials
# - OPENAI_API_KEY
# - COMPOSIO_API_KEY
# - Auth Config IDs from Composio dashboard
```

### 3. Run the Server

```powershell
# Development mode
python main.py

# Or using uvicorn directly
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 4. Access API Documentation

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 📋 TODO for Contributors

All files contain placeholder functions with `TODO` comments. Contributors should:

1. **Choose a module** to implement
2. **Read the TODO comments** in that file
3. **Implement the logic** following the function signatures
4. **Test your implementation**
5. **Document any new dependencies** in requirements.txt

### Priority Implementation Order

1. **Core Infrastructure**
   - ✅ Config and logging (already setup)
   - ⏳ OAuth integration (modules/integrations/oauth.py)
   - ⏳ Database models (if needed)

2. **Resume Processing**
   - ⏳ Resume extractor (PDF, DOCX parsing)
   - ⏳ JD parser
   - ⏳ Resume enricher

3. **Scoring System**
   - ⏳ LLM scorer
   - ⏳ Keyword scorer
   - ⏳ Final score calculator

4. **Embeddings**
   - ⏳ Embedder (vector generation)
   - ⏳ Vector store (ChromaDB/Pinecone)

5. **Integrations**
   - ⏳ Gmail integration
   - ⏳ Calendar integration
   - ⏳ Sheets integration

6. **API Endpoints**
   - ⏳ Connect API endpoints to business logic

## 🔧 Development Guidelines

### Adding New Dependencies

```powershell
pip install package-name
pip freeze > requirements.txt
```

### Code Style

- Follow PEP 8
- Add type hints
- Write docstrings
- Comment TODOs clearly

### Testing

```powershell
# Install test dependencies
pip install pytest pytest-asyncio httpx

# Run tests
pytest
```

## 🔑 Composio Setup

1. Go to https://platform.composio.dev
2. Create Auth Configs for:
   - Gmail
   - Google Calendar
   - Google Sheets
3. Copy Auth Config IDs to `.env`

## 📝 API Overview

### Job Description
- `POST /api/v1/jd/parse` - Parse JD
- `POST /api/v1/jd/upload` - Upload JD file
- `GET /api/v1/jd/{jd_id}` - Get JD details

### Scoring
- `POST /api/v1/scoring/score` - Score resume
- `POST /api/v1/scoring/batch-score` - Batch scoring
- `GET /api/v1/scoring/ranking/{jd_id}` - Get rankings

### Actions
- `POST /api/v1/actions/email/send` - Send email
- `POST /api/v1/actions/calendar/schedule` - Schedule interview

### Integrations
- `GET /api/v1/integrations/connect/{service}` - Connect service
- `GET /api/v1/integrations/status` - Integration status

## 🤝 Contributing

Each contributor should:
1. Pick a TODO from any module
2. Implement the function
3. Test thoroughly
4. Document any changes

## 📄 License

[Add your license here]
