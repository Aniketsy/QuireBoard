from flask import Flask, request, jsonify, render_template
from werkzeug.utils import secure_filename
import os
from src.utils.parser import parse_text_from_file
from src.ai.analyzer import Analyzer
from src.ai.generator import Generator
from src.models.resume import Resume

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        # Handle job description
        job_desc = request.files.get('job_description')
        if not job_desc:
            job_desc_text = request.form.get('job_description_text', '')
        else:
            job_desc_text = parse_text_from_file(job_desc)

        # Handle resumes
        resumes = request.files.getlist('resume')
        analyzer = Analyzer()
        generator = Generator()
        
        results = []
        for resume_file in resumes:
            resume_text = parse_text_from_file(resume_file)
            fit_status = analyzer.evaluate_fit(resume_text, job_desc_text)
            score = analyzer.calculate_fit_score(resume_text, job_desc_text)
            
            result = {
                'filename': resume_file.filename,
                'status': fit_status,
                'score': score
            }
            
            # Generate improved resume if it's not a good fit and only one resume was uploaded
            if len(resumes) == 1 and fit_status == "not fit":
                user_data = Resume.from_text(resume_text).to_dict()
                improved_resume = generator.generate_resume(job_desc_text, user_data)
                result['improved_resume'] = improved_resume
                
            results.append(result)
            
        # Sort results by score
        results.sort(key=lambda x: x['score'], reverse=True)
        
        return jsonify({
            'multiple_resumes': len(resumes) > 1,
            'results': results
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400