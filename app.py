from flask import Flask, render_template, request, jsonify
from job_matcher import JobMatcher
from utils.resume_parser import parse_resume
import os
import json

app = Flask(__name__)
job_matcher = JobMatcher("data/job_listing.csv")

class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, float):
            return float(obj)
        return super().default(obj)

app.json_encoder = CustomJSONEncoder


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/candidate', methods=['GET', 'POST'])
def candidate():
    if request.method == 'POST':
        if 'resume' in request.files:
            file = request.files['resume']
            if file.filename != '':
                try:
                    recommendations = job_matcher.process_resume(file)
                    return jsonify({'recommendations': recommendations})
                except Exception as e:
                    return jsonify({'error': str(e)}), 400
        elif 'resume_text' in request.form:
            resume_text = request.form['resume_text']
            if resume_text.strip():
                try:
                    recommendations = job_matcher.process_resume(resume_text)
                    return jsonify({'recommendations': recommendations})
                except Exception as e:
                    return jsonify({'error': str(e)}), 400
        return jsonify({'error': 'No resume provided'}), 400
    return render_template('candidate.html')

@app.route('/employer', methods=['GET', 'POST'])
def employer():
    if request.method == 'POST':
        job_description = request.form['job_description']
        resumes = request.form.getlist('resumes')
        if job_description and resumes:
            matches = job_matcher.match_candidates(job_description, resumes)
            return jsonify({'matches': matches})
        return jsonify({'error': 'Missing job description or resumes'}), 400
    return render_template('employer.html')

if __name__ == '__main__':
    app.run(debug=True)