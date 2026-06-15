"""
Career paths data — sourced from roadmap.sh's public catalog (data.json).
Curated metadata (_RICH) adds salary / demand / skills for key roles.
Everything else gets title + image URL from the JSON automatically.
"""
import json
from pathlib import Path

_DATA_FILE = Path(__file__).resolve().parent.parent.parent / 'data.json'


def _load_catalog():
    with open(_DATA_FILE) as f:
        return {x['id']: x for x in json.load(f) if x.get('group') == 'Roadmaps'}


_CATALOG = _load_catalog()


def _img(slug):
    return f"https://roadmap.sh/roadmaps/{slug}.png"


def _link(entry):
    return f"https://roadmap.sh{entry['url']}"


# Rich metadata for the roadmaps we highlight most.
# Any roadmap NOT listed here still appears — it just won't show the meta bar.
_RICH = {
    # ── Role roadmaps ──────────────────────────────────────────────────────
    "frontend": {
        "tagline": "Build what users see — interfaces, interactions and experiences.",
        "key_skills": ["HTML & CSS", "JavaScript", "React", "TypeScript", "Git"],
        "time_to_job": "6–9 months", "demand": "Very High", "demand_color": "green", "avg_salary": "₹4–12 LPA",
    },
    "backend": {
        "tagline": "Power applications with servers, APIs and databases.",
        "key_skills": ["Python / Java / Node.js", "SQL", "REST APIs", "System Design", "Git"],
        "time_to_job": "6–9 months", "demand": "Very High", "demand_color": "green", "avg_salary": "₹5–15 LPA",
    },
    "full-stack": {
        "tagline": "Deliver complete products — from database to browser.",
        "key_skills": ["HTML/CSS/JS", "React", "Node.js / Python", "SQL", "System Design"],
        "time_to_job": "9–12 months", "demand": "Very High", "demand_color": "green", "avg_salary": "₹5–18 LPA",
    },
    "android": {
        "tagline": "Build apps for 3 billion Android users worldwide.",
        "key_skills": ["Kotlin / Java", "Android SDK", "Jetpack Compose", "REST APIs", "Git"],
        "time_to_job": "6–9 months", "demand": "High", "demand_color": "blue", "avg_salary": "₹4–12 LPA",
    },
    "ios": {
        "tagline": "Build native apps for the world's most valuable device platform.",
        "key_skills": ["Swift", "SwiftUI", "UIKit", "Xcode", "REST APIs"],
        "time_to_job": "7–10 months", "demand": "High", "demand_color": "blue", "avg_salary": "₹5–15 LPA",
    },
    "data-analyst": {
        "tagline": "Turn raw data into decisions businesses act on.",
        "key_skills": ["SQL", "Python", "Excel", "Power BI / Tableau", "Statistics"],
        "time_to_job": "5–8 months", "demand": "High", "demand_color": "blue", "avg_salary": "₹4–10 LPA",
    },
    "ai-data-scientist": {
        "tagline": "Build systems that learn from data — ML, deep learning and AI.",
        "key_skills": ["Python", "Machine Learning", "Deep Learning", "SQL", "Statistics"],
        "time_to_job": "10–14 months", "demand": "Very High", "demand_color": "green", "avg_salary": "₹6–20 LPA",
    },
    "ai-engineer": {
        "tagline": "Build and deploy AI-powered applications and pipelines.",
        "key_skills": ["Python", "LLMs", "APIs", "Prompt Engineering", "MLOps"],
        "time_to_job": "8–12 months", "demand": "Very High", "demand_color": "green", "avg_salary": "₹8–25 LPA",
    },
    "machine-learning": {
        "tagline": "Design and train models that turn data into intelligence.",
        "key_skills": ["Python", "Scikit-learn", "TensorFlow / PyTorch", "Statistics", "Feature Engineering"],
        "time_to_job": "10–15 months", "demand": "Very High", "demand_color": "green", "avg_salary": "₹7–22 LPA",
    },
    "devops": {
        "tagline": "Automate, deploy and scale — the bridge between dev and production.",
        "key_skills": ["Linux", "Docker", "Kubernetes", "CI/CD", "AWS / Azure"],
        "time_to_job": "10–14 months", "demand": "High", "demand_color": "blue", "avg_salary": "₹6–18 LPA",
    },
    "cyber-security": {
        "tagline": "Protect systems and data — one of the fastest-growing fields in tech.",
        "key_skills": ["Networking", "Linux", "Ethical Hacking", "SIEM", "Python"],
        "time_to_job": "9–13 months", "demand": "Very High", "demand_color": "green", "avg_salary": "₹5–18 LPA",
    },
    "qa": {
        "tagline": "Ship software that actually works — testing, automation and quality.",
        "key_skills": ["Manual Testing", "Selenium / Cypress", "API Testing", "Python / Java", "JIRA"],
        "time_to_job": "4–7 months", "demand": "High", "demand_color": "blue", "avg_salary": "₹3–8 LPA",
    },
    "ux-design": {
        "tagline": "Design products people love — the human side of technology.",
        "key_skills": ["Figma", "User Research", "Wireframing", "Prototyping", "Accessibility"],
        "time_to_job": "6–10 months", "demand": "High", "demand_color": "blue", "avg_salary": "₹4–14 LPA",
    },
    # ── Skill roadmaps ─────────────────────────────────────────────────────
    "javascript": {
        "tagline": "The language of the web — every frontend journey starts here.",
        "key_skills": ["ES6+", "DOM", "Async / Await", "Modules", "Fetch API"],
        "time_to_job": "3–5 months", "demand": "Very High", "demand_color": "green", "avg_salary": "₹4–12 LPA",
    },
    "typescript": {
        "tagline": "Type-safe JavaScript — the industry default for large codebases.",
        "key_skills": ["Types & Interfaces", "Generics", "Decorators", "Strict Mode", "Tooling"],
        "time_to_job": "2–4 months", "demand": "High", "demand_color": "blue", "avg_salary": "₹5–14 LPA",
    },
    "python": {
        "tagline": "The language of AI, data and modern backend — master it first.",
        "key_skills": ["Python Core", "OOP", "Standard Library", "APIs & Libraries", "Testing"],
        "time_to_job": "4–7 months", "demand": "Very High", "demand_color": "green", "avg_salary": "₹4–12 LPA",
    },
    "java": {
        "tagline": "Enterprise backend — the backbone of Indian IT companies.",
        "key_skills": ["Java Core", "OOP & Design Patterns", "Spring Boot", "SQL", "Microservices"],
        "time_to_job": "6–9 months", "demand": "High", "demand_color": "blue", "avg_salary": "₹4–14 LPA",
    },
    "sql": {
        "tagline": "Every data job starts here — query, model and optimise data.",
        "key_skills": ["SQL Basics", "Joins & Aggregations", "Indexing", "Stored Procedures", "PostgreSQL"],
        "time_to_job": "2–4 months", "demand": "Very High", "demand_color": "green", "avg_salary": "₹3–9 LPA",
    },
    "react": {
        "tagline": "Master the world's most used frontend library.",
        "key_skills": ["JSX", "Hooks", "State Management", "REST APIs", "TypeScript"],
        "time_to_job": "4–7 months", "demand": "High", "demand_color": "blue", "avg_salary": "₹5–14 LPA",
    },
    "system-design": {
        "tagline": "Design systems that scale to millions — essential for senior roles.",
        "key_skills": ["Scalability", "Caching", "Load Balancing", "Databases", "Microservices"],
        "time_to_job": "6–12 months", "demand": "Very High", "demand_color": "green", "avg_salary": "₹12–40 LPA",
    },
    "datastructures-and-algorithms": {
        "tagline": "Crack product company interviews — DSA is the gate.",
        "key_skills": ["Arrays & Strings", "Trees & Graphs", "Dynamic Programming", "Sorting", "Complexity"],
        "time_to_job": "3–6 months", "demand": "Very High", "demand_color": "green", "avg_salary": "₹8–30 LPA",
    },
    "docker": {
        "tagline": "Containerise everything — the foundation of modern deployment.",
        "key_skills": ["Images & Containers", "Docker Compose", "Networking", "Volumes", "Registry"],
        "time_to_job": "2–4 months", "demand": "High", "demand_color": "blue", "avg_salary": "₹5–16 LPA",
    },
    "aws": {
        "tagline": "The cloud everyone runs on — essential for backend and DevOps.",
        "key_skills": ["EC2 / S3 / RDS", "IAM", "Lambda", "VPC", "CLI & SDK"],
        "time_to_job": "4–8 months", "demand": "Very High", "demand_color": "green", "avg_salary": "₹6–20 LPA",
    },
    "git-github": {
        "tagline": "Version control is non-negotiable — every developer uses Git.",
        "key_skills": ["Branching", "Merging & Rebasing", "Pull Requests", "CI/CD", "GitHub Actions"],
        "time_to_job": "1–2 months", "demand": "Very High", "demand_color": "green", "avg_salary": "Foundational",
    },
}


