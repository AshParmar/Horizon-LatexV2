"""
Resume Formatter Module

Person 2: Resume Formatting - IMPLEMENTED
Finalize candidate JSON with vector_text for embeddings
Takes enriched candidate JSON and prepares it for Person 3 (Scoring Engine)
"""

from typing import Dict, Any, List
import logging
from datetime import datetime

logger = logging.getLogger(__name__)


class ResumeFormatter:
    """
    Resume Data Formatter
    
    Final step in Person 2's pipeline:
    1. Build vector_text from candidate data (for embeddings)
    2. Finalize candidate JSON
    3. Return standardized format ready for scoring
    """
    
    def __init__(self):
        """
        Initialize Resume Formatter
        """
        logger.info("ResumeFormatter initialized")
    
    
    def finalize_candidate(self, enriched_json: Dict[str, Any]) -> Dict[str, Any]:
        """
        Finalize candidate JSON with vector_text
        
        This is the final step before passing to Person 3 (Scoring Engine)
        
        Args:
            enriched_json: Enriched candidate JSON from enricher
            
        Returns:
            Finalized candidate JSON with vector_text populated
        """
        logger.info(f"Finalizing candidate: {enriched_json.get('name', 'Unknown')}")
        
        finalized = enriched_json.copy()
        
        # Build vector text for embeddings
        vector_text = self.build_vector_text(finalized)
        finalized['vector_text'] = vector_text
        
        # Add final metadata
        if 'metadata' not in finalized:
            finalized['metadata'] = {}
        
        finalized['metadata']['finalized_at'] = datetime.utcnow().isoformat()
        finalized['metadata']['ready_for_scoring'] = True
        
        logger.info(f"Candidate finalized. Vector text length: {len(vector_text)} characters")
        return finalized
    
    
    def build_vector_text(self, candidate_json: Dict[str, Any]) -> str:
        """
        Build comprehensive text for vector embeddings
        
        Combines all important information into a single text block
        that will be used for semantic search and similarity matching.
        
        Format:
        - Name
        - Skills (original + enriched)
        - Experience details
        - Education details
        - Summary
        
        Args:
            candidate_json: Candidate data
            
        Returns:
            Combined text for embeddings
        """
        logger.info("Building vector text for embeddings...")
        
        parts = []
        
        # Name
        name = candidate_json.get('name', '')
        if name:
            parts.append(f"Name: {name}")
        
        # Summary
        summary = candidate_json.get('summary', '')
        if summary:
            parts.append(f"Summary: {summary}")
        
        # Skills (original + enriched)
        all_skills = []
        all_skills.extend(candidate_json.get('skills', []))
        all_skills.extend(candidate_json.get('enriched_skills', []))
        all_skills = list(set(all_skills))  # Deduplicate
        
        if all_skills:
            parts.append(f"Skills: {', '.join(all_skills)}")
        
        # Experience
        experiences = candidate_json.get('experience', [])
        if experiences:
            exp_texts = []
            for exp in experiences:
                title = exp.get('title', '')
                company = exp.get('company', '')
                duration = exp.get('duration', '')
                
                exp_str = f"{title}"
                if company:
                    exp_str += f" at {company}"
                if duration:
                    exp_str += f" ({duration})"
                
                exp_texts.append(exp_str)
            
            parts.append(f"Experience: {'; '.join(exp_texts)}")
        
        # Education
        education = candidate_json.get('education', [])
        if education:
            edu_texts = []
            for edu in education:
                degree = edu.get('degree', '')
                institution = edu.get('institution', '')
                year = edu.get('year', '')
                
                edu_str = degree
                if institution:
                    edu_str += f" from {institution}"
                if year:
                    edu_str += f" ({year})"
                
                edu_texts.append(edu_str)
            
            parts.append(f"Education: {'; '.join(edu_texts)}")
        
        # Combine all parts
        vector_text = ". ".join(parts)
        
        logger.info(f"Built vector text with {len(parts)} components")
        return vector_text

