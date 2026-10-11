
from fastapi import FastAPI, UploadFile, File, Form, HTTPException, Request
from fastapi.templating import Jinja2Templates
from pypdf import PdfReader
from pathlib import Path
from io import BytesIO
import re

app = FastAPI(title="AI Resume Analyzer")
templates = Jinja2Templates(directory=str(Path(__file__).parent / "templates"))

SKILLS_LIST = [
    "python", "java", "c", "c++", "c#", "sql",
    "html", "css", "javascript", "fastapi",
    "django", "flask", "pandas", "numpy",
    "machine learning", "deep learning",
    "scikit-learn", "tensorflow", "pytorch",
    "selenium", "git", "github", "flutter",
    "dart", "firebase", "excel", "power bi",
    "tableau", "aws", "azure", "docker",
    "rest api", "data analysis", "nlp"
]

def extract_pdf_text(pdf_bytes):
    reader = PdfReader(BytesIO(pdf_bytes))
    text_parts = []
    for page in reader.pages:
        page_text = page.extract_text(extraction_mode="layout") or ""
        text_parts.append(page_text)
    return "\n".join(text_parts)

def clean_text(text):
    return " ".join(text.split()).lower()

def extract_skills(text):
    found_skills = []
    for skill in SKILLS_LIST:
        pattern = r"(?<!\w)" + re.escape(skill) + r"(?!\w)"
        if re.search(pattern, text):
            found_skills.append(skill)
    return found_skills

def compare_skills(resume_skills, job_skills):
    matched = [skill for skill in job_skills if skill in resume_skills]
    missing = [skill for skill in job_skills if skill not in resume_skills]
    if job_skills:
        score = len(matched) / len(job_skills) * 100
    else:
        score = 0
    return matched, missing, score


def generate_suggestions(missing_skills):
    suggestions = []

    for skill in missing_skills:
        suggestions.append(
            f"If you have experience with {skill}, "
            f"include it clearly in your resume."
        )

    if not missing_skills:
        suggestions.append(
            "Your resume contains all the skills detected "
            "in the job description. Review your projects "
            "and experience for relevance."
        )

    return suggestions


@app.get("/")
def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html"
    )

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.post("/analyze")
async def analyze_resume(
    resume: UploadFile = File(...),
    job_description: str = Form(...)
):
    if not resume.filename or Path(resume.filename).suffix.lower() != ".pdf":
        raise HTTPException(
            status_code=400,
            detail="Please upload a PDF resume."
        )

    if not job_description.strip():
        raise HTTPException(
            status_code=400,
            detail="Please enter a job description."
        )

    try:
        pdf_bytes = await resume.read()
        raw_text = extract_pdf_text(pdf_bytes)
    except Exception:
        raise HTTPException(
            status_code=400,
            detail="Could not read this PDF."
        )
    finally:
        await resume.close()

    if not raw_text.strip():
        raise HTTPException(
            status_code=400,
            detail="No selectable text found. Scanned PDFs need OCR."
        )

    cleaned_text = clean_text(raw_text)
    resume_skills = extract_skills(cleaned_text)
    job_text = clean_text(job_description)
    job_skills = extract_skills(job_text)

    matched, missing, score = compare_skills(resume_skills, job_skills)
    suggestions = generate_suggestions(missing)

    return {
        "resume_filename": resume.filename,
        "resume_skills": resume_skills,
        "job_skills": job_skills,
        "matched_skills": matched,
        "missing_skills": missing,
        "match_score": round(score, 2),
        "suggestions": suggestions
    }
