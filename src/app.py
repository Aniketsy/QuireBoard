from flask import Flask, request, jsonify, render_template
from werkzeug.utils import secure_filename
import os
from src.utils.parser import parse_file, save_resume_to_db, save_job_description_to_db, save_to_db
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
            job_desc_id = save_job_description_to_db({'text': job_desc_text})
        else:
            job_desc_text = parse_file(job_desc)
            job_desc_id = save_job_description_to_db({'filename': job_desc.filename, 'text': job_desc_text})


        # Handle resumes
        resumes = request.files.getlist('resume')
        analyzer = Analyzer()
        generator = Generator()
        results = []
        analysis_db_records = []
        for resume_file in resumes:
            resume_text = parse_file(resume_file)
            fit_status = analyzer.evaluate_fit(resume_text, job_desc_text)
            score = analyzer.calculate_fit_score(resume_text, job_desc_text)
            resume_data = Resume.from_text(resume_text).to_dict()
            resume_id = save_resume_to_db({**resume_data, 'filename': resume_file.filename})

            result = {
                'filename': resume_file.filename,
                'status': fit_status,
                'score': score
            }

            analysis_record = {
                'resume_id': resume_id,
                'job_description_id': job_desc_id,
                'fit_status': fit_status,
                'score': score,
                'created_at': None  # Will be set by save_to_db
            }

            # Generate improved resume if it's not a good fit and only one resume was uploaded
            if len(resumes) == 1 and fit_status == "not fit":
                improved_resume = generator.generate_resume(job_desc_text, resume_data)
                result['improved_resume'] = improved_resume
                analysis_record['improved_resume'] = improved_resume

            analysis_id = save_to_db(analysis_record, 'analyses')
            result['analysis_id'] = analysis_id
            analysis_db_records.append(analysis_record)
            results.append(result)

        # Sort results by score
        results.sort(key=lambda x: x['score'], reverse=True)

        return jsonify({
            'multiple_resumes': len(resumes) > 1,
            'results': results
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)