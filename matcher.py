import os
import fitz  # PyMuPDF
from docx import Document
import google.generativeai as genai
from dotenv import load_dotenv
import time

# === Load API Key from .env ===
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# === Read file content safely ===
def read_file_text(file_path):
    ext = file_path.rsplit('.', 1)[-1].lower()

    if not os.path.exists(file_path):
        print(f"❌ File not found: {file_path}")
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
        print(f"❌ Error reading {file_path}: {e}")
        return ""
    return ""

# === Gemini Matching Logic ===
def match_resumes(resume_folder, jd_folder):
    jd_texts = []
    for jd_file in os.listdir(jd_folder):
        jd_path = os.path.join(jd_folder, jd_file)
        jd_content = read_file_text(jd_path)
        if jd_content:
            jd_texts.append(jd_content)

    jd_combined = "\n\n".join(jd_texts).strip()

    if not jd_combined:
        print("⚠️ No JD content found.")
        return []

    model = genai.GenerativeModel("gemini-2.0-flash")
    candidates = []

    for resume_file in os.listdir(resume_folder):
        resume_path = os.path.join(resume_folder, resume_file)
        resume_text = read_file_text(resume_path).strip()

        if not resume_text:
            print(f"⚠️ Skipping empty resume: {resume_file}")
            continue

        prompt = f"""
You are a resume screening assistant. Match the following resume against the job descriptions provided.

--- JOB DESCRIPTION ---
{jd_combined}

--- RESUME ---
{resume_text}

Your task has 2 parts:

PART 1 (For Table Display Only):
1. Candidate Name (extract the full name from the resume content)
2. A rating out of 5 (based on skills, experience, and education match)
3. One-line Skill/Profile Summary
4. Shortlist Reasons (at least 2 bullet points for why candidate matches)

PART 2 (For CSV Export Only, NOT for table):
Extract the following details (write '-' if not found):
- Email address
- Phone number (if available)
- Education Summary (e.g., BTech in Computer Engineering from XYZ University)
- Experience Summary (e.g., “3 years in Web Development”)
- Current Job Title (if any)
- LinkedIn or Portfolio Links
- Matched Job Title / Role

Respond strictly in this format:

Name: <name>
Rating: <rating>/5
Skill: <summary>
Reasons:
- <reason 1>
- <reason 2>
Email: <email>
Phone: <phone>
Education: <education summary>
Experience: <experience summary>
Current Title: <current job title>
Links: <linkedin or portfolio>
Matched Role: <role>
"""

        try:
            response = model.generate_content(prompt)
            output = response.text.strip()

            # === Use filename as fallback if name is not found ===
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
            links = "-"
            matched_role = "-"

            for line in output.splitlines():
                line = line.strip()
                if line.lower().startswith("name:"):
                    parsed_name = line.split(":", 1)[1].strip()
                    if parsed_name and parsed_name.lower() != "name not found":
                        name = parsed_name
                    else:
                        name = default_name
                elif line.lower().startswith("rating:"):
                    rating = line.split(":", 1)[1].strip().split("/")[0]
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
                elif line.lower().startswith("links:"):
                    links = line.split(":", 1)[1].strip() or "-"
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
                "links": links,
                "matched_role": matched_role
            })

        except Exception as e:
            print(f"❌ Gemini failed for {resume_file}: {e}")
            if "429" in str(e):
                print("⏳ Rate limit hit. Waiting before retrying...")
                time.sleep(60)
            continue

    return sorted(candidates, key=lambda x: x["score"], reverse=True)[:5]

