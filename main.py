
from pypdf import PdfReader
from pathlib import Path
import re

def extract_text_from_pdf(filename):
    pdf_path = Path(filename)
    if not pdf_path.exists():
        raise FileNotFoundError(f"PDF file not found: {filename}")
    if pdf_path.suffix.lower() != ".pdf":
        raise ValueError("Please provide a PDF file.")
    reader = PdfReader(str(pdf_path))
    text_parts = []
    for page_number, page in enumerate(reader.pages, start=1):
        page_text = page.extract_text(extraction_mode="layout") or ""
        if page_text.strip():
            text_parts.append(page_text)
        else:
            print(f"Warning: No text extracted from page {page_number}.")
    return "\n".join(text_parts)

def clean_text(text):
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    text = " ".join(lines)
    text = " ".join(text.split())
    return text.lower()

def tokenize_text(text):
    return text.split()

def extract_skills(text):
    skills_list = [
        "python", "java", "c", "c++", "c#",
        "sql", "html", "css", "javascript",
        "fastapi", "django", "flask",
        "pandas", "numpy", "machine learning",
        "deep learning", "scikit-learn",
        "tensorflow", "pytorch", "selenium",
        "git", "github", "flutter", "dart",
        "firebase", "excel", "power bi",
        "tableau", "aws", "azure", "docker",
        "rest api", "data analysis", "nlp"
    ]

    found_skills = []

    for skill in skills_list:
        pattern = r"(?<!\w)" + re.escape(skill) + r"(?!\w)"
        if re.search(pattern, text):
            found_skills.append(skill)

    return found_skills

def compare_skills(resume_skills, job_skills):
    matched_skills = []
    missing_skills = []
    for skill in job_skills:
        if skill in resume_skills:
            matched_skills.append(skill)
        else:
            missing_skills.append(skill)
    if not job_skills:
        match_score = 0
    else:
        match_score = len(matched_skills) / len(job_skills) * 100
    return matched_skills, missing_skills, match_score

def main():
    filename = "cv.pdf"
    try:
        raw_text = extract_text_from_pdf(filename)
        cleaned_text = clean_text(raw_text)
        words = tokenize_text(cleaned_text)
        skills = extract_skills(cleaned_text)

        print("\n--- SKILLS FOUND IN RESUME ---")
        print(skills)
        print("Total skills found:", len(skills))

        print("\nEnter the job description below.")
        print("Type END on a new line when finished.")
        job_lines = []

        while True:
            line = input()
            if line.strip().upper() == "END":
                break
            job_lines.append(line)

        job_description = "\n".join(job_lines)
        job_text = clean_text(job_description)
        job_skills = extract_skills(job_text)

        matched, missing, score = compare_skills(skills, job_skills)

        print("\n--- JOB SKILLS ---")
        print(job_skills)
        print("\n--- MATCHED SKILLS ---")
        print(matched)
        print("\n--- MISSING SKILLS ---")
        print(missing)
        print(f"\n--- MATCH SCORE: {score:.2f}% ---")

        print("\nTotal words in resume:", len(words))

    except (FileNotFoundError, ValueError) as error:
        print("Error:", error)
    except Exception as error:
        print("Could not process the PDF:", error)

if __name__ == "__main__":
    main()