# ── Group definitions ─────────────────────────────────────────────────────────
# Ordered: most relevant first for Indian students.

_ROLE_GROUPS_DEF = [
    ("Web & Mobile",     ["frontend", "backend", "full-stack", "android", "ios", "game-developer", "server-side-game-developer"]),
    ("Data & AI",        ["data-analyst", "ai-data-scientist", "ai-engineer", "machine-learning", "data-engineer", "bi-analyst"]),
    ("Infrastructure",   ["devops", "devsecops", "mlops", "cyber-security", "network-engineer", "postgresql-dba"]),
    ("Product & Design", ["qa", "ux-design", "product-manager", "software-architect", "technical-writer", "engineering-manager", "devrel", "blockchain", "forward-deployed-engineer"]),
]

_SKILL_GROUPS_DEF = [
    ("Languages",       ["javascript", "typescript", "python", "java", "golang", "rust", "cpp", "kotlin", "php", "ruby", "scala", "swift-ui"]),
    ("Frontend & Mobile", ["react", "vue", "angular", "nextjs", "html", "css", "flutter", "react-native", "design-system"]),
    ("Backend & APIs",  ["nodejs", "spring-boot", "aspnet-core", "laravel", "django", "ruby-on-rails", "graphql", "api-design", "wordpress"]),
    ("Databases",       ["sql", "mongodb", "redis", "elasticsearch"]),
    ("DevOps & Cloud",  ["docker", "kubernetes", "aws", "terraform", "linux", "shell-bash", "cloudflare", "git-github"]),
    ("CS Fundamentals", ["computer-science", "datastructures-and-algorithms", "system-design", "software-design-architecture", "code-review"]),
    ("AI & Emerging",   ["prompt-engineering", "ai-agents", "ai-red-teaming", "leetcode", "vibe-coding", "claude-code"]),
]


