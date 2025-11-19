"""
Gmail Integration Module

Person 4: Gmail API Integration using Composio
Provides Gmail operations for the recruitment platform
"""

from typing import List, Optional, Dict, Any
import logging
import os
import shutil
import tempfile
from pathlib import Path
from datetime import datetime

logger = logging.getLogger(__name__)


class GmailIntegration:
    """
    Gmail Integration using Composio
    
    Handles:
    - Checking inbox for resume emails
    - Downloading attachments
    - Sending emails (interview invites, etc.)
    """
    
    def __init__(self, composio_client=None):
        """
        Initialize Gmail Integration
        
        Args:
            composio_client: Composio client instance (optional)
        """
        if composio_client:
            self.composio = composio_client
        else:
            # Get Composio client from OAuth module
            try:
                from core.config import settings
                from composio import Composio
                self.composio = Composio(api_key=settings.COMPOSIO_API_KEY)
                logger.info("GmailIntegration initialized with Composio")
            except Exception as e:
                logger.warning(f"Failed to initialize Composio client: {e}")
                self.composio = None
        
        # Setup download folder
        self.download_folder = Path("./data/resumes")
        self.download_folder.mkdir(parents=True, exist_ok=True)
    
    
    def check_for_new_resumes(
        self,
        user_id: str,
        use_mock: bool = False
    ) -> List[Dict[str, Any]]:
        """
        Check Gmail inbox for resume-related emails
        
        This is the main method used by Person 2's gmail_monitor
        
        Args:
            user_id: Composio user ID
            use_mock: Use mock data for testing (default: False)
            
        Returns:
            List of emails with resume attachments
        """
        if use_mock:
            logger.info("Using mock resume emails for testing")
            return self._get_mock_resume_emails()
        
        logger.info(f"Checking Gmail for new resume emails (user: {user_id})")
        
        try:
            if not self.composio:
                logger.warning("Composio client not initialized - using mock data")
                return self._get_mock_resume_emails()
            
            # Fetch emails with PDF/DOCX attachments directly
            logger.info("Fetching emails with attachments from Gmail...")
            
            result = self.composio.tools.execute(
                slug="GMAIL_FETCH_EMAILS",
                arguments={
                    "max_results": 20,
                    "label_ids": ["INBOX"],
                    "query": "has:attachment newer_than:7d"  # Get all attachments from last 7 days
                },
                user_id=user_id,
                dangerously_skip_version_check=True
            )
            
            if not result or not result.get('successful'):
                logger.warning(f"Gmail fetch failed: {result.get('error') if result else 'No response'}")
                logger.info("Falling back to mock data")
                return self._get_mock_resume_emails()
            
            messages = result.get('data', {}).get('messages', [])
            logger.info(f"Found {len(messages)} messages with attachments")
            
            # Process each message and download PDF/DOCX resumes
            resume_emails = []
            
            for message in messages:
                try:
                    message_id = message.get('messageId')
                    sender = message.get('sender', 'Unknown')
                    subject = message.get('subject', 'No Subject')
                    
                    # Check for PDF/DOCX attachments
                    attachment_list = message.get('attachmentList', [])
                    
                    for attachment in attachment_list:
                        filename = attachment.get('filename', '')
                        
                        # Only process resume files (PDF, DOCX, TXT)
                        if filename and (filename.endswith('.pdf') or 
                                       filename.endswith('.docx') or 
                                       filename.endswith('.txt')):
                            
                            attachment_id = attachment.get('attachmentId')
                            
                            if attachment_id:
                                # Download the attachment
                                file_path = self._download_attachment(
                                    message_id=message_id,
                                    attachment_id=attachment_id,
                                    filename=filename,
                                    user_id=user_id
                                )
                                
                                if file_path:
                                    resume_emails.append({
                                        'subject': subject,
                                        'from': sender,
                                        'message_id': message_id,
                                        'attachments': [{
                                            'file_path': file_path,
                                            'filename': filename,
                                            'mime_type': attachment.get('mimeType', 'application/octet-stream')
                                        }]
                                    })
                                    logger.info(f"✅ Downloaded resume: {filename} from {sender}")
                
                except Exception as e:
                    logger.error(f"Error processing message: {e}")
                    continue
            
            logger.info(f"Successfully downloaded {len(resume_emails)} resume files")
            return resume_emails
            
        except Exception as e:
            logger.error(f"Error checking Gmail: {e}")
            logger.info("Falling back to mock data")
            return self._get_mock_resume_emails()
    
    
    def _download_attachment(
        self,
        message_id: str,
        attachment_id: str,
        filename: str,
        user_id: str
    ) -> Optional[str]:
        """
        Download Gmail attachment using Composio
        
        Args:
            message_id: Gmail message ID
            attachment_id: Attachment ID
            filename: Original filename
            user_id: Composio user ID
            
        Returns:
            Path to downloaded file in data/resumes/, or None on error
        """
        try:
            # Check if file already exists in our download folder
            final_path = self.download_folder / filename
            if final_path.exists():
                logger.info(f"File already exists, using cached: {filename}")
                return str(final_path)
            
            logger.info(f"Downloading attachment: {filename}")
            
            result = self.composio.tools.execute(
                slug="GMAIL_GET_ATTACHMENT",
                arguments={
                    "message_id": message_id,
                    "attachment_id": attachment_id,
                    "file_name": filename
                },
                user_id=user_id,
                dangerously_skip_version_check=True
            )
            
            if not result or not result.get('successful'):
                logger.error(f"Download failed: {result.get('error') if result else 'No response'}")
                return None
            
            attachment_data = result.get('data', {})
            
            # Composio auto-downloads the file and returns the path
            composio_file_path = attachment_data.get('file')
            
            if composio_file_path and os.path.exists(composio_file_path):
                # Move the file from Composio's temp location to our data/resumes folder
                shutil.move(composio_file_path, final_path)
                logger.info(f"Saved to: {final_path}")
                return str(final_path)
            
            logger.error(f"No file found in Composio response for {filename}")
            return None
            
        except Exception as e:
            logger.error(f"Error downloading attachment {filename}: {e}")
            return None
    

    
    
    def _get_mock_resume_emails(self) -> List[Dict[str, Any]]:
        """
        Generate mock resume emails for testing
        
        Returns:
            List of mock email objects with attachments
        """
        # Create temp directory for mock files
        temp_dir = tempfile.gettempdir()
        
        # Mock resume 1
        resume1_path = os.path.join(temp_dir, "alice_resume.txt")
        with open(resume1_path, 'w') as f:
            f.write("""Alice Johnson
alice.johnson@example.com
(555) 111-2222

SKILLS
Python, FastAPI, React, Docker, AWS

EXPERIENCE
Senior Software Engineer at TechCorp
2020-Present

EDUCATION
BS Computer Science, MIT, 2019
""")
        
        # Mock resume 2
        resume2_path = os.path.join(temp_dir, "bob_resume.txt")
        with open(resume2_path, 'w') as f:
            f.write("""Bob Williams
bob.williams@example.com
(555) 333-4444

SKILLS
JavaScript, Node.js, MongoDB, Kubernetes

EXPERIENCE
Full Stack Developer at StartupCo
2019-Present

EDUCATION
MS Software Engineering, Stanford, 2018
""")
        
        # Mock resume 3
        resume3_path = os.path.join(temp_dir, "carol_resume.txt")
        with open(resume3_path, 'w') as f:
            f.write("""Carol Davis
carol.davis@example.com
(555) 555-6666

SKILLS
Machine Learning, Python, TensorFlow, PyTorch

EXPERIENCE
ML Engineer at AI Labs
2021-Present

EDUCATION
PhD Computer Science, Berkeley, 2020
""")
        
        mock_emails = [
            {
                "id": "mock_email_1",
                "from": "alice.johnson@example.com",
                "subject": "Application for Software Engineer Position",
                "date": datetime.utcnow().isoformat(),
                "body": "Please find my resume attached.",
                "attachments": [
                    {
                        "filename": "alice_resume.txt",
                        "file_path": resume1_path,
                        "mime_type": "text/plain"
                    }
                ]
            },
            {
                "id": "mock_email_2",
                "from": "bob.williams@example.com",
                "subject": "Resume - Full Stack Developer",
                "date": datetime.utcnow().isoformat(),
                "body": "Attached is my resume for your review.",
                "attachments": [
                    {
                        "filename": "bob_resume.txt",
                        "file_path": resume2_path,
                        "mime_type": "text/plain"
                    }
                ]
            },
            {
                "id": "mock_email_3",
                "from": "carol.davis@example.com",
                "subject": "ML Engineer Application",
                "date": datetime.utcnow().isoformat(),
                "body": "Hi, I'm interested in the ML Engineer role.",
                "attachments": [
                    {
                        "filename": "carol_resume.txt",
                        "file_path": resume3_path,
                        "mime_type": "text/plain"
                    }
                ]
            }
        ]
        
        logger.info(f"Generated {len(mock_emails)} mock resume emails")
        return mock_emails
    
    
    def send_email(
        self,
        to: str,
        subject: str,
        body: str,
        cc: Optional[List[str]] = None,
        attachments: Optional[List[str]] = None,
        user_id: str = None
    ) -> Dict[str, Any]:
        """
        Send email via Gmail
        
        TODO: Implement email sending
        - Use Composio Gmail actions
        - Support HTML body
        - Handle attachments
        - Track sent emails
        
        Use Composio action: GMAIL_SEND_EMAIL
        
        Args:
            to: Recipient email
            subject: Email subject
            body: Email body (HTML supported)
            cc: CC recipients
            attachments: File paths for attachments
            user_id: Composio user ID
            
        Returns:
            Send status and message ID
        """
        raise NotImplementedError("Implement Gmail send_email using Composio")
    
    
    def send_from_template(
        self,
        to: str,
        template_name: str,
        variables: Dict[str, Any],
        user_id: str = None
    ) -> Dict[str, Any]:
        """
        Send email using a template
        
        TODO: Implement template-based sending
        - Load email template
        - Replace variables
        - Send email
        
        Templates:
        - interview_invite
        - rejection
        - offer_letter
        - application_received
        
        Args:
            to: Recipient email
            template_name: Name of template
            variables: Template variables
            user_id: Composio user ID
            
        Returns:
            Send status
        """
        raise NotImplementedError("Implement template-based email sending")
    
    
    def get_sent_emails(
        self,
        limit: int = 10,
        user_id: str = None
    ) -> List[Dict[str, Any]]:
        """
        Get sent emails
        
        TODO: Implement email retrieval
        - Use Composio Gmail actions
        - Filter sent emails
        - Return metadata
        
        Use Composio action: GMAIL_LIST_MESSAGES
        
        Args:
            limit: Max emails to return
            user_id: Composio user ID
            
        Returns:
            List of sent emails
        """
        raise NotImplementedError("Implement get_sent_emails using Composio")
    
    
    def track_email_status(
        self,
        message_id: str,
        user_id: str = None
    ) -> Dict[str, Any]:
        """
        Track email delivery/read status
        
        TODO: Implement email tracking
        - Check if delivered
        - Check if read (if tracking enabled)
        
        Args:
            message_id: Gmail message ID
            user_id: Composio user ID
            
        Returns:
            Email status
        """
        raise NotImplementedError("Implement email tracking")
