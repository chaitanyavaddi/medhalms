LANGUAGE_OPTIONS = [
    {"name": "Python",     "oc_slug": "python",     "logo_domain": "python.org"},
    {"name": "JavaScript", "oc_slug": "javascript",  "logo_domain": "javascript.com"},
    {"name": "Java",       "oc_slug": "java",        "logo_domain": "java.com"},
    {"name": "TypeScript", "oc_slug": "typescript",  "logo_domain": "typescriptlang.org"},
    {"name": "C",          "oc_slug": "c",           "logo_domain": "gnu.org"},
    {"name": "C++",        "oc_slug": "cpp",         "logo_domain": "cplusplus.com"},
    {"name": "C#",         "oc_slug": "csharp",      "logo_domain": "dotnet.microsoft.com"},
    {"name": "Go",         "oc_slug": "go",          "logo_domain": "go.dev"},
    {"name": "Rust",       "oc_slug": "rust",        "logo_domain": "rust-lang.org"},
    {"name": "PHP",        "oc_slug": "php",         "logo_domain": "php.net"},
    {"name": "Ruby",       "oc_slug": "ruby",        "logo_domain": "ruby-lang.org"},
    {"name": "Kotlin",     "oc_slug": "kotlin",      "logo_domain": "kotlinlang.org"},
    {"name": "Swift",      "oc_slug": "swift",       "logo_domain": "swift.org"},
    {"name": "Dart",       "oc_slug": "dart",        "logo_domain": "dart.dev"},
    {"name": "R",          "oc_slug": "r",           "logo_domain": "r-project.org"},
    {"name": "Scala",      "oc_slug": "scala",       "logo_domain": "scala-lang.org"},
]

WEB_OPTIONS = [
    {"name": "HTML",         "oc_slug": "html",        "logo_domain": "w3.org"},
    {"name": "React",        "oc_slug": "react",       "logo_domain": "react.dev"},
    {"name": "Vue",          "oc_slug": "vuejs",       "logo_domain": "vuejs.org"},
    {"name": "Angular",      "oc_slug": "angularjs",   "logo_domain": "angular.io"},
    {"name": "Next.js",      "oc_slug": "nextjs",      "logo_domain": "nextjs.org"},
    {"name": "Node.js",      "oc_slug": "nodejs",      "logo_domain": "nodejs.org"},
    {"name": "Svelte",       "oc_slug": "svelte",      "logo_domain": "svelte.dev"},
    {"name": "jQuery",       "oc_slug": "jquery",      "logo_domain": "jquery.com"},
    {"name": "Bootstrap",    "oc_slug": "bootstrap",   "logo_domain": "getbootstrap.com"},
    {"name": "Tailwind CSS", "oc_slug": "tailwindcss", "logo_domain": "tailwindcss.com"},
]

DATABASE_OPTIONS = [
    {"name": "MySQL",      "oc_slug": "mysql",      "logo_domain": "mysql.com"},
    {"name": "PostgreSQL", "oc_slug": "postgresql", "logo_domain": "postgresql.org"},
    {"name": "SQLite",     "oc_slug": "sqlite",     "logo_domain": "sqlite.org"},
    {"name": "MongoDB",    "oc_slug": "mongodb",    "logo_domain": "mongodb.com"},
    {"name": "Redis",      "oc_slug": "redis",      "logo_domain": "redis.io"},
    {"name": "MariaDB",    "oc_slug": "mariadb",    "logo_domain": "mariadb.org"},
    {"name": "Oracle",     "oc_slug": "oracle",     "logo_domain": "oracle.com"},
    {"name": "MS SQL",     "oc_slug": "mssql",      "logo_domain": "microsoft.com"},
]

ALL_OPTIONS = {opt["oc_slug"]: opt for opt in LANGUAGE_OPTIONS + WEB_OPTIONS + DATABASE_OPTIONS}
