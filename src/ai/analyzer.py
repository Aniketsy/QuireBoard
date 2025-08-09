from datetime import datetime
from src.utils.parser import parse_resume, parse_job_description
import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Import your new PostgreSQL/SQLAlchemy save functions
from src.config.database import SessionLocal
from src.models.orm import ResumeORM, JobDescriptionORM, AnalysisORM  

class Analyzer:
    def __init__(self):
        self.nlp = spacy.load('en_core_web_sm')
        self.vectorizer = TfidfVectorizer()

    def evaluate_fit(self, resume, job_description):
        score = self.calculate_fit_score(resume, job_description)
        if score < 50:
            return "not fit"
        elif 50 <= score < 75:
            return "good fit"
        else:
            return "best fit"

    def calculate_fit_score(self, resume, job_description):
        try:
            resume_doc = self.nlp(str(resume).lower())
            job_doc = self.nlp(str(job_description).lower())

            resume_processed = ' '.join([token.lemma_ for token in resume_doc
                                         if not token.is_stop and not token.is_punct])
            job_processed = ' '.join([token.lemma_ for token in job_doc
                                      if not token.is_stop and not token.is_punct])

            vectors = self.vectorizer.fit_transform([resume_processed, job_processed])
            similarity = cosine_similarity(vectors[0:1], vectors[1:2])[0][0]
            score = int(similarity * 100)

            keywords = set(job_processed.split())
            resume_words = set(resume_processed.split())
            keyword_match_ratio = len(keywords.intersection(resume_words)) / len(keywords) if keywords else 0

            final_score = min(100, score + (keyword_match_ratio * 20))
            return final_score

        except Exception as e:
            print(f"Error calculating fit score: {str(e)}")
            return 0

    def analyze_and_store(self, resume_file, job_description):
        try:
            db = SessionLocal()
            # Parse resume and job description
            resume_data = parse_resume(resume_file)
            job_desc_text = parse_job_description(job_description)

            # Save resume to DB
            resume_obj = ResumeORM(**resume_data)
            db.add(resume_obj)
            db.commit()
            db.refresh(resume_obj)

            # Save job description to DB
            job_obj = JobDescriptionORM(description=job_desc_text, title='Job Position')
            db.add(job_obj)
            db.commit()
            db.refresh(job_obj)

            # Perform analysis
            score = self.calculate_fit_score(resume_data.get('experience', ''), job_desc_text)
            status = self.evaluate_fit(resume_data.get('experience', ''), job_desc_text)

            # Store analysis result
            analysis_result = AnalysisORM(
                resume_id=resume_obj.id,
                job_id=job_obj.id,
                score=score,
                status=status,
                created_at=datetime.utcnow()
            )
            db.add(analysis_result)
            db.commit()
            db.refresh(analysis_result)

            db.close()

            return {
                'score': score,
                'status': status,
                'resume_id': resume_obj.id,
                'job_id': job_obj.id
            }

        except Exception as e:
            print(f"Analysis error: {str(e)}")
            raise