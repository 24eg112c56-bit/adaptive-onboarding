import json
import os
import re
from dotenv import load_dotenv

load_dotenv()

# Try Gemini, fall back to rule-based if unavailable
GEMINI_AVAILABLE = False
client = None

try:
    from google import genai
    api_key = os.getenv("GEMINI_API_KEY")
    if api_key:
        client = genai.Client(api_key=api_key)
        GEMINI_AVAILABLE = True
except Exception:
    pass

# ── Prompts ──────────────────────────────────────────────────────────────────

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

# ── Helpers ───────────────────────────────────────────────────────────────────

def clean_json(raw: str) -> str:
    raw = raw.strip()
    if raw.startswith("```"):
        lines = raw.split("\n")
        lines = [l for l in lines if not l.startswith("```")]
        raw = "\n".join(lines)
    return raw.strip()

# ── Rule-based fallback extractor ─────────────────────────────────────────────

KNOWN_SKILLS = [
    "python", "java", "javascript", "typescript", "c++", "c#", "go", "rust", "php", "ruby",
    "react", "angular", "vue", "node.js", "django", "flask", "fastapi", "spring",
    "sql", "mysql", "postgresql", "mongodb", "redis", "elasticsearch",
    "aws", "azure", "gcp", "docker", "kubernetes", "terraform", "ansible",
    "machine learning", "deep learning", "nlp", "data analysis", "data science",
    "pandas", "numpy", "scikit-learn", "tensorflow", "pytorch",
    "git", "linux", "devops", "ci/cd", "agile", "scrum",
    "communication", "leadership", "project management", "excel", "power bi",
    "cybersecurity", "networking", "html", "css", "rest api", "graphql",
]

SENIOR_KEYWORDS = ["senior", "lead", "principal", "architect", "manager", "director", "head"]
JUNIOR_KEYWORDS = ["junior", "intern", "trainee", "fresher", "entry"]

def detect_level(text: str, skill: str) -> str:
    text_lower = text.lower()
    # look for years near skill mention
    years_match = re.findall(r'(\d+)\+?\s*years?', text_lower)
    max_years = max([int(y) for y in years_match], default=0)
    if max_years >= 5:
        return "advanced"
    elif max_years >= 2:
        return "intermediate"
    for kw in SENIOR_KEYWORDS:
        if kw in text_lower:
            return "advanced"
    for kw in JUNIOR_KEYWORDS:
        if kw in text_lower:
            return "beginner"
    return "intermediate"

def detect_role(text: str) -> str:
    roles = [
        "software engineer", "data scientist", "data analyst", "ml engineer",
        "devops engineer", "frontend developer", "backend developer", "full stack developer",
        "product manager", "project manager", "business analyst", "qa engineer",
        "cloud architect", "security engineer", "mobile developer",
    ]
    text_lower = text.lower()
    for role in roles:
        if role in text_lower:
            return role.title()
    return "Professional"

def rule_based_resume(text: str) -> dict:
    text_lower = text.lower()
    found_skills = []
    for skill in KNOWN_SKILLS:
        if skill in text_lower:
            found_skills.append({
                "name": skill,
                "level": detect_level(text, skill),
                "years": 0
            })
    years_match = re.findall(r'(\d+)\+?\s*years?', text_lower)
    exp_years = max([int(y) for y in years_match], default=0)
    return {
        "skills": found_skills[:15],
        "experience_years": exp_years,
        "current_role": detect_role(text)
    }

def rule_based_jd(text: str) -> dict:
    text_lower = text.lower()
    found_skills = []
    priority_keywords = ["required", "must", "essential", "mandatory", "need"]
    for skill in KNOWN_SKILLS:
        if skill in text_lower:
            # check if it's near a priority keyword
            idx = text_lower.find(skill)
            context = text_lower[max(0, idx-100):idx+100]
            priority = "must-have" if any(k in context for k in priority_keywords) else "nice-to-have"
            found_skills.append({
                "name": skill,
                "required_level": "intermediate",
                "priority": priority
            })

    # detect domain
    domain = "technical"
    if any(w in text_lower for w in ["manager", "management", "lead", "director"]):
        domain = "managerial"
    elif any(w in text_lower for w in ["warehouse", "logistics", "operator", "labor"]):
        domain = "operational"

    return {
        "required_skills": found_skills[:12],
        "role_title": detect_role(text),
        "domain": domain
    }

# ── Main extraction functions ─────────────────────────────────────────────────

def extract_resume_skills(resume_text: str) -> dict:
    if GEMINI_AVAILABLE:
        try:
            response = client.models.generate_content(
                model="gemini-2.0-flash",
                contents=RESUME_PROMPT.format(text=resume_text[:4000])
            )
            return json.loads(clean_json(response.text))
        except Exception as e:
            print(f"Gemini failed, using fallback: {e}")
    return rule_based_resume(resume_text)

def extract_jd_skills(jd_text: str) -> dict:
    if GEMINI_AVAILABLE:
        try:
            response = client.models.generate_content(
                model="gemini-2.0-flash",
                contents=JD_PROMPT.format(text=jd_text[:4000])
            )
            return json.loads(clean_json(response.text))
        except Exception as e:
            print(f"Gemini failed, using fallback: {e}")
    return rule_based_jd(jd_text)
