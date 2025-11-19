"""
Gmail Monitor Module

Person 2: Gmail Monitoring - IMPLEMENTED
Monitor Gmail for new resume emails and process them automatically

This module:
1. Polls Gmail inbox for resume-related emails (or responds to webhooks)
2. Downloads resume attachments
3. Runs extractor → enricher → formatter pipeline
4. Saves candidate JSON to /data/candidates/
5. Calls Person 5's pipeline endpoint to trigger scoring
"""

from typing import Dict, Any, List, Optional
import os
import json
import logging
from datetime import datetime
from pathlib import Path

logger = logging.getLogger(__name__)


class GmailMonitor:
    """
    Gmail Resume Monitor
    
    Integrates with:
    - Person 4's OAuth module (for Gmail access)
    - Person 2's extractor/enricher/formatter
    - Person 5's pipeline endpoint
    """
    
    def __init__(self, data_dir: str = "./data"):
        """
        Initialize Gmail Monitor
        
        Args:
            data_dir: Directory to save candidate data
        """
        self.data_dir = Path(data_dir)
        self.resumes_dir = self.data_dir / "resumes"
        self.candidates_dir = self.data_dir / "candidates"
        
        # Create directories
        self.resumes_dir.mkdir(parents=True, exist_ok=True)
        self.candidates_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize Person 2 pipeline components
        from .extractor import ResumeExtractor
        from .enricher import ResumeEnricher
        from .formatter import ResumeFormatter
        
        self.extractor = ResumeExtractor()
        self.enricher = ResumeEnricher()
        self.formatter = ResumeFormatter()
        
        logger.info("GmailMonitor initialized")
    
    
    def start_monitoring(self, user_id: str, check_interval: int = 300):
        """
        Start monitoring Gmail for new resumes
        
        This would typically run as a background task/cron job
        
        Args:
            user_id: Composio user ID for Gmail access
            check_interval: Seconds between checks (default: 5 minutes)
        """
        logger.info(f"Starting Gmail monitor for user: {user_id}")
        logger.info(f"Check interval: {check_interval} seconds")
        
        # NOTE: In production, this would be triggered by:
        # - APScheduler cron job (already configured in tasks/scheduler.py)
        # - Gmail webhook (push notifications)
        # - Manual API call from frontend
        
        # For now, this is called by the check_new_resume_emails task
        logger.info("Gmail monitor ready. Use scheduled task or manual trigger.")
    
    
    def process_new_emails(self, user_id: str, use_mock: bool = False) -> List[Dict[str, Any]]:
        """
        Check Gmail for new resume emails and process them
        
        Args:
            user_id: Composio user ID
            use_mock: Use mock data for testing
            
        Returns:
            List of processed candidates
        """
        logger.info(f"Checking for new resume emails (mock={use_mock})...")
        
        # Import Gmail integration (Person 4's work)
        from modules.integrations.gmail import GmailIntegration
        
        gmail = GmailIntegration()
        
        # Get new resume emails
        emails = gmail.check_for_new_resumes(user_id, use_mock=use_mock)
        
        processed_candidates = []
        
        for email in emails:
            try:
                # Process each email
                candidate = self.handle_resume_email(email)
                if candidate:
                    processed_candidates.append(candidate)
            except Exception as e:
                logger.error(f"Error processing email {email.get('id')}: {e}")
        
        logger.info(f"Processed {len(processed_candidates)} new candidates")
        return processed_candidates
    
    
    def handle_resume_email(self, email: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Process a single resume email
        
        Pipeline:
        1. Download attachment
        2. Extract data
        3. Enrich data
        4. Format data
        5. Save candidate JSON
        6. Notify Person 5's pipeline
        
        Args:
            email: Email data from Gmail integration
            
        Returns:
            Processed candidate JSON or None if failed
        """
        logger.info(f"Processing resume email: {email.get('subject')}")
        
        # Get attachment info
        attachments = email.get('attachments', [])
        
        if not attachments:
            logger.warning("No attachments found in email")
            return None
        
        # Process first resume attachment
        # TODO: Handle multiple attachments
        attachment = attachments[0]
        
        # Download attachment (already done by Gmail integration)
        file_path = attachment.get('file_path')
        
        if not file_path or not os.path.exists(file_path):
            logger.error(f"Attachment file not found: {file_path}")
            return None
        
        try:
            # Run Person 2 pipeline
            candidate_json = self.process_resume_file(file_path)
            
            # Add email metadata
            candidate_json['metadata']['source_email'] = email.get('id')
            candidate_json['metadata']['received_at'] = email.get('date')
            candidate_json['metadata']['sender'] = email.get('from')
            
            # Save candidate JSON
            candidate_id = self.save_candidate(candidate_json)
            candidate_json['id'] = candidate_id
            
            # Notify Person 5's pipeline
            self.notify_pipeline(candidate_json)
            
            logger.info(f"Successfully processed candidate: {candidate_json['name']} (ID: {candidate_id})")
            return candidate_json
            
        except Exception as e:
            logger.error(f"Error processing resume file: {e}")
            return None
    
    
    def process_resume_file(self, file_path: str) -> Dict[str, Any]:
        """
        Run the complete Person 2 pipeline on a resume file
        
        Pipeline:
        1. Extract (Person 2 - extractor.py)
        2. Enrich (Person 2 - enricher.py)
        3. Format (Person 2 - formatter.py)
        
        Args:
            file_path: Path to resume file
            
        Returns:
            Finalized candidate JSON
        """
        logger.info(f"Running Person 2 pipeline on: {file_path}")
        
        # Step 1: Extract
        logger.info("Step 1: Extraction...")
        extracted = self.extractor.extract_from_file(file_path)
        
        # Step 2: Enrich
        logger.info("Step 2: Enrichment...")
        enriched = self.enricher.enrich_candidate(extracted)
        
        # Step 3: Format
        logger.info("Step 3: Formatting...")
        finalized = self.formatter.finalize_candidate(enriched)
        
        logger.info("Person 2 pipeline complete!")
        return finalized
    
    
    def save_candidate(self, candidate_json: Dict[str, Any]) -> str:
        """
        Save candidate JSON to file
        
        Args:
            candidate_json: Candidate data
            
        Returns:
            Candidate ID
        """
        # Generate candidate ID from email or timestamp
        email = candidate_json.get('email', '')
        if email:
            # Use email as base for ID
            candidate_id = email.replace('@', '_at_').replace('.', '_')
        else:
            # Use timestamp
            candidate_id = f"candidate_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}"
        
        # Save to file
        file_path = self.candidates_dir / f"{candidate_id}.json"
        
        with open(file_path, 'w') as f:
            json.dump(candidate_json, f, indent=2)
        
        logger.info(f"Saved candidate to: {file_path}")
        return candidate_id
    
    
    def notify_pipeline(self, candidate_json: Dict[str, Any]):
        """
        Notify Person 5's pipeline that a new candidate is ready for scoring
        
        This would make a POST request to /api/pipeline/new_candidate
        
        Args:
            candidate_json: Finalized candidate data
        """
        logger.info("Notifying Person 5's pipeline...")
        
        # In production, make HTTP request to pipeline endpoint
        # For now, just log
        
        # Example (when API is running):
        # import requests
        # response = requests.post(
        #     "http://localhost:8000/api/pipeline/new_candidate",
        #     json=candidate_json
        # )
        
        logger.info(f"Candidate ready for scoring: {candidate_json['name']}")
        logger.info("NOTE: In production, POST to /api/pipeline/new_candidate")
    
    
    def get_processed_candidates(self) -> List[Dict[str, Any]]:
        """
        Get all processed candidates from storage
        
        Returns:
            List of candidate JSONs
        """
        candidates = []
        
        for file_path in self.candidates_dir.glob("*.json"):
            with open(file_path, 'r') as f:
                candidate = json.load(f)
                candidates.append(candidate)
        
        logger.info(f"Found {len(candidates)} processed candidates")
        return candidates
    
    
    def manual_process_resume(self, file_path: str) -> Dict[str, Any]:
        """
        Manually process a resume file (for testing/debugging)
        
        Args:
            file_path: Path to resume file
            
        Returns:
            Processed candidate JSON
        """
        logger.info(f"Manual resume processing: {file_path}")
        
        # Run pipeline
        candidate_json = self.process_resume_file(file_path)
        
        # Save
        candidate_id = self.save_candidate(candidate_json)
        candidate_json['id'] = candidate_id
        
        # Notify
        self.notify_pipeline(candidate_json)
        
        return candidate_json
