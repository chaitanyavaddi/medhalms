"""
Career path definitions — sourced from roadmap.sh community roadmaps.
Each role maps to a well-maintained roadmap.sh page embedded in the UI.
Add / edit roles here; no DB or migration needed.
"""

CAREER_TRACKS = [
    {
        "id": "web",
        "label": "Web Development",
        "roles": [
            {
                "id": "frontend",
                "name": "Frontend Developer",
                "roadmap_url": "https://roadmap.sh/frontend",
                "image_url": "https://roadmap.sh/roadmaps/frontend.png",
                "tagline": "Build what users see — interfaces, interactions and experiences.",
                "key_skills": ["HTML & CSS", "JavaScript", "React", "TypeScript", "Git"],
                "time_to_job": "6–9 months",
                "demand": "Very High",
                "avg_salary": "₹4–12 LPA",
                "demand_color": "green",
            },
            {
                "id": "backend",
                "name": "Backend Developer",
                "roadmap_url": "https://roadmap.sh/backend",
                "image_url": "https://roadmap.sh/roadmaps/backend.png",
                "tagline": "Power applications with servers, APIs and databases.",
                "key_skills": ["Python / Java / Node.js", "SQL", "REST APIs", "System Design", "Git"],
                "time_to_job": "6–9 months",
                "demand": "Very High",
                "avg_salary": "₹5–15 LPA",
                "demand_color": "green",
            },
            {
                "id": "full-stack",
                "name": "Full Stack Developer",
                "roadmap_url": "https://roadmap.sh/full-stack",
                "image_url": "https://roadmap.sh/roadmaps/full-stack.png",
                "tagline": "Deliver complete products — from database to browser.",
                "key_skills": ["HTML/CSS/JS", "React", "Node.js / Python", "SQL", "System Design"],
                "time_to_job": "9–12 months",
                "demand": "Very High",
                "avg_salary": "₹5–18 LPA",
                "demand_color": "green",
            },
            {
                "id": "react",
                "name": "React Developer",
                "roadmap_url": "https://roadmap.sh/react",
                "image_url": "https://roadmap.sh/roadmaps/react.png",
                "tagline": "Master the world's most used frontend library.",
                "key_skills": ["JavaScript ES6+", "React", "Redux / Zustand", "REST APIs", "TypeScript"],
                "time_to_job": "4–7 months",
                "demand": "High",
                "avg_salary": "₹5–14 LPA",
                "demand_color": "blue",
            },
        ],
    },
    {
        "id": "data",
        "label": "Data & AI",
        "roles": [
            {
                "id": "data-analyst",
                "name": "Data Analyst",
                "roadmap_url": "https://roadmap.sh/data-analyst",
                "image_url": "https://roadmap.sh/roadmaps/data-analyst.png",
                "tagline": "Turn raw data into decisions businesses act on.",
                "key_skills": ["SQL", "Python", "Excel", "Power BI / Tableau", "Statistics"],
                "time_to_job": "5–8 months",
                "demand": "High",
                "avg_salary": "₹4–10 LPA",
                "demand_color": "blue",
            },
            {
                "id": "ai-data-scientist",
                "name": "Data Scientist / AI",
                "roadmap_url": "https://roadmap.sh/ai-data-scientist",
                "image_url": "https://roadmap.sh/roadmaps/ai-data-scientist.png",
                "tagline": "Build systems that learn from data — ML, deep learning and AI.",
                "key_skills": ["Python", "Machine Learning", "Deep Learning", "SQL", "Statistics & Math"],
                "time_to_job": "10–14 months",
                "demand": "Very High",
                "avg_salary": "₹6–20 LPA",
                "demand_color": "green",
            },
            {
                "id": "python",
                "name": "Python Developer",
                "roadmap_url": "https://roadmap.sh/python",
                "image_url": "https://roadmap.sh/roadmaps/python.png",
                "tagline": "The language of AI, data and modern backend — master it first.",
                "key_skills": ["Python Core", "OOP", "Standard Library", "APIs & Libraries", "Testing"],
                "time_to_job": "4–7 months",
                "demand": "Very High",
                "avg_salary": "₹4–12 LPA",
                "demand_color": "green",
            },
            {
                "id": "sql",
                "name": "SQL & Databases",
                "roadmap_url": "https://roadmap.sh/sql",
                "image_url": "https://roadmap.sh/roadmaps/sql.png",
                "tagline": "Every data job starts here — query, model and optimise data.",
                "key_skills": ["SQL Basics", "Joins & Aggregations", "Indexing", "Stored Procedures", "PostgreSQL"],
                "time_to_job": "2–4 months",
                "demand": "Very High",
                "avg_salary": "₹3–9 LPA",
                "demand_color": "green",
            },
        ],
    },
    {
        "id": "mobile",
        "label": "Mobile Development",
        "roles": [
            {
                "id": "android",
                "name": "Android Developer",
                "roadmap_url": "https://roadmap.sh/android",
                "image_url": "https://roadmap.sh/roadmaps/android.png",
                "tagline": "Build apps for 3 billion Android users worldwide.",
                "key_skills": ["Kotlin / Java", "Android SDK", "Jetpack Compose", "REST APIs", "Git"],
                "time_to_job": "6–9 months",
                "demand": "High",
                "avg_salary": "₹4–12 LPA",
                "demand_color": "blue",
            },
        ],
    },
    {
        "id": "devops",
        "label": "DevOps & Cloud",
        "roles": [
            {
                "id": "devops",
                "name": "DevOps Engineer",
                "roadmap_url": "https://roadmap.sh/devops",
                "image_url": "https://roadmap.sh/roadmaps/devops.png",
                "tagline": "Automate, deploy and scale — the bridge between dev and production.",
                "key_skills": ["Linux", "Docker", "Kubernetes", "CI/CD Pipelines", "AWS / Azure / GCP"],
                "time_to_job": "10–14 months",
                "demand": "High",
                "avg_salary": "₹6–18 LPA",
                "demand_color": "blue",
            },
            {
                "id": "java",
                "name": "Java Developer",
                "roadmap_url": "https://roadmap.sh/java",
                "image_url": "https://roadmap.sh/roadmaps/java.png",
                "tagline": "Enterprise backend — the backbone of Indian IT companies.",
                "key_skills": ["Java Core", "OOP & Design Patterns", "Spring Boot", "SQL", "Microservices"],
                "time_to_job": "6–9 months",
                "demand": "High",
                "avg_salary": "₹4–14 LPA",
                "demand_color": "blue",
            },
        ],
    },
    {
        "id": "quality",
        "label": "Quality Engineering",
        "roles": [
            {
                "id": "qa",
                "name": "QA / Test Engineer",
                "roadmap_url": "https://roadmap.sh/qa",
                "image_url": "https://roadmap.sh/roadmaps/qa.png",
                "tagline": "Ship software that actually works — testing, automation and quality.",
                "key_skills": ["Manual Testing", "Selenium / Cypress", "API Testing", "Python / Java", "JIRA"],
                "time_to_job": "4–7 months",
                "demand": "High",
                "avg_salary": "₹3–8 LPA",
                "demand_color": "blue",
            },
        ],
    },
]


def _build_role_index():
    idx = {}
    for track in CAREER_TRACKS:
        for role in track["roles"]:
            idx[role["id"]] = role
    return idx


ALL_ROLES = _build_role_index()
DEFAULT_ROLE_ID = "frontend"
