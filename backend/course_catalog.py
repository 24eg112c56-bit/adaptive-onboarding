# Static course catalog — grounded recommendations (no hallucinations)
# Each skill maps to a list of courses with level and duration

COURSE_CATALOG = {
    "python": [
        {"title": "Python for Beginners", "level": "beginner", "duration": "8h", "url": "https://docs.python.org/3/tutorial/"},
        {"title": "Intermediate Python", "level": "intermediate", "duration": "12h", "url": "https://realpython.com/"},
        {"title": "Advanced Python Patterns", "level": "advanced", "duration": "10h", "url": "https://realpython.com/tutorials/advanced/"},
    ],
    "machine learning": [
        {"title": "ML Crash Course", "level": "beginner", "duration": "15h", "url": "https://developers.google.com/machine-learning/crash-course"},
        {"title": "Scikit-learn Fundamentals", "level": "intermediate", "duration": "10h", "url": "https://scikit-learn.org/stable/tutorial/"},
        {"title": "Deep Learning Specialization", "level": "advanced", "duration": "40h", "url": "https://www.coursera.org/specializations/deep-learning"},
    ],
    "sql": [
        {"title": "SQL Basics", "level": "beginner", "duration": "6h", "url": "https://www.w3schools.com/sql/"},
        {"title": "Advanced SQL for Analytics", "level": "intermediate", "duration": "8h", "url": "https://mode.com/sql-tutorial/"},
    ],
    "data analysis": [
        {"title": "Data Analysis with Pandas", "level": "beginner", "duration": "10h", "url": "https://pandas.pydata.org/docs/getting_started/"},
        {"title": "Exploratory Data Analysis", "level": "intermediate", "duration": "8h", "url": "https://www.kaggle.com/learn/data-visualization"},
    ],
    "javascript": [
        {"title": "JavaScript Fundamentals", "level": "beginner", "duration": "10h", "url": "https://javascript.info/"},
        {"title": "Modern JavaScript (ES6+)", "level": "intermediate", "duration": "8h", "url": "https://javascript.info/js"},
        {"title": "JavaScript Design Patterns", "level": "advanced", "duration": "12h", "url": "https://www.patterns.dev/"},
    ],
    "react": [
        {"title": "React Official Tutorial", "level": "beginner", "duration": "8h", "url": "https://react.dev/learn"},
        {"title": "React Advanced Patterns", "level": "advanced", "duration": "10h", "url": "https://react.dev/reference/react"},
    ],
    "docker": [
        {"title": "Docker Getting Started", "level": "beginner", "duration": "5h", "url": "https://docs.docker.com/get-started/"},
        {"title": "Docker for Production", "level": "intermediate", "duration": "8h", "url": "https://docs.docker.com/"},
    ],
    "kubernetes": [
        {"title": "Kubernetes Basics", "level": "beginner", "duration": "10h", "url": "https://kubernetes.io/docs/tutorials/kubernetes-basics/"},
        {"title": "Kubernetes in Production", "level": "advanced", "duration": "20h", "url": "https://kubernetes.io/docs/home/"},
    ],
    "aws": [
        {"title": "AWS Cloud Practitioner Essentials", "level": "beginner", "duration": "12h", "url": "https://aws.amazon.com/training/digital/aws-cloud-practitioner-essentials/"},
        {"title": "AWS Solutions Architect", "level": "intermediate", "duration": "40h", "url": "https://aws.amazon.com/certification/certified-solutions-architect-associate/"},
    ],
    "communication": [
        {"title": "Business Communication Essentials", "level": "beginner", "duration": "4h", "url": "https://www.coursera.org/learn/wharton-communication-skills"},
    ],
    "project management": [
        {"title": "Project Management Fundamentals", "level": "beginner", "duration": "8h", "url": "https://www.pmi.org/learning/training-development/online-courses"},
        {"title": "Agile & Scrum", "level": "intermediate", "duration": "6h", "url": "https://www.scrum.org/resources/what-is-scrum"},
    ],
    "java": [
        {"title": "Java Programming Basics", "level": "beginner", "duration": "12h", "url": "https://dev.java/learn/"},
        {"title": "Java OOP & Design Patterns", "level": "intermediate", "duration": "15h", "url": "https://refactoring.guru/design-patterns/java"},
    ],
    "git": [
        {"title": "Git & GitHub Fundamentals", "level": "beginner", "duration": "4h", "url": "https://docs.github.com/en/get-started"},
    ],
    "data structures": [
        {"title": "Data Structures & Algorithms", "level": "intermediate", "duration": "20h", "url": "https://www.coursera.org/specializations/data-structures-algorithms"},
    ],
    "nlp": [
        {"title": "NLP with Python", "level": "intermediate", "duration": "15h", "url": "https://www.nltk.org/book/"},
        {"title": "Transformers & LLMs", "level": "advanced", "duration": "20h", "url": "https://huggingface.co/learn/nlp-course/"},
    ],
    "excel": [
        {"title": "Excel for Data Analysis", "level": "beginner", "duration": "6h", "url": "https://support.microsoft.com/en-us/excel"},
    ],
    "leadership": [
        {"title": "Leadership Fundamentals", "level": "beginner", "duration": "5h", "url": "https://www.coursera.org/learn/leadership-collaboration"},
    ],
    "cybersecurity": [
        {"title": "Cybersecurity Fundamentals", "level": "beginner", "duration": "10h", "url": "https://www.coursera.org/learn/intro-cyber-security"},
        {"title": "Ethical Hacking", "level": "advanced", "duration": "30h", "url": "https://www.offensive-security.com/"},
    ],
    "devops": [
        {"title": "DevOps Fundamentals", "level": "beginner", "duration": "8h", "url": "https://www.coursera.org/learn/devops-culture-and-mindset"},
        {"title": "CI/CD Pipelines", "level": "intermediate", "duration": "10h", "url": "https://docs.github.com/en/actions"},
    ],
}

def get_courses_for_skill(skill: str, candidate_level: str = "beginner") -> list:
    """Return courses for a skill, filtered by what the candidate still needs."""
    skill_lower = skill.lower()
    matched_key = None
    for key in COURSE_CATALOG:
        if key in skill_lower or skill_lower in key:
            matched_key = key
            break
    if not matched_key:
        return []

    levels = ["beginner", "intermediate", "advanced"]
    start_idx = levels.index(candidate_level) if candidate_level in levels else 0
    return [c for c in COURSE_CATALOG[matched_key] if levels.index(c["level"]) >= start_idx]
