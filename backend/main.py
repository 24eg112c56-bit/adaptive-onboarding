from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from dotenv import load_dotenv
import traceback
import os

from parser import extract_text
from skill_extractor import extract_resume_skills, extract_jd_skills
from gap_analyzer import analyze_gap, build_learning_pathway

load_dotenv()

app = FastAPI(title="AI-Adaptive Onboarding Engine", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/analyze")
async def analyze(
    resume: UploadFile = File(...),
    job_description: UploadFile = File(...),
):
    try:
        resume_bytes = await resume.read()
        jd_bytes = await job_description.read()

        resume_text = extract_text(resume_bytes, resume.filename)
        jd_text = extract_text(jd_bytes, job_description.filename)

        if not resume_text:
            raise HTTPException(status_code=400, detail="Could not extract text from resume.")
        if not jd_text:
            raise HTTPException(status_code=400, detail="Could not extract text from job description.")

        resume_data = extract_resume_skills(resume_text)
        jd_data = extract_jd_skills(jd_text)

        gap_report = analyze_gap(resume_data, jd_data)
        pathway = build_learning_pathway(gap_report)

        return {
            "success": True,
            "resume_skills": resume_data,
            "jd_skills": jd_data,
            "gap_report": gap_report,
            "pathway": pathway,
        }

    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

# Serve frontend
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def serve_frontend():
    return FileResponse("static/index.html")
