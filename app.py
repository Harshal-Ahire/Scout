from flask import Flask, render_template, request, redirect, flash, send_from_directory, url_for, session, send_file 
import os
import zipfile
import time
import io
import csv
from werkzeug.utils import secure_filename
from matcher import match_resumes

app = Flask(__name__)
app.secret_key = 'scout_secret_key'

# Define directory paths for uploads
UPLOAD_FOLDER = os.path.join('static', 'uploads')
RESUME_FOLDER = os.path.join(UPLOAD_FOLDER, 'resumes')
JD_FOLDER = os.path.join(UPLOAD_FOLDER, 'job_descriptions')

# Define allowed file extensions
ALLOWED_RESUME_EXT = {'pdf', 'docx'}
ALLOWED_JD_EXT = {'pdf', 'txt', 'docx'}

# Ensure upload directories exist
os.makedirs(RESUME_FOLDER, exist_ok=True)
os.makedirs(JD_FOLDER, exist_ok=True)

def allowed_file(filename, allowed_exts):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_exts

@app.route('/')
def landing_page():
    return render_template('landing.html')

@app.route('/upload')
def upload_page():
    return render_template('upload.html')

@app.route('/upload', methods=['POST'])
def upload_files():
    resume_files = request.files.getlist('resumes')
    jd_files = request.files.getlist('jds')

    # Clear previous uploads to maintain a clean workspace
    for folder in [RESUME_FOLDER, JD_FOLDER]:
        for f in os.listdir(folder):
            try:
                file_path = os.path.join(folder, f)
                os.remove(file_path)
            except PermissionError:
                # Log issues with locked files and attempt a brief delay
                print(f"File access denied, skipping: {file_path}")
                time.sleep(1)

    for file in resume_files:
        if file and file.filename != '':
            ext = file.filename.rsplit('.', 1)[-1].lower()
            
            # Handle ZIP archives by extracting contents to the resume folder
            if ext == 'zip' and zipfile.is_zipfile(file):
                # Reset file pointer to ensure the entire stream is read
                file.seek(0) 
                
                zip_path = os.path.join(RESUME_FOLDER, secure_filename(file.filename))
                file.save(zip_path)
                
                with zipfile.ZipFile(zip_path) as zip_ref:
                    zip_ref.extractall(RESUME_FOLDER)
                
                # Clean up the temporary ZIP file after extraction
                os.remove(zip_path)
            
            # Process standard individual file uploads
            elif allowed_file(file.filename, ALLOWED_RESUME_EXT):
                filename = secure_filename(file.filename)
                file.save(os.path.join(RESUME_FOLDER, filename))

    for file in jd_files:
        if file and allowed_file(file.filename, ALLOWED_JD_EXT):
            filename = secure_filename(file.filename)
            file.save(os.path.join(JD_FOLDER, filename))

    # Execute matching logic and generate results
    top_candidates = match_resumes(RESUME_FOLDER, JD_FOLDER)

    for c in top_candidates:
        c["resume_url"] = url_for("download_resume", filename=c.get("file", "N/A"))

    # Store results in session for persistence across routes
    session['candidates'] = top_candidates

    return redirect(url_for('show_results'))

@app.route('/results')
def show_results():
    candidates = session.get('candidates', [])
    return render_template('result.html', candidates=candidates)

@app.route('/download/<path:filename>')
def download_resume(filename):
    # Using absolute path resolution for reliable file retrieval
    resume_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), 'static', 'uploads', 'resumes'))
    return send_from_directory(resume_folder, filename, as_attachment=True)

@app.route('/export_csv', methods=['POST'])
def export_csv():
    candidates = session.get('candidates', [])

    output = io.StringIO()
    writer = csv.writer(output)

    # Define CSV Header
    writer.writerow([
        "Candidate Name",
        "Email Address",
        "Phone Number",
        "Match Score",
        "Key Skills Matched",
        "Education Summary",
        "Experience Summary",
        "Current Job Title",
        "Links",
        "Matched Role",
        "Shortlisting Reason"
    ])

    for c in candidates:
        writer.writerow([
            c.get("name", "-"),
            c.get("email", "-"),
            c.get("phone", "-"),
            f"{c.get('score', '-')}/5",
            c.get("skill", "-"),
            c.get("education", "-"),
            c.get("experience", "-"),
            c.get("current_title", "-"),
            c.get("links", "-"),
            c.get("matched_role", "-"),
            c.get("reason", "-").replace("<br>", " | ")
        ])

    output.seek(0)
    return send_file(
        io.BytesIO(output.getvalue().encode('utf-8')),
        mimetype='text/csv',
        as_attachment=True,
        download_name='top_candidates.csv'
    )

if __name__ == '__main__':
    app.run(debug=True)
