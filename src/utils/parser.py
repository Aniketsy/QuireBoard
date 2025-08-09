import pytesseract
from pdf2image import convert_from_path
import docx
import os
from werkzeug.utils import secure_filename

def parse_file(file) -> str:
    """Extract text from various file formats (PDF, DOCX, Image, TXT)"""
    filename = secure_filename(file.filename)
    file_path = os.path.join('uploads', filename)
    file.save(file_path)
    
    try:
        file_ext = filename.rsplit('.', 1)[1].lower()
        
        if file_ext == 'pdf':
            # Convert PDF to images and extract text
            images = convert_from_path(file_path)
            return ' '.join(pytesseract.image_to_string(image) for image in images)
            
        elif file_ext == 'docx':
            # Extract text from DOCX
            doc = docx.Document(file_path)
            return ' '.join(paragraph.text for paragraph in doc.paragraphs)
            
        elif file_ext in ['png', 'jpg', 'jpeg']:
            # Extract text from image
            return pytesseract.image_to_string(file_path)
            
        elif file_ext == 'txt':
            # Read text file
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
                
        else:
            raise ValueError(f"Unsupported file format: {file_ext}")
            
    finally:
        if os.path.exists(file_path):
            os.remove(file_path)

def parse_resume(file):
    """Parse resume file and extract structured information"""
    text = parse_file(file)
    
    # Split text into sections (basic implementation - enhance based on your needs)
    sections = text.split('\n\n')
    
    resume_data = {
        'name': '',
        'contact': '',
        'education': '',
        'experience': '',
        'skills': [],
        'summary': '',
        'achievements': ''
    }
    
    # Basic section identification logic
    for section in sections:
        section = section.strip()
        if not section:
            continue
            
        # Identify sections based on common headers
        lower_section = section.lower()
        if any(word in lower_section for word in ['@', 'phone', 'email']):
            resume_data['contact'] = section
        elif any(word in lower_section for word in ['education', 'degree', 'university']):
            resume_data['education'] = section
        elif any(word in lower_section for word in ['experience', 'work', 'employment']):
            resume_data['experience'] = section
        elif any(word in lower_section for word in ['skill', 'technology', 'programming']):
            resume_data['skills'] = [skill.strip() for skill in section.split(',')]
        elif any(word in lower_section for word in ['summary', 'objective', 'profile']):
            resume_data['summary'] = section
        elif any(word in lower_section for word in ['achievement', 'accomplishment']):
            resume_data['achievements'] = section
        elif not resume_data['name']:  # Assume first unmatched section is name
            resume_data['name'] = section
            
    return resume_data

def parse_job_description(file_or_text):
    """Parse job description from file or text"""
    if hasattr(file_or_text, 'read'):
        return parse_file(file_or_text)
    return file_or_text

# ...existing code...

from src.config.database import SessionLocal
from src.models.orm import ResumeORM, JobDescriptionORM, AnalysisORM
from datetime import datetime

def save_resume_to_db(resume_data: dict, user_id: str = None) -> int:
    """Save resume data to PostgreSQL using SQLAlchemy ORM"""
    db = SessionLocal()
    try:
        resume = ResumeORM(
            name=resume_data.get('name', ''),
            contact=resume_data.get('contact', ''),
            education=resume_data.get('education', ''),
            experience=resume_data.get('experience', ''),
            skills=','.join(resume_data.get('skills', [])),
            summary=resume_data.get('summary', ''),
            achievements=resume_data.get('achievements', ''),
            user_id=user_id,
            filename=resume_data.get('filename', None)
        )
        db.add(resume)
        db.commit()
        db.refresh(resume)
        return resume.id
    finally:
        db.close()

def save_job_description_to_db(job_data: dict) -> int:
    """Save job description to PostgreSQL using SQLAlchemy ORM"""
    db = SessionLocal()
    try:
        job = JobDescriptionORM(
            text=job_data.get('text', ''),
            filename=job_data.get('filename', None)
        )
        db.add(job)
        db.commit()
        db.refresh(job)
        return job.id
    finally:
        db.close()

def save_to_db(data: dict, collection_name: str) -> int:
    """Save analysis or other data to PostgreSQL using SQLAlchemy ORM"""
    db = SessionLocal()
    try:
        if collection_name == 'analyses':
            analysis = AnalysisORM(
                resume_id=data.get('resume_id'),
                job_description_id=data.get('job_description_id'),
                fit_status=data.get('fit_status'),
                score=data.get('score'),
                improved_resume=data.get('improved_resume', None),
                created_at=datetime.utcnow()
            )
            db.add(analysis)
            db.commit()
            db.refresh(analysis)
            return analysis.id
        else:
            raise ValueError(f"Unknown collection_name: {collection_name}")
    finally:
        db.close()