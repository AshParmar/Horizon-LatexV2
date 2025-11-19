"""
Resume Enricher API Endpoints

Person 2: Resume Processing API - IMPLEMENTED
Test endpoints for extraction, enrichment, formatting, and Gmail monitoring
"""

from fastapi import APIRouter, HTTPException, UploadFile, File, Query
from pydantic import BaseModel
from typing import Dict, Any, Optional, List
import os
import tempfile
import logging

logger = logging.getLogger(__name__)

router = APIRouter()


class CandidateJSON(BaseModel):
    """Standardized Candidate JSON (Person 2 output format)"""
    name: str
    email: str
    phone: str
    skills: List[str]
    education: List[Dict[str, str]]
    experience: List[Dict[str, str]]
    summary: str
    enriched_skills: List[str]
    vector_text: str
    metadata: Dict[str, Any]


class ProcessResumeResponse(BaseModel):
    """Response from processing a resume"""
    success: bool
    candidate: Optional[CandidateJSON] = None
    message: str


@router.post("/extract", response_model=Dict[str, Any])
async def extract_resume(file: UploadFile = File(...)):
    """
    Extract structured data from resume file
    
    Tests Person 2's extractor.py module
    
    Supported formats: PDF, DOCX, TXT
    
    Args:
        file: Resume file to extract
        
    Returns:
        Extracted candidate JSON
    """
    from modules.resume.extractor import ResumeExtractor
    
    try:
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file.filename)[1]) as tmp:
            content = await file.read()
            tmp.write(content)
            tmp_path = tmp.name
        
        # Extract
        extractor = ResumeExtractor()
        candidate_json = extractor.extract_from_file(tmp_path)
        
        # Cleanup
        os.unlink(tmp_path)
        
        return {
            "success": True,
            "candidate": candidate_json,
            "message": f"Extracted data from {file.filename}"
        }
        
    except Exception as e:
        logger.error(f"Extraction error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/enrich", response_model=Dict[str, Any])
async def enrich_candidate(candidate_json: Dict[str, Any]):
    """
    Enrich candidate JSON with additional skills
    
    Tests Person 2's enricher.py module
    
    Args:
        candidate_json: Candidate JSON from extractor
        
    Returns:
        Enriched candidate JSON
    """
    from modules.resume.enricher import ResumeEnricher
    
    try:
        enricher = ResumeEnricher()
        enriched = enricher.enrich_candidate(candidate_json)
        
        return {
            "success": True,
            "candidate": enriched,
            "enriched_skills_count": len(enriched.get('enriched_skills', [])),
            "message": "Enrichment complete"
        }
        
    except Exception as e:
        logger.error(f"Enrichment error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/format", response_model=Dict[str, Any])
async def format_candidate(candidate_json: Dict[str, Any]):
    """
    Finalize candidate JSON with vector_text
    
    Tests Person 2's formatter.py module
    
    Args:
        candidate_json: Enriched candidate JSON
        
    Returns:
        Finalized candidate JSON (ready for scoring)
    """
    from modules.resume.formatter import ResumeFormatter
    
    try:
        formatter = ResumeFormatter()
        finalized = formatter.finalize_candidate(candidate_json)
        
        return {
            "success": True,
            "candidate": finalized,
            "vector_text_length": len(finalized.get('vector_text', '')),
            "message": "Formatting complete. Ready for Person 3 (Scoring Engine)."
        }
        
    except Exception as e:
        logger.error(f"Formatting error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/process-complete", response_model=ProcessResumeResponse)
async def process_complete_pipeline(file: UploadFile = File(...)):
    """
    Run the complete Person 2 pipeline: Extract → Enrich → Format
    
    This is the full pipeline that would be triggered by Gmail monitor
    
    Args:
        file: Resume file
        
    Returns:
        Finalized candidate JSON
    """
    from modules.resume.gmail_monitor import GmailMonitor
    
    try:
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file.filename)[1]) as tmp:
            content = await file.read()
            tmp.write(content)
            tmp_path = tmp.name
        
        # Run complete pipeline
        monitor = GmailMonitor()
        candidate_json = monitor.process_resume_file(tmp_path)
        
        # Cleanup
        os.unlink(tmp_path)
        
        return ProcessResumeResponse(
            success=True,
            candidate=CandidateJSON(**candidate_json),
            message=f"Complete pipeline executed for {file.filename}"
        )
        
    except Exception as e:
        logger.error(f"Pipeline error: {e}")
        return ProcessResumeResponse(
            success=False,
            message=f"Pipeline failed: {str(e)}"
        )


@router.get("/gmail/check")
async def check_gmail_for_resumes(
    user_id: str = Query(..., description="Composio user ID"),
    use_mock: bool = Query(True, description="Use mock data for testing")
):
    """
    Check Gmail for new resume emails and process them
    
    Tests Person 2's gmail_monitor.py module
    
    Args:
        user_id: Composio user ID for Gmail access
        use_mock: Use mock data (default True for testing)
        
    Returns:
        List of processed candidates
    """
    from modules.resume.gmail_monitor import GmailMonitor
    
    try:
        monitor = GmailMonitor()
        candidates = monitor.process_new_emails(user_id, use_mock=use_mock)
        
        return {
            "success": True,
            "candidates_processed": len(candidates),
            "candidates": candidates,
            "message": f"Processed {len(candidates)} new resume emails"
        }
        
    except Exception as e:
        logger.error(f"Gmail monitoring error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/candidates")
async def get_processed_candidates():
    """
    Get all candidates processed by Person 2's pipeline
    
    Returns:
        List of candidate JSONs from storage
    """
    from modules.resume.gmail_monitor import GmailMonitor
    
    try:
        monitor = GmailMonitor()
        candidates = monitor.get_processed_candidates()
        
        return {
            "success": True,
            "total": len(candidates),
            "candidates": candidates
        }
        
    except Exception as e:
        logger.error(f"Error fetching candidates: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/batch-enrich")
async def batch_enrich(resume_ids: list[str]):
    """
    Enrich multiple resumes
    
    TODO: Implement batch enrichment
    - Process multiple resumes
    - Use async processing
    - Queue for background jobs
    
    Args:
        resume_ids: List of resume IDs
        
    Returns:
        Batch job status
    """
    raise HTTPException(status_code=501, detail="Not implemented")
