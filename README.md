# AI-Adaptive Onboarding Engine

An AI-driven adaptive learning engine that parses a new hire's resume and a target job description, identifies skill gaps, and generates a personalized, optimized training pathway.

---

## How It Works (Skill-Gap Analysis Logic)

1. **Document Parsing** — Resumes and JDs (PDF/TXT) are parsed using `pdfplumber` to extract raw text.
2. **LLM Skill Extraction** — Llama 3.2 (via Ollama) extracts structured skill lists with proficiency levels from both documents.
3. **Gap Analysis** — Candidate skills are compared against JD requirements. Gaps are classified as `missing_skill` or `level_upgrade`.
4. **Adaptive Pathing Algorithm** — A custom graph-based topological sort orders learning modules by skill dependencies. Must-have gaps are prioritized over nice-to-have. Missing prerequisites are automatically injected.
5. **Grounded Recommendations** — All course recommendations come strictly from a curated `course_catalog.py` — zero hallucinations.
6. **Reasoning Trace** — Every decision in the pathway is explained step-by-step.

---

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | React 18, Tailwind CSS |
| Backend | FastAPI, Python 3.11 |
| LLM | Llama 3.2 (Ollama — local, no API key needed) |
| PDF Parsing | pdfplumber |
| Adaptive Logic | Custom graph-based topological sort |
| Containerization | Docker, docker-compose |

---

## Setup Instructions

### Prerequisites
- Python 3.11+
- Node.js 18+
- [Ollama](https://ollama.com) installed and running

### 1. Clone the repo
```bash
git clone https://github.com/your-username/adaptive-onboarding.git
cd adaptive-onboarding
```

### 2. Start Ollama and pull the model
```bash
ollama serve
ollama pull llama3.2
```

### 3. Backend setup
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload --port 8001
```

### 4. Frontend setup (new terminal)
```bash
cd frontend
npm install
npm start
```

Open [http://localhost:3000](http://localhost:3000)

---

## Docker (Optional)

```bash
docker-compose up --build
```

Open [http://localhost:8001](http://localhost:8001)

---

## Dependencies

**Backend:** `fastapi`, `uvicorn`, `pdfplumber`, `python-dotenv`, `pydantic`, `python-multipart`, `aiofiles`

**Frontend:** `react`, `react-dom`, `axios`

---

## Datasets & Models

- **LLM:** Llama 3.2 via Ollama (local inference, no API key required)
- **Course Catalog:** Manually curated from public sources (Coursera, Google, AWS Training, MDN, etc.)
- **Reference Datasets:**
  - [Kaggle Resume Dataset](https://www.kaggle.com/datasets/snehaanbhawal/resume-dataset/data)
  - [O*NET Occupational Database](https://www.onetcenter.org/db_releases.html)
  - [Jobs & Job Descriptions](https://www.kaggle.com/datasets/kshitizregmi/jobs-and-job-description)
