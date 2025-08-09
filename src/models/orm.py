from sqlalchemy import Column, Integer, String, Text, DateTime
from src.config.database import Base
from datetime import datetime

class ResumeORM(Base):
    __tablename__ = 'resumes'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255))
    contact = Column(Text)
    education = Column(Text)
    experience = Column(Text)
    skills = Column(Text)
    summary = Column(Text)
    achievements = Column(Text)
    user_id = Column(String(255), nullable=True)
    filename = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class JobDescriptionORM(Base):
    __tablename__ = 'job_descriptions'
    id = Column(Integer, primary_key=True, index=True)
    text = Column(Text)
    filename = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class AnalysisORM(Base):
    __tablename__ = 'analyses'
    id = Column(Integer, primary_key=True, index=True)
    resume_id = Column(Integer)
    job_description_id = Column(Integer)
    fit_status = Column(String(50))
    score = Column(Integer)
    improved_resume = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
