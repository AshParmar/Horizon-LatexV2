from fastapi import APIRouter, UploadFile, File, HTTPException
from app.models import JDTextRequest
from app.jd_parser.parser import parse_jd_with_gemini
from app.utils import extract_text_from_pdf, save_to_json_file, generate_id

router = APIRouter()

@router.post("/parse-text")
async def parse_jd_text(data: JDTextRequest):
    """Parse JD from text"""
    try:
        job_id = generate_id("JD")
        parsed = parse_jd_with_gemini(data.jd_text)
        parsed["job_id"] = job_id
        parsed["source"] = "text"
        
        filepath = f"data/jds/{job_id}.json"
        save_to_json_file(filepath, parsed)
        
        return {
            "success": True,
            "job_id": job_id,
            "file": filepath,
            "data": parsed
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/parse-pdf")
async def parse_jd_pdf(file: UploadFile = File(...)):
    """Parse JD from PDF"""
    try:
        if not file.filename.lower().endswith('.pdf'):
            raise HTTPException(status_code=400, detail="Only PDF allowed")
        
        job_id = generate_id("JD")
        pdf_bytes = await file.read()
        jd_text = extract_text_from_pdf(pdf_bytes)
        
        parsed = parse_jd_with_gemini(jd_text)
        parsed["job_id"] = job_id
        parsed["source"] = "pdf"
        parsed["filename"] = file.filename
        
        filepath = f"data/jds/{job_id}.json"
        save_to_json_file(filepath, parsed)
        
        return {
            "success": True,
            "job_id": job_id,
            "file": filepath,
            "data": parsed
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))