import re

BAZA_SKILLURI = {
    # Limbaje de programare
    "Python": ["python"],
    "Java": ["java"],
    "JavaScript": ["javascript", "js"],
    "TypeScript": ["typescript", "ts"],
    "C++": ["c++", "cpp"],
    "C#": ["c#", "csharp"],
    "C": ["c"],  
    "PHP": ["php"],
    "Ruby": ["ruby"],
    "Go": ["golang"],  
    "Rust": ["rust"],
    "Kotlin": ["kotlin"],
    "Swift": ["swift"],

    # Baze de date
    "SQL": ["sql"],
    "MySQL": ["mysql"],
    "PostgreSQL": ["postgresql", "postgres"],
    "SQLite": ["sqlite"],
    "MongoDB": ["mongodb", "mongo"],

    # Web / Frontend
    "HTML": ["html"],
    "CSS": ["css"],
    "React": ["react", "react.js", "reactjs"],
    "Angular": ["angular"],
    "Vue": ["vue", "vue.js", "vuejs"],
    "Node.js": ["node.js", "nodejs", "node"],

    # Backend / Framework-uri
    "Django": ["django"],
    "Flask": ["flask"],
    "FastAPI": ["fastapi"],
    "Spring": ["spring", "spring boot"],
    ".NET": [".net", "dotnet", "asp.net"],
    "Laravel": ["laravel"],

    # Tooling / DevOps
    "Git": ["git"],
    "GitHub": ["github"],
    "GitLab": ["gitlab"],
    "Docker": ["docker"],
    "Kubernetes": ["kubernetes", "k8s"],
    "Linux": ["linux"],
    "Bash": ["bash", "shell scripting"],
    "CI/CD": ["ci/cd", "cicd", "ci cd"],
    "REST API": ["rest api", "restful", "rest"],
    "GraphQL": ["graphql"],

    # Cloud
    "AWS": ["aws", "amazon web services"],
    "Azure": ["azure"],
    "Google Cloud": ["gcp", "google cloud"],

    # Data / AI
    "Pandas": ["pandas"],
    "NumPy": ["numpy"],
    "TensorFlow": ["tensorflow"],
    "PyTorch": ["pytorch"],
    "Scikit-learn": ["scikit-learn", "sklearn", "scikit learn"],
    "Machine Learning": ["machine learning", "ml"],
    "Deep Learning": ["deep learning"],
    "Data Analysis": ["data analysis", "analiza datelor"],
    "Power BI": ["power bi", "powerbi"],
    "Excel": ["excel"],
    "Tableau": ["tableau"],
    "Streamlit": ["streamlit"],

    # Metodologii
    "Agile": ["agile"],
    "Scrum": ["scrum"],
    "Jira": ["jira"],
}


def _tokenizeaza(text):
    """
    Transformă un text brut într-o listă de "cuvinte" (tokens) normalizate.

    - trece totul la litere mici;
    - păstrează caracterele + # . în interiorul token-urilor (pentru c++, c#, node.js);
    - orice alt separator (spații, virgule, /, -, paranteze, diacritice) devine spațiu;
    - curăță punctele/underscore-urile rămase la marginea token-urilor
      ("python." -> "python", ".net" -> "net").
    """
    if not text:
        return []
    text = text.lower()
    text = re.sub(r"[^\w+#.]+", " ", text)
    tokens = []
    for t in text.split():
        t = t.strip("._")
        if t:
            tokens.append(t)
    return tokens


def _apare_secventa(sub_tokens, tokens):
    """
    Verifică dacă secvența `sub_tokens` apare, în ordine și consecutiv,
    în lista `tokens`. Astfel prindem corect și skill-urile din mai multe
    cuvinte, ex: ["machine", "learning"].
    """
    n = len(sub_tokens)
    if n == 0:
        return False
    for i in range(len(tokens) - n + 1):
        if tokens[i:i + n] == sub_tokens:
            return True
    return False


_ALIAS_TOKENIZAT = {
    skill: [_tokenizeaza(alias) for alias in aliasuri]
    for skill, aliasuri in BAZA_SKILLURI.items()
}


def _skill_prezent(skill, tokens_text):
    """Întoarce True dacă oricare formă (alias) a skill-ului apare în text."""
    return any(
        _apare_secventa(alias_tok, tokens_text)
        for alias_tok in _ALIAS_TOKENIZAT.get(skill, [])
    )



def extrage_cerinte(text_job, cerinte_extra=None):
    """
    Izolează din textul jobului tehnologiile esențiale, comparând cu baza de skill-uri.

    :param text_job: textul cerințelor postului (Job Description).
    :param cerinte_extra: listă opțională de cerințe suplimentare (ex: extrase de
                          AI-ul Membrului 2) care se adaugă la cele detectate local.
    :return: listă cu numele de afișare ale tehnologiilor cerute (fără duplicate).
    """
    tokens_job = _tokenizeaza(text_job)
    cerinte = [skill for skill in BAZA_SKILLURI if _skill_prezent(skill, tokens_job)]

    if cerinte_extra:
        for extra in cerinte_extra:
            if extra and extra not in cerinte:
                cerinte.append(extra)

    return cerinte


def _mesaj_scor(scor):
    if scor >= 80:
        return "Potrivire excelentă! CV-ul acoperă foarte bine cerințele jobului."
    elif scor >= 60:
        return "Potrivire bună. Merită să adaugi câteva dintre skill-urile lipsă."
    elif scor >= 40:
        return "Potrivire medie. Ai destule goluri de completat față de cerințe."
    else:
        return "Potrivire scăzută. CV-ul trebuie ajustat serios pentru acest rol."



def calculeaza_scor_ats(text_cv, text_job, cerinte_extra=None):
    """
    Calculează compatibilitatea dintre un CV și cerințele unui job.

    Pasul 2 -> caută prezența termenilor esențiali în textul CV-ului.
    Pasul 3 -> scor procentual = (cerințe găsite / total cerințe) * 100.
    Pasul 4 -> împachetează totul într-un dict clar pentru UI.
    """
    # Validare de bază, ca UI-ul să primească mereu o structură coerentă.
    if not text_cv or not text_job or not text_cv.strip() or not text_job.strip():
        return {
            "scor": 0,
            "gasite": [],
            "lipsa": [],
            "total_cerute": 0,
            "mesaj": "Completează atât textul CV-ului, cât și cerințele jobului.",
        }

    cerinte = extrage_cerinte(text_job, cerinte_extra=cerinte_extra)

    if not cerinte:
        return {
            "scor": 0,
            "gasite": [],
            "lipsa": [],
            "total_cerute": 0,
            "mesaj": "Nu am identificat tehnologii cunoscute în descrierea jobului.",
        }

    tokens_cv = _tokenizeaza(text_cv)
    gasite = [skill for skill in cerinte if _skill_prezent(skill, tokens_cv)]
    lipsa = [skill for skill in cerinte if skill not in gasite]

    scor = round(len(gasite) / len(cerinte) * 100)

    return {
        "scor": scor,
        "gasite": sorted(gasite),
        "lipsa": sorted(lipsa),
        "total_cerute": len(cerinte),
        "mesaj": _mesaj_scor(scor),
    }
