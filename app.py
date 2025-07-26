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

# ✅ Updated to store uploads inside static/uploads/
UPLOAD_FOLDER = os.path.join('static', 'uploads' , 'job_descriptions')
RESUME_FOLDER = os.path.join(UPLOAD_FOLDER, 'resumes')
JD_FOLDER = os.path.join(UPLOAD_FOLDER, 'job_descriptions')

ALLOWED_RESUME_EXT = {'pdf', 'docx'}
ALLOWED_JD_EXT = {'pdf', 'txt', 'docx'}

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

    for folder in [RESUME_FOLDER, JD_FOLDER]:
        for f in os.listdir(folder):
            try:
                file_path = os.path.join(folder, f)
                os.remove(file_path)
            except PermissionError:
                print(f"⚠️ Skipping locked file: {file_path}")
                time.sleep(1)

    for file in resume_files:
        if file and file.filename != '':
            ext = file.filename.rsplit('.', 1)[-1].lower()
            if ext == 'zip' and zipfile.is_zipfile(file):
                zip_path = os.path.join(RESUME_FOLDER, secure_filename(file.filename))
                file.save(zip_path)
                with zipfile.ZipFile(zip_path) as zip_ref:
                    zip_ref.extractall(RESUME_FOLDER)
                os.remove(zip_path)
            elif allowed_file(file.filename, ALLOWED_RESUME_EXT):
                filename = secure_filename(file.filename)
                file.save(os.path.join(RESUME_FOLDER, filename))

    for file in jd_files:
        if file and allowed_file(file.filename, ALLOWED_JD_EXT):
            filename = secure_filename(file.filename)
            file.save(os.path.join(JD_FOLDER, filename))

    top_candidates = match_resumes(RESUME_FOLDER, JD_FOLDER)

    for c in top_candidates:
        c["resume_url"] = url_for("download_resume", filename=c.get("file", "N/A"))

    session['candidates'] = top_candidates

    return redirect(url_for('show_results'))

@app.route('/results')
def show_results():
    candidates = session.get('candidates', [])
    return render_template('result.html', candidates=candidates)

# ✅ This now correctly matches static/uploads/resumes/
@app.route('/download/<path:filename>')
def download_resume(filename):
    resume_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), 'static', 'uploads', 'resumes'))
    return send_from_directory(resume_folder, filename, as_attachment=True)

@app.route('/export_csv', methods=['POST'])
def export_csv():
    candidates = session.get('candidates', [])

    output = io.StringIO()
    writer = csv.writer(output)

    writer.writerow([
        "Candidate Name",
        "Email Address",
        "Phone Number (if available)",
        "Resume Score / Match Score",
        "Key Skills Matched",
        "Education Summary",
        "Experience Summary",
        "Current Job Title (if parsed)",
        "LinkedIn or Portfolio Links (if available)",
        "Matched Job Title / Role",
        "Reason for Shortlisting"
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

# ✅ FINAL UPDATED BLOCK FOR RENDER COMPATIBILITY
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
