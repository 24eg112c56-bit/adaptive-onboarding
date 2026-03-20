"""
Adaptive Pathing Algorithm — Original Implementation
Uses a graph-based skill dependency model to order learning modules optimally.
"""
from course_catalog import get_courses_for_skill, COURSE_CATALOG

# Skill prerequisite graph — defines learning dependencies
SKILL_GRAPH = {
    "machine learning": ["python", "data analysis", "data structures"],
    "deep learning": ["machine learning", "python"],
    "nlp": ["python", "machine learning"],
    "react": ["javascript"],
    "kubernetes": ["docker"],
    "devops": ["git", "docker"],
    "aws": ["docker"],
    "data analysis": ["python", "sql", "excel"],
    "cybersecurity": ["networking"],
    "project management": ["communication"],
    "leadership": ["communication"],
}

LEVELS = ["beginner", "intermediate", "advanced"]

def level_index(level: str) -> int:
    return LEVELS.index(level) if level in LEVELS else 0

def analyze_gap(resume_data: dict, jd_data: dict) -> dict:
    """
    Core skill-gap analysis:
    1. Build a map of candidate's current skills + levels
    2. Compare against JD required skills
    3. Identify gaps (missing skills or insufficient level)
    4. Return structured gap report
    """
    candidate_skills = {
        s["name"].lower(): s for s in resume_data.get("skills", [])
    }
    required_skills = jd_data.get("required_skills", [])

    gaps = []
    already_has = []

    for req in required_skills:
        skill_name = req["name"].lower()
        required_level = req.get("required_level", "beginner")
        priority = req.get("priority", "must-have")

        if skill_name in candidate_skills:
            candidate_level = candidate_skills[skill_name].get("level", "beginner")
            if level_index(candidate_level) < level_index(required_level):
                gaps.append({
                    "skill": req["name"],
                    "current_level": candidate_level,
                    "required_level": required_level,
                    "gap_type": "level_upgrade",
                    "priority": priority,
                })
            else:
                already_has.append({"skill": req["name"], "level": candidate_level})
        else:
            gaps.append({
                "skill": req["name"],
                "current_level": None,
                "required_level": required_level,
                "gap_type": "missing_skill",
                "priority": priority,
            })

    return {
        "gaps": gaps,
        "already_has": already_has,
        "candidate_experience_years": resume_data.get("experience_years", 0),
        "current_role": resume_data.get("current_role"),
        "target_role": jd_data.get("role_title"),
        "domain": jd_data.get("domain", "technical"),
    }

def topological_sort(skills: list) -> list:
    """
    Order skills by prerequisites using DFS-based topological sort.
    Skills with no prerequisites come first.
    """
    visited = set()
    order = []

    def dfs(skill):
        if skill in visited:
            return
        visited.add(skill)
        for prereq in SKILL_GRAPH.get(skill, []):
            if prereq in skills:
                dfs(prereq)
        order.append(skill)

    for skill in skills:
        dfs(skill)
    return order

def build_learning_pathway(gap_report: dict) -> dict:
    """
    Adaptive Pathing:
    1. Prioritize must-have gaps over nice-to-have
    2. Inject prerequisite skills if missing
    3. Topologically sort to create a logical learning order
    4. Map each skill to grounded course catalog entries
    5. Estimate total learning time
    """
    gaps = gap_report["gaps"]
    candidate_skills = {g["skill"].lower() for g in gap_report.get("already_has", [])}

    must_have = [g for g in gaps if g["priority"] == "must-have"]
    nice_to_have = [g for g in gaps if g["priority"] != "must-have"]

    skills_to_learn = [g["skill"].lower() for g in must_have + nice_to_have]

    # Inject missing prerequisites
    all_skills = list(skills_to_learn)
    for skill in skills_to_learn:
        for prereq in SKILL_GRAPH.get(skill, []):
            if prereq not in candidate_skills and prereq not in all_skills:
                all_skills.insert(0, prereq)

    ordered_skills = topological_sort(all_skills)

    modules = []
    total_hours = 0
    reasoning_steps = []

    for i, skill in enumerate(ordered_skills):
        gap_info = next((g for g in gaps if g["skill"].lower() == skill), None)
        start_level = gap_info["current_level"] if gap_info and gap_info["current_level"] else "beginner"
        courses = get_courses_for_skill(skill, start_level)

        module_hours = sum(
            int(c["duration"].replace("h", "")) for c in courses if c.get("duration")
        )
        total_hours += module_hours

        is_prereq = skill not in [g["skill"].lower() for g in gaps]
        priority = gap_info["priority"] if gap_info else "prerequisite"

        modules.append({
            "step": i + 1,
            "skill": skill,
            "gap_type": gap_info["gap_type"] if gap_info else "prerequisite",
            "current_level": start_level,
            "target_level": gap_info["required_level"] if gap_info else "beginner",
            "priority": priority,
            "is_prerequisite": is_prereq,
            "courses": courses,
            "estimated_hours": module_hours,
        })

        if is_prereq:
            reasoning_steps.append(
                f"Step {i+1}: '{skill}' added as a prerequisite for a required skill."
            )
        elif gap_info["gap_type"] == "missing_skill":
            reasoning_steps.append(
                f"Step {i+1}: '{skill}' is missing entirely. Starting from {start_level}. Priority: {priority}."
            )
        else:
            reasoning_steps.append(
                f"Step {i+1}: '{skill}' exists at {start_level} but role requires {gap_info['required_level']}. Upgrading."
            )

    return {
        "target_role": gap_report["target_role"],
        "current_role": gap_report["current_role"],
        "domain": gap_report["domain"],
        "total_modules": len(modules),
        "total_estimated_hours": total_hours,
        "modules": modules,
        "skills_already_proficient": [s["skill"] for s in gap_report.get("already_has", [])],
        "reasoning_trace": reasoning_steps,
    }