def _build_entry(rid):
    entry = _CATALOG.get(rid)
    if not entry:
        return None
    rich = _RICH.get(rid, {})
    description = entry.get('description', '').replace('@currentYear@', '2025')
    return {
        "id": rid,
        "name": entry['title'],
        "roadmap_url": _link(entry),
        "image_url": _img(rid),
        "tagline": rich.get('tagline') or description,
        "key_skills": rich.get('key_skills', []),
        "time_to_job": rich.get('time_to_job', ''),
        "demand": rich.get('demand', ''),
        "demand_color": rich.get('demand_color', ''),
        "avg_salary": rich.get('avg_salary', ''),
        "is_rich": bool(rich),
    }


def _build_groups(defs):
    result = []
    for label, ids in defs:
        items = [e for rid in ids for e in [_build_entry(rid)] if e]
        if items:
            result.append({"label": label, "items": items})
    return result


ROLE_GROUPS  = _build_groups(_ROLE_GROUPS_DEF)
SKILL_GROUPS = _build_groups(_SKILL_GROUPS_DEF)

# Flat lookup — role and skill ids share a single namespace (no overlaps in practice)
ALL_ROADMAPS = {item['id']: item for grp in ROLE_GROUPS + SKILL_GROUPS for item in grp['items']}
ROLE_IDS     = {item['id'] for grp in ROLE_GROUPS  for item in grp['items']}
SKILL_IDS    = {item['id'] for grp in SKILL_GROUPS for item in grp['items']}

DEFAULT_ROLE_ID  = "frontend"
DEFAULT_SKILL_ID = "javascript"
