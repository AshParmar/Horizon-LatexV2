from app.config import get_gemini_model
from app.utils import clean_text, parse_gemini_json_response
import re

def parse_jd_with_gemini(jd_text: str) -> dict:
    """Parse JD using Gemini AI"""
    
    cleaned_text = clean_text(jd_text)
    
    prompt = f"""
Analyze this Job Description and extract information as JSON.

Job Description:
{cleaned_text}

Return ONLY valid JSON (no markdown):

{{
  "role": "Job title",
  "skills": ["skill1", "skill2"],
  "experience_required": "X years",
  "responsibilities": ["resp1", "resp2"],
  "requirements": ["req1", "req2"],
  "keywords": ["keyword1", "keyword2"]
}}

Rules:
- Extract ALL technical skills
- Normalize experience ("2+ years" → "2 years")
- Capitalize skill names properly
- Remove duplicates
"""

    try:
        model = get_gemini_model()
        response = model.generate_content(prompt)
        parsed_data = parse_gemini_json_response(response.text)
        return normalize_jd_data(parsed_data)
    except Exception as e:
        raise Exception(f"Parsing error: {str(e)}")

def normalize_jd_data(data: dict) -> dict:
    """Normalize JD data"""
    
    # Normalize skills
    if "skills" in data:
        skills = []
        seen = set()
        for skill in data["skills"]:
            if skill:
                normalized = str(skill).strip().title()
                if normalized.lower() not in seen:
                    skills.append(normalized)
                    seen.add(normalized.lower())
        data["skills"] = skills
    
    # Normalize role
    if "role" in data:
        data["role"] = str(data["role"]).strip().title()
    
    # Normalize experience
    if "experience_required" in data:
        exp = str(data["experience_required"]).strip()
        match = re.search(r'(\d+)', exp)
        if match:
            data["experience_required"] = f"{match.group(1)} years"
        elif "entry" in exp.lower() or "fresher" in exp.lower():
            data["experience_required"] = "Entry level"
    
    # Default values
    defaults = {
        "role": "Unknown",
        "skills": [],
        "experience_required": "Not specified",
        "responsibilities": [],
        "requirements": [],
        "keywords": []
    }
    
    for key, value in defaults.items():
        if key not in data or not data[key]:
            data[key] = value
    
    return data