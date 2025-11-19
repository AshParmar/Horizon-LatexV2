"""
Resume Extractor Module

Person 2: Resume Extraction - IMPLEMENTED
Extract structured data from resume files (PDF, DOCX, TXT)
Returns standardized candidate JSON for Person 3 (Scoring Engine)
"""

from typing import Dict, Any, List, Optional
import os
import re
import logging
from datetime import datetime

logger = logging.getLogger(__name__)


class ResumeExtractor:
    """
    Resume Text and Data Extractor
    
    TODO: Implement extraction from multiple formats
    """
    
    def __init__(self):
        """Initialize Resume Extractor"""
        self.supported_formats = ['.pdf', '.docx', '.txt']
    
    
    def extract_text_from_pdf(self, file_path: str) -> str:
        """
        Extract raw text from PDF file
        
        Args:
            file_path: Path to PDF file
            
        Returns:
            Extracted raw text
        """
        logger.info(f"Extracting text from PDF: {file_path}")
        
        try:
            # Try with pdfplumber first (better for structured PDFs)
            try:
                import pdfplumber
                text = ""
                with pdfplumber.open(file_path) as pdf:
                    for page in pdf.pages:
                        page_text = page.extract_text()
                        if page_text:
                            text += page_text + "\n"
                logger.info(f"Extracted {len(text)} characters using pdfplumber")
                return text
            except ImportError:
                logger.warning("pdfplumber not installed, falling back to PyPDF2")
            
            # Fallback to PyPDF2
            try:
                import PyPDF2
                text = ""
                with open(file_path, 'rb') as file:
                    pdf_reader = PyPDF2.PdfReader(file)
                    for page in pdf_reader.pages:
                        text += page.extract_text() + "\n"
                logger.info(f"Extracted {len(text)} characters using PyPDF2")
                return text
            except ImportError:
                logger.error("Neither pdfplumber nor PyPDF2 installed")
                return ""
                
        except Exception as e:
            logger.error(f"Error extracting PDF text: {e}")
            return ""
    
    
    def extract_text_from_docx(self, file_path: str) -> str:
        """
        Extract raw text from DOCX file
        
        Args:
            file_path: Path to DOCX file
            
        Returns:
            Extracted raw text
        """
        logger.info(f"Extracting text from DOCX: {file_path}")
        
        try:
            import docx
            doc = docx.Document(file_path)
            text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
            logger.info(f"Extracted {len(text)} characters from DOCX")
            return text
        except ImportError:
            logger.error("python-docx not installed")
            return ""
        except Exception as e:
            logger.error(f"Error extracting DOCX text: {e}")
            return ""
    
    
    def extract_text_from_txt(self, file_path: str) -> str:
        """
        Extract text from TXT file
        
        Args:
            file_path: Path to TXT file
            
        Returns:
            File content
        """
        logger.info(f"Reading text file: {file_path}")
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                text = f.read()
            logger.info(f"Read {len(text)} characters from TXT")
            return text
        except UnicodeDecodeError:
            # Try with different encoding
            try:
                with open(file_path, 'r', encoding='latin-1') as f:
                    text = f.read()
                return text
            except Exception as e:
                logger.error(f"Error reading TXT file: {e}")
                return ""
        except Exception as e:
            logger.error(f"Error reading TXT file: {e}")
            return ""
    
    
    def extract_from_file(self, file_path: str) -> Dict[str, Any]:
        """
        Main entry point: Extract and parse resume file to standardized JSON
        
        This method:
        1. Extracts text from file (PDF/DOCX/TXT)
        2. Parses fields (name, email, skills, etc.)
        3. Cleans data
        4. Builds standardized candidate JSON
        
        Args:
            file_path: Path to resume file
            
        Returns:
            Standardized candidate JSON (ready for Person 2 enricher)
        """
        logger.info(f"Processing resume file: {file_path}")
        
        # Step 1: Extract text
        file_ext = os.path.splitext(file_path)[1].lower()
        
        if file_ext == '.pdf':
            text = self.extract_text_from_pdf(file_path)
        elif file_ext == '.docx':
            text = self.extract_text_from_docx(file_path)
        elif file_ext == '.txt':
            text = self.extract_text_from_txt(file_path)
        else:
            logger.error(f"Unsupported file format: {file_ext}")
            raise ValueError(f"Unsupported file format: {file_ext}")
        
        if not text:
            logger.error("No text extracted from file")
            return {}
        
        # Step 2: Parse fields
        parsed_data = self.extract_fields(text)
        
        # Step 3: Clean fields
        cleaned_data = self.clean_fields(parsed_data)
        
        # Step 4: Build standardized JSON
        candidate_json = self.build_candidate_json(cleaned_data)
        
        return candidate_json
    
    
    def extract_email(self, text: str) -> str:
        """
        Extract email address from text
        
        Args:
            text: Resume text
            
        Returns:
            Email address or empty string
        """
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        matches = re.findall(email_pattern, text)
        return matches[0] if matches else ""
    
    
    def extract_phone(self, text: str) -> str:
        """
        Extract phone number from text
        
        Args:
            text: Resume text
            
        Returns:
            Phone number or empty string
        """
        # Patterns for various phone formats
        patterns = [
            r'\b\d{10}\b',  # 1234567890
            r'\b\d{3}[-.\s]?\d{3}[-.\s]?\d{4}\b',  # 123-456-7890
            r'\(\d{3}\)\s*\d{3}[-.\s]?\d{4}',  # (123) 456-7890
            r'\+\d{1,3}\s*\d{10}',  # +1 1234567890
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, text)
            if matches:
                return matches[0]
        
        return ""
    
    
    def extract_name(self, text: str) -> str:
        """
        Extract candidate name (usually first line or after "Name:")
        
        Args:
            text: Resume text
            
        Returns:
            Candidate name
        """
        lines = text.split('\n')
        
        # Try to find name after "Name:" label
        for line in lines[:10]:  # Check first 10 lines
            if 'name' in line.lower() and ':' in line:
                name = line.split(':', 1)[1].strip()
                if name and len(name) < 50:  # Reasonable name length
                    return name
        
        # Otherwise, assume first non-empty line is the name
        for line in lines[:5]:
            line = line.strip()
            if line and len(line) < 50 and not '@' in line and not line.isdigit():
                return line
        
        return "Unknown"
    
    
    def extract_skills(self, text: str) -> List[str]:
        """
        Extract skills from resume text
        
        Args:
            text: Resume text
            
        Returns:
            List of identified skills
        """
        # Common technical skills to look for
        skill_keywords = [
            'python', 'java', 'javascript', 'typescript', 'c++', 'c#', 'ruby', 'go', 'rust',
            'react', 'angular', 'vue', 'node.js', 'express', 'django', 'flask', 'spring',
            'sql', 'nosql', 'mongodb', 'postgresql', 'mysql', 'redis',
            'aws', 'azure', 'gcp', 'docker', 'kubernetes', 'jenkins',
            'git', 'agile', 'scrum', 'jira', 'ci/cd',
            'machine learning', 'deep learning', 'tensorflow', 'pytorch', 'scikit-learn',
            'data analysis', 'pandas', 'numpy', 'matplotlib',
            'html', 'css', 'sass', 'bootstrap', 'tailwind',
            'rest api', 'graphql', 'microservices', 'websockets',
            'linux', 'bash', 'shell scripting'
        ]
        
        text_lower = text.lower()
        found_skills = []
        
        for skill in skill_keywords:
            if skill in text_lower:
                found_skills.append(skill.title())
        
        # Deduplicate
        found_skills = list(set(found_skills))
        
        logger.info(f"Extracted {len(found_skills)} skills")
        return found_skills
    
    
    def extract_education(self, text: str) -> List[Dict[str, str]]:
        """
        Extract education information
        
        Args:
            text: Resume text
            
        Returns:
            List of education entries
        """
        education = []
        
        # Look for degree keywords
        degrees = ['bachelor', 'master', 'phd', 'doctorate', 'b.s.', 'm.s.', 'b.a.', 'm.a.', 
                   'b.tech', 'm.tech', 'mba', 'associate']
        
        lines = text.split('\n')
        for i, line in enumerate(lines):
            line_lower = line.lower()
            for degree in degrees:
                if degree in line_lower:
                    # Try to get institution (usually next line)
                    institution = lines[i + 1].strip() if i + 1 < len(lines) else ""
                    
                    education.append({
                        "degree": line.strip(),
                        "institution": institution,
                        "year": self._extract_year(line + " " + institution)
                    })
                    break
        
        return education[:3]  # Return max 3 education entries
    
    
    def _extract_year(self, text: str) -> str:
        """Extract year from text (e.g., 2020, 2018-2022)"""
        year_pattern = r'\b(19|20)\d{2}\b'
        matches = re.findall(year_pattern, text)
        return matches[0] if matches else ""
    
    
    def extract_experience(self, text: str) -> List[Dict[str, str]]:
        """
        Extract work experience
        
        Args:
            text: Resume text
            
        Returns:
            List of experience entries
        """
        experience = []
        
        # Find "Experience" section
        exp_section = ""
        lines = text.split('\n')
        in_exp_section = False
        
        for line in lines:
            if 'experience' in line.lower() and len(line) < 30:
                in_exp_section = True
                continue
            
            if in_exp_section:
                # Stop at next section (Education, Skills, etc.)
                if any(keyword in line.lower() for keyword in ['education', 'skills', 'projects', 'certifications']):
                    break
                exp_section += line + "\n"
        
        # Simple extraction: look for job titles and companies
        job_titles = ['engineer', 'developer', 'manager', 'analyst', 'designer', 'consultant']
        
        for i, line in enumerate(exp_section.split('\n')):
            line_lower = line.lower()
            if any(title in line_lower for title in job_titles):
                experience.append({
                    "title": line.strip(),
                    "company": "",  # TODO: Extract company name
                    "duration": self._extract_year(line)
                })
        
        return experience[:5]  # Return max 5 experiences
    
    
    def extract_fields(self, text: str) -> Dict[str, Any]:
        """
        Parse all fields from resume text
        
        Args:
            text: Raw resume text
            
        Returns:
            Dictionary with extracted fields
        """
        logger.info("Parsing resume fields...")
        
        fields = {
            "name": self.extract_name(text),
            "email": self.extract_email(text),
            "phone": self.extract_phone(text),
            "skills": self.extract_skills(text),
            "education": self.extract_education(text),
            "experience": self.extract_experience(text),
            "raw_text": text
        }
        
        logger.info(f"Extracted fields for candidate: {fields['name']}")
        return fields
    
    
    def clean_fields(self, parsed_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Clean and normalize extracted fields
        
        Args:
            parsed_data: Raw parsed data
            
        Returns:
            Cleaned data
        """
        logger.info("Cleaning extracted fields...")
        
        cleaned = parsed_data.copy()
        
        # Clean name
        if cleaned.get('name'):
            cleaned['name'] = cleaned['name'].strip()
        
        # Clean email
        if cleaned.get('email'):
            cleaned['email'] = cleaned['email'].lower().strip()
        
        # Clean phone
        if cleaned.get('phone'):
            # Remove formatting, keep digits only
            cleaned['phone'] = re.sub(r'[^\d+]', '', cleaned['phone'])
        
        # Deduplicate skills
        if cleaned.get('skills'):
            cleaned['skills'] = list(set(cleaned['skills']))
        
        return cleaned
    
    
    def build_candidate_json(self, cleaned_fields: Dict[str, Any]) -> Dict[str, Any]:
        """
        Build standardized candidate JSON format for Person 3 (Scoring Engine)
        
        REQUIRED FORMAT for integration with scoring engine:
        {
          "name": "",
          "email": "",
          "phone": "",
          "skills": [],
          "education": [],
          "experience": [],
          "summary": "",
          "enriched_skills": [],
          "vector_text": ""
        }
        
        Args:
            cleaned_fields: Cleaned extracted data
            
        Returns:
            Standardized candidate JSON
        """
        logger.info("Building standardized candidate JSON...")
        
        # Generate basic summary from experience
        summary = ""
        if cleaned_fields.get('experience'):
            exp_count = len(cleaned_fields['experience'])
            summary = f"Professional with {exp_count} relevant experience entries"
        
        candidate_json = {
            "name": cleaned_fields.get('name', ''),
            "email": cleaned_fields.get('email', ''),
            "phone": cleaned_fields.get('phone', ''),
            "skills": cleaned_fields.get('skills', []),
            "education": cleaned_fields.get('education', []),
            "experience": cleaned_fields.get('experience', []),
            "summary": summary,
            "enriched_skills": [],  # Will be filled by Person 2 enricher
            "vector_text": "",  # Will be filled by Person 2 formatter
            "metadata": {
                "extracted_at": datetime.utcnow().isoformat(),
                "source": "resume_extractor"
            }
        }
        
        logger.info(f"Built candidate JSON for: {candidate_json['name']}")
        return candidate_json
