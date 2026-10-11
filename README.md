# Resume Analyzer 📄

A Python-based web application that compares a resume with a job description and identifies matching and missing skills.

## 🚀 Features

- Upload a resume in PDF format.
- Extract text from PDF resumes.
- Detect skills from the resume and job description.
- Calculate a resume-to-job skill match percentage.
- Display matched and missing skills.
- Download the analysis report as a Microsoft Word document (`.docx`).

## 🛠️ Technologies Used

- **Python** — core programming language
- **FastAPI** — backend framework
- **HTML and CSS** — webpage design
- **JavaScript** — frontend functionality
- **PyPDF** — PDF text extraction
- **python-docx library in the browser** — Word report generation through the `docx` JavaScript library

## 📂 Project Structure

```text
Resume_Analyzer/
├── app.py
├── main.py
├── requirements.txt
├── README.md
├── .gitignore
└── templates/
    └── index.html
```

## ⚙️ Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/rautsamiksha0311/Resume_Analyzer.git
cd Resume_Analyzer
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

### 3. Activate the virtual environment

**Windows:**

```bash
venv\Scripts\activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Run the application

```bash
python -m uvicorn app:app --reload
```

### 6. Open the application

Visit http://127.0.0.1:8000/ in your browser.

## 📊 How It Works

1. Upload a PDF resume.
2. Paste the job description.
3. Click **Analyze Resume**.
4. View the match percentage, detected resume skills, matched skills, and missing skills.
5. Download the analysis report as a Word document.

## 🧠 Current Analysis Method

The current version uses rule-based skill extraction and matching against a predefined skills list. The match percentage represents the proportion of detected job-description skills that also appear in the resume. It is not an official ATS score.

## 🔮 Future Improvements

- Add NLP-based semantic matching.
- Improve skill detection using machine learning.
- Support additional resume formats.
- Improve the user interface and analysis accuracy.

---

## 📜 License

This project is available for educational and portfolio purposes.

## 📞 Contact

For questions or suggestions, reach out at **rautsamiksha0811@gmail.com**
