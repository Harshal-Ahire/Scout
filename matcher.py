import os
import time
import fitz  # PyMuPDF
from docx import Document
from google import genai
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

def read_file_text(file_path):
    """Safely reads text content from PDF, DOCX, or TXT files."""
    ext = file_path.rsplit('.', 1)[-1].lower()

    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return ""

    try:
        if ext == 'pdf':
            doc = fitz.open(file_path)
            return " ".join([page.get_text() for page in doc])
        elif ext == 'docx':
            return "\n".join([para.text for para in Document(file_path).paragraphs])
        elif ext == 'txt':
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return ""

    return ""

def match_resumes(resume_folder, jd_folder):
    """Processes resumes and job descriptions using Gemini to find the best matches."""
    jd_texts = []
    for jd_file in os.listdir(jd_folder):
        jd_path = os.path.join(jd_folder, jd_file)
        jd_content = read_file_text(jd_path)
        if jd_content:
            jd_texts.append(jd_content)

    jd_combined = "\n\n".join(jd_texts).strip()

    if not jd_combined:
        print("No Job Description content found.")
        return []

    candidates = []

    for resume_file in os.listdir(resume_folder):
        resume_path = os.path.join(resume_folder, resume_file)
        resume_text = read_file_text(resume_path).strip()

        if not resume_text:
            print(f"Skipping empty resume: {resume_file}")
            continue

        prompt = f"""
You are a senior technical recruiter and resume screening expert. Your job is to evaluate how well a candidate's resume matches a given job description.

--- JOB DESCRIPTION ---
{jd_combined}

--- RESUME ---
{resume_text}

Evaluate the resume against the job description using these strict criteria:

SCORING GUIDE (out of 5):
- 5.0: Perfect match — candidate meets 90%+ of required skills, experience level, and role
- 4.0-4.9: Strong match — meets 70-89% of requirements, minor gaps only
- 3.0-3.9: Moderate match — meets 50-69%, some key skills missing
- 2.0-2.9: Weak match — meets 30-49%, significant gaps
- 1.0-1.9: Poor match — meets less than 30% of requirements
- 0.0: No match — completely unrelated profile

SHORTLISTING RULES:
- Only recommend shortlisting if score is 3.5 or above
- Be strict about required technical skills listed in the JD
- Transferable skills count but weigh less than direct experience
- Student/fresher profiles can score high if projects strongly align with JD requirements
- Extract exactly 3 key skills from the resume that directly match the JD (comma separated, no long sentences)

EXTRACT THESE DETAILS CAREFULLY:
- Full name from resume header
- Email address (look for @ symbol)
- Phone number (digits, may have country code)
- Education: degree + field + university + year (e.g. B.E. Computer Engineering, XYZ University, 2026)
- Experience: total years if working, or "Fresher with X projects" if student
- Current Job Title: actual job title if employed, or "Student" if currently studying
- LinkedIn URL and GitHub URL separately (look for linkedin.com and github.com links)
- Matched Role: the specific job title from the JD this resume best fits

Respond ONLY in this exact format, no extra text:

Name: <full name>
Rating: <number only, e.g. 3.5>/5
Skill: <exactly 3 comma-separated skills that match JD>
Reasons:
- <specific reason 1 citing JD requirement and resume evidence>
- <specific reason 2 citing JD requirement and resume evidence>
- <specific reason 3 citing JD requirement and resume evidence>
Email: <email>
Phone: <phone>
Education: <degree, university, year>
Experience: <years or fresher status>
Current Title: <job title or Student>
LinkedIn: <linkedin url or ->
GitHub: <github url or ->
Matched Role: <role from JD>
"""

        output = ""
        for attempt in range(3):
            try:
                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=prompt,
                )
                output = response.text.strip()
                print(f"Successfully processed: {resume_file}")
                break

            except Exception as e:
                print(f"Attempt {attempt + 1} failed for {resume_file}: {e}")
                if "503" in str(e) or "UNAVAILABLE" in str(e):
                    print(f"Gemini busy, retrying in 5 seconds...")
                    time.sleep(5)
                    continue
                elif "429" in str(e) or "RESOURCE_EXHAUSTED" in str(e):
                    print("Quota limit hit. Waiting 15 seconds before next resume...")
                    time.sleep(15)
                    break
                else:
                    break

        if not output:
            print(f"All attempts failed for {resume_file}, skipping.")
            time.sleep(3)
            continue

        # Parse response
        default_name = os.path.splitext(resume_file)[0]
        name = default_name
        rating = "0"
        skill = "-"
        reasons = []
        email = "-"
        phone = "-"
        education = "-"
        experience = "-"
        current_title = "-"
        linkedin = "-"
        github = "-"
        matched_role = "-"

        for line in output.splitlines():
            line = line.strip()
            if line.lower().startswith("name:"):
                parsed_name = line.split(":", 1)[1].strip()
                name = parsed_name if parsed_name and parsed_name.lower() != "name not found" else default_name
            elif line.lower().startswith("rating:"):
                rating = line.split(":", 1)[1].strip().split("/")[0].strip()
            elif line.lower().startswith("skill:"):
                skill = line.split(":", 1)[1].strip() or "-"
            elif line.startswith("-"):
                reasons.append(line)
            elif line.lower().startswith("email:"):
                email = line.split(":", 1)[1].strip() or "-"
            elif line.lower().startswith("phone:"):
                phone = line.split(":", 1)[1].strip() or "-"
            elif line.lower().startswith("education:"):
                education = line.split(":", 1)[1].strip() or "-"
            elif line.lower().startswith("experience:"):
                experience = line.split(":", 1)[1].strip() or "-"
            elif line.lower().startswith("current title:"):
                current_title = line.split(":", 1)[1].strip() or "-"
            elif line.lower().startswith("linkedin:"):
                linkedin = line.split(":", 1)[1].strip() or "-"
            elif line.lower().startswith("github:"):
                github = line.split(":", 1)[1].strip() or "-"
            elif line.lower().startswith("matched role:"):
                matched_role = line.split(":", 1)[1].strip() or "-"

        candidates.append({
            "name": name,
            "score": float(rating) if rating.replace('.', '', 1).isdigit() else 0.0,
            "skill": skill,
            "reason": "<br>".join(reasons) if reasons else "-",
            "file": resume_file,
            "email": email,
            "phone": phone,
            "education": education,
            "experience": experience,
            "current_title": current_title,
            "linkedin": linkedin,
            "github": github,
            "matched_role": matched_role
        })

        # Pause between resumes to avoid overwhelming the API
        time.sleep(4)

    return sorted(candidates, key=lambda x: x["score"], reverse=True)[:5]
