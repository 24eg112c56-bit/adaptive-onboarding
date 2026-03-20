# AI-Adaptive Onboarding Engine

An AI-driven adaptive learning engine that parses a new hire's resume and a target job description, identifies skill gaps, and generates a personalized, optimized training pathway.

🌐 **Live Demo:** [https://adaptive-onboarding.onrender.com](https://adaptive-onboarding.onrender.com)

---

## How It Works (Skill-Gap Analysis Logic)

1. **Document Parsing** — Resumes and JDs (PDF/TXT) are parsed using `pdfplumber` to extract raw text.
2. **LLM Skill Extraction** — Google Gemini 2.0 Flash extracts structured skill lists with proficiency levels from both documents.
3. **Fallback Extractor** — If LLM is unavailable, a rule-based extractor ensures zero downtime.
4. **Gap Analysis** — Candidate skills are compared against JD requirements. Gaps are classified as `missing_skill` or `level_upgrade`.
5. **Adaptive Pathing Algorithm** — A custom graph-based topological sort orders learning modules by skill dependencies. Must-have gaps are prioritized. Missing prerequisites are automatically injected.
6. **Grounded Recommendations** — All course recommendations come strictly from a curated `course_catalog.py` — zero hallucinations.
7. **Reasoning Trace** — Every decision in the pathway is explained step-by-step.

---

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | HTML, Tailwind CSS (served via FastAPI) |
| Backend | FastAPI, Python 3.11 |
| LLM | Google Gemini 2.0 Flash |
| Fallback | Rule-based skill extractor |
| PDF Parsing | pdfplumber |
| Adaptive Logic | Custom graph-based topological sort |
| Deployment | Render.com |
| Containerization | Docker (optional) |

---

## Setup Instructions (Local)

### Prerequisites
- Python 3.11+
- A Gemini API key ([get one free here](https://aistudio.google.com/app/apikey))

### 1. Clone the repo
```bash
git clone https://github.com/24eg112c56-bit/adaptive-onboarding.git
cd adaptive-onboarding
```

### 2. Install dependencies
```bash
cd backend
pip install -r requirements.txt
```

### 3. Add your API key
```bash
cp .env.example .env
# Edit .env and add your GEMINI_API_KEY
```

### 4. Run the server
```bash
python -m uvicorn main:app --port 8000
```

Open [http://localhost:8000](http://localhost:8000)

---

## Docker (Optional)

```bash
docker-compose up --build
```

---

## Dependencies

`fastapi`, `uvicorn`, `pdfplumber`, `google-genai`, `python-dotenv`, `pydantic`, `python-multipart`, `aiofiles`

---

## Datasets & Models

- **LLM:** Google Gemini 2.0 Flash (skill extraction)
- **Fallback:** Custom rule-based extractor (zero downtime)
- **Course Catalog:** Curated from Coursera, Google, AWS Training, MDN, etc.
- **Reference Datasets:**
  - [Kaggle Resume Dataset](https://www.kaggle.com/datasets/snehaanbhawal/resume-dataset/data)
  - [O*NET Occupational Database](https://www.onetcenter.org/db_releases.html)
  - [Jobs & Job Descriptions](https://www.kaggle.com/datasets/kshitizregmi/jobs-and-job-description)
