import json
import urllib.request

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3.2"

RESUME_PROMPT = """You are an expert HR analyst. Extract skills from the resume below.
Return a JSON object with this exact structure:
{{
  "skills": [
    {{"name": "skill name", "level": "beginner|intermediate|advanced", "years": 0}}
  ],
  "experience_years": 0,
  "current_role": "job title or null"
}}
Only return valid JSON, no extra text, no markdown fences.

Resume:
{text}
"""

JD_PROMPT = """You are an expert HR analyst. Extract required skills from the job description below.
Return a JSON object with this exact structure:
{{
  "required_skills": [
    {{"name": "skill name", "required_level": "beginner|intermediate|advanced", "priority": "must-have|nice-to-have"}}
  ],
  "role_title": "job title",
  "domain": "technical|operational|managerial|other"
}}
Only return valid JSON, no extra text, no markdown fences.

Job Description:
{text}
"""

def clean_json(raw: str) -> str:
    raw = raw.strip()
    if raw.startswith("```"):
        lines = raw.split("\n")
        lines = [l for l in lines if not l.startswith("```")]
        raw = "\n".join(lines)
    return raw.strip()

def call_ollama(prompt: str) -> str:
    payload = json.dumps({
        "model": MODEL,
        "prompt": prompt,
        "stream": False
    }).encode("utf-8")
    req = urllib.request.Request(
        OLLAMA_URL,
        data=payload,
        headers={"Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req, timeout=120) as res:
        result = json.loads(res.read().decode("utf-8"))
        return result["response"]

def extract_resume_skills(resume_text: str) -> dict:
    raw = call_ollama(RESUME_PROMPT.format(text=resume_text[:4000]))
    return json.loads(clean_json(raw))

def extract_jd_skills(jd_text: str) -> dict:
    raw = call_ollama(JD_PROMPT.format(text=jd_text[:4000]))
    return json.loads(clean_json(raw))
