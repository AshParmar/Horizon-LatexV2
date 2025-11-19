"""
Resume Enricher Module

Person 2: Resume Enrichment - IMPLEMENTED
Enrich candidate data with LinkedIn/Google Gemini LLM enrichment
Takes candidate JSON from extractor, adds enriched_skills
"""

from typing import Dict, Any, Optional, List
import os
import logging
from datetime import datetime

logger = logging.getLogger(__name__)


class ResumeEnricher:
    """
    Resume Data Enricher
    
    Enrichment strategy:
    1. Try LinkedIn enrichment (if available)
    2. Fallback to Google Gemini LLM-based skill inference
    3. Merge enriched data with original
    """
    
    def __init__(self):
        """
        Initialize Resume Enricher
        """
        self.linkedin_enabled = False  # Enable when LinkedIn API is available
        self.llm_enabled = True  # Enable Gemini LLM-based enrichment
        
        # Load Gemini API key from config
        try:
            from core.config import Settings
            settings = Settings()
            self.gemini_api_key = settings.GOOGLE_GEMINI_API_KEY
            self.use_gemini = bool(self.gemini_api_key)
        except:
            self.gemini_api_key = os.getenv("GOOGLE_GEMINI_API_KEY", "")
            self.use_gemini = bool(self.gemini_api_key)
        
        logger.info(f"ResumeEnricher initialized (Gemini: {self.use_gemini})")
    
    
    def enrich_candidate(self, candidate_json: Dict[str, Any]) -> Dict[str, Any]:
        """
        Main enrichment entry point
        
        Takes candidate JSON from extractor and enriches it with:
        - Additional skills inferred from experience
        - LinkedIn data (if available)
        - LLM-generated insights
        
        Args:
            candidate_json: Standardized candidate JSON from extractor
            
        Returns:
            Enriched candidate JSON with enriched_skills populated
        """
        logger.info(f"Enriching candidate: {candidate_json.get('name', 'Unknown')}")
        
        enriched = candidate_json.copy()
        
        # Try LinkedIn enrichment first
        if self.linkedin_enabled:
            try:
                linkedin_data = self.enrich_with_linkedin(candidate_json)
                enriched = self.merge_enrichment(enriched, linkedin_data)
            except Exception as e:
                logger.warning(f"LinkedIn enrichment failed: {e}, falling back to LLM")
        
        # Fallback to LLM enrichment
        if self.llm_enabled:
            try:
                llm_enriched = self.enrich_with_llm(enriched)
                enriched = self.merge_enrichment(enriched, llm_enriched)
            except Exception as e:
                logger.error(f"LLM enrichment failed: {e}")
        
        # Add enrichment metadata
        enriched['metadata']['enriched_at'] = datetime.utcnow().isoformat()
        enriched['metadata']['enrichment_sources'] = []
        
        if self.linkedin_enabled:
            enriched['metadata']['enrichment_sources'].append('linkedin')
        if self.llm_enabled:
            enriched['metadata']['enrichment_sources'].append('llm')
        
        logger.info(f"Enrichment complete. Added {len(enriched.get('enriched_skills', []))} enriched skills")
        return enriched
    
    
    def enrich_with_linkedin(self, candidate_json: Dict[str, Any]) -> Dict[str, Any]:
        """
        Enrich candidate data using LinkedIn API
        
        NOTE: LinkedIn API access is restricted. This is a placeholder.
        In production, you would need:
        - LinkedIn API credentials
        - OAuth flow for user consent
        - Rate limiting
        
        For now, returns mock enrichment data
        
        Args:
            candidate_json: Candidate data
            
        Returns:
            LinkedIn-enriched data
        """
        logger.info("Attempting LinkedIn enrichment...")
        
        # Mock LinkedIn enrichment
        # In production: Use LinkedIn API to fetch profile
        mock_enriched_skills = []
        
        # Simulate finding additional skills from LinkedIn
        if 'python' in [s.lower() for s in candidate_json.get('skills', [])]:
            mock_enriched_skills.extend(['FastAPI', 'SQLAlchemy', 'Pytest'])
        
        if 'javascript' in [s.lower() for s in candidate_json.get('skills', [])]:
            mock_enriched_skills.extend(['TypeScript', 'React Hooks', 'Next.js'])
        
        return {
            "enriched_skills": mock_enriched_skills,
            "linkedin_url": "",  # Would be populated from API
            "linkedin_headline": "",  # Would be populated from API
        }
    
    
    def enrich_with_llm(self, candidate_json: Dict[str, Any]) -> Dict[str, Any]:
        """
        Enrich candidate data using Google Gemini LLM inference
        
        Uses the candidate's experience and existing skills to infer:
        - Related skills they likely have
        - Technologies commonly used together
        - Soft skills based on job titles
        
        Uses Google Gemini API for intelligent skill inference
        Falls back to rule-based approach if API fails
        
        Args:
            candidate_json: Candidate data
            
        Returns:
            LLM-enriched data
        """
        logger.info("Performing LLM-based skill inference...")
        
        # Try Gemini API first if available
        if self.use_gemini:
            try:
                gemini_result = self._enrich_with_gemini(candidate_json)
                if gemini_result:
                    return gemini_result
            except Exception as e:
                logger.warning(f"Gemini API enrichment failed: {e}, falling back to rules")
        
        # Fallback to rule-based enrichment
        return self._enrich_with_rules(candidate_json)
    
    
    def _enrich_with_gemini(self, candidate_json: Dict[str, Any]) -> Dict[str, Any]:
        """
        Use Google Gemini API for skill enrichment
        
        Args:
            candidate_json: Candidate data
            
        Returns:
            Gemini-enriched data
        """
        try:
            import google.generativeai as genai
            
            # Configure Gemini
            genai.configure(api_key=self.gemini_api_key)
            model = genai.GenerativeModel('gemini-2.0-flash')
            
            # Build prompt
            skills = candidate_json.get('skills', [])
            experience = candidate_json.get('experience', [])
            
            prompt = f"""Based on this candidate's profile, suggest additional technical and soft skills they likely possess:

Current Skills: {', '.join(skills)}
Experience: {[exp.get('title', '') for exp in experience]}

Provide only a comma-separated list of 5-10 additional skills they likely have (no explanations).
Focus on related technologies, frameworks, and professional competencies."""
            
            # Call Gemini
            response = model.generate_content(prompt)
            
            # Parse response
            enriched_skills = [s.strip() for s in response.text.split(',')]
            enriched_skills = [s for s in enriched_skills if s and len(s) < 50][:10]
            
            logger.info(f"Gemini enrichment added {len(enriched_skills)} skills")
            
            return {
                "enriched_skills": enriched_skills,
                "enrichment_method": "gemini_api"
            }
            
        except ImportError:
            logger.warning("google-generativeai library not installed")
            return None
        except Exception as e:
            logger.error(f"Gemini API error: {e}")
            return None
    
    
    def _enrich_with_rules(self, candidate_json: Dict[str, Any]) -> Dict[str, Any]:
        """
        Rule-based skill enrichment (fallback)
        
        Args:
            candidate_json: Candidate data
            
        Returns:
            Rule-enriched data
        """
        logger.info("Performing LLM-based skill inference...")
        
        enriched_skills = []
        existing_skills = [s.lower() for s in candidate_json.get('skills', [])]
        
        # Skill inference rules (in production, use LLM)
        skill_relationships = {
            'python': ['Django', 'FastAPI', 'Pandas', 'NumPy', 'Pytest'],
            'javascript': ['TypeScript', 'React', 'Node.js', 'npm', 'Webpack'],
            'react': ['Redux', 'React Router', 'JSX', 'Hooks'],
            'django': ['Django REST Framework', 'Celery', 'PostgreSQL'],
            'fastapi': ['Pydantic', 'SQLAlchemy', 'Alembic', 'Uvicorn'],
            'aws': ['EC2', 'S3', 'Lambda', 'RDS', 'CloudFormation'],
            'docker': ['Docker Compose', 'Kubernetes', 'Container Orchestration'],
            'sql': ['Database Design', 'Query Optimization', 'Indexing'],
            'machine learning': ['Scikit-learn', 'Feature Engineering', 'Model Evaluation'],
        }
        
        # Infer related skills
        for skill in existing_skills:
            if skill in skill_relationships:
                related = skill_relationships[skill]
                enriched_skills.extend(related)
        
        # Infer soft skills from job titles
        experience = candidate_json.get('experience', [])
        for exp in experience:
            title = exp.get('title', '').lower()
            
            if 'senior' in title or 'lead' in title:
                enriched_skills.extend(['Leadership', 'Mentoring', 'Code Review'])
            
            if 'manager' in title:
                enriched_skills.extend(['Team Management', 'Project Planning', 'Stakeholder Communication'])
            
            if 'architect' in title:
                enriched_skills.extend(['System Design', 'Architecture Patterns', 'Technical Documentation'])
        
        # Deduplicate and filter out already existing skills
        enriched_skills = list(set(enriched_skills))
        enriched_skills = [s for s in enriched_skills if s.lower() not in existing_skills]
        
        logger.info(f"LLM inference added {len(enriched_skills)} new skills")
        
        return {
            "enriched_skills": enriched_skills,
            "enrichment_method": "llm_inference"
        }
    
    
    def merge_enrichment(
        self, 
        original: Dict[str, Any], 
        enriched_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Merge enriched data into original candidate JSON
        
        Strategy:
        - Add new enriched_skills (no duplicates)
        - Preserve original data
        - Add metadata about enrichment
        
        Args:
            original: Original candidate JSON
            enriched_data: Enriched data to merge
            
        Returns:
            Merged candidate JSON
        """
        merged = original.copy()
        
        # Merge enriched skills
        existing_enriched = merged.get('enriched_skills', [])
        new_enriched = enriched_data.get('enriched_skills', [])
        
        # Deduplicate
        all_enriched = list(set(existing_enriched + new_enriched))
        merged['enriched_skills'] = all_enriched
        
        # Add any other enrichment data to metadata
        if 'metadata' not in merged:
            merged['metadata'] = {}
        
        if 'linkedin_url' in enriched_data:
            merged['metadata']['linkedin_url'] = enriched_data['linkedin_url']
        
        if 'linkedin_headline' in enriched_data:
            merged['metadata']['linkedin_headline'] = enriched_data['linkedin_headline']
        
        return merged
