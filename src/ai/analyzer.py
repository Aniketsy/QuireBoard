from datetime import datetime
from src.utils.parser import save_resume_to_db, save_job_description_to_db, parse_resume, parse_job_description, save_to_db
import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class Analyzer:
    def __init__(self):
        # Load spacy model once during initialization
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
            # Preprocess texts
            resume_doc = self.nlp(str(resume).lower())
            job_doc = self.nlp(str(job_description).lower())
        
            # Remove stopwords and lemmatize
            resume_processed = ' '.join([token.lemma_ for token in resume_doc 
                                if not token.is_stop and not token.is_punct])
            job_processed = ' '.join([token.lemma_ for token in job_doc 
                                if not token.is_stop and not token.is_punct])
        
            # Create TF-IDF vectors
            vectors = self.vectorizer.fit_transform([resume_processed, job_processed])
        
            # Calculate cosine similarity
            similarity = cosine_similarity(vectors[0:1], vectors[1:2])[0][0]
        
            # Convert similarity to percentage score (0-100)
            score = int(similarity * 100)
        
            # Keywords matching bonus
            keywords = set(job_processed.split())
            resume_words = set(resume_processed.split())
            keyword_match_ratio = len(keywords.intersection(resume_words)) / len(keywords)
        
            # Add keyword matching bonus (up to 20 points)
            final_score = min(100, score + (keyword_match_ratio * 20))
        
            return final_score
        
        except Exception as e:
            print(f"Error calculating fit score: {str(e)}")
            return 0
        
    def analyze_and_store(self, resume_file, job_description):
        try:
            # Parse and store resume
            resume_data = parse_resume(resume_file)
            resume_id = save_resume_to_db(resume_data)
            
            # Parse and store job description
            job_data = {
                'description': parse_job_description(job_description),
                'title': 'Job Position'
            }
            job_id = save_job_description_to_db(job_data)
            
            # Perform analysis
            score = self.calculate_fit_score(resume_data['experience'], job_data['description'])
            status = self.evaluate_fit(resume_data['experience'], job_data['description'])
            
            # Store analysis result
            analysis_result = {
                'resume_id': resume_id,
                'job_id': job_id,
                'score': score,
                'status': status,
                'created_at': datetime.utcnow()
            }
            save_to_db(analysis_result, 'analyses')

            return {
                'score': score,
                'status': status,
                'resume_id': resume_id,
                'job_id': job_id
            }
            
        except Exception as e:
            print(f"Analysis error: {str(e)}")
            raise