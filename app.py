from flask import Flask, render_template, request, redirect, flash, send_from_directory, url_for, session, send_file
import os
import zipfile
import time
import io
import csv
from werkzeug.utils import secure_filename
from matcher import match_resumes  # Gemini logic happens here

app = Flask(__name__)
app.secret_key = 'scout_secret_key'

UPLOAD_FOLDER_JD = 'static/uploads/job_descriptions'
UPLOAD_FOLDER_RESUME = 'static/uploads/resumes'

os.makedirs(UPLOAD_FOLDER_JD, exist_ok=True)
os.makedirs(UPLOAD_FOLDER_RESUME, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'jd' not in request.files or 'resumes' not in request.files:
        flash('No file part')
        return redirect(request.url)

    jd_file = request.files['jd']
    resume_files = request.files.getlist('resumes')

    if jd_file.filename == '' or all(resume.filename == '' for resume in resume_files):
        flash('No selected file')
        return redirect(request.url)

    jd_filename = secure_filename(jd_file.filename)
    jd_path = os.path.join(UPLOAD_FOLDER_JD, jd_filename)
    jd_file.save(jd_path)

    saved_resume_paths = []
    for resume in resume_files:
        if resume and resume.filename:
            resume_filename = secure_filename(resume.filename)
            resume_path = os.path.join(UPLOAD_FOLDER_RESUME, resume_filename)
            resume.save(resume_path)
            saved_resume_paths.append(resume_path)

    matched_results = match_resumes(jd_path, saved_resume_paths)

    # Store matched results in session for download
    session['matched_results'] = matched_results

    return render_template('result.html', matched_results=matched_results)

@app.route('/download/<path:filename>')
def download_resume(filename):
    resume_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), 'static', 'uploads', 'resumes'))
    return send_from_directory(resume_folder, filename, as_attachment=True)

@app.route('/download_csv')
def download_csv():
    matched_results = session.get('matched_results', [])

    if not matched_results:
        flash('No data to download.')
        return redirect(url_for('index'))

    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=matched_results[0].keys())
    writer.writeheader()
    writer.writerows(matched_results)

    mem = io.BytesIO()
    mem.write(output.getvalue().encode('utf-8'))
    mem.seek(0)

    return send_file(mem,
                     mimetype='text/csv',
                     download_name='matched_results.csv',
                     as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
