import google.generativeai as genai
import streamlit as st
GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]

genai.configure(api_key=GEMINI_API_KEY)

import google.generativeai as genai
import streamlit as st
GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
 
genai.configure(api_key=GEMINI_API_KEY)
 
MODEL = "gemini-2.5-flash"
 

def _curata_raspuns(text):
    """Elimină spațiile în plus și blocurile markdown ```...``` din răspuns."""
    if not text:
        return ""
    text = text.strip()
    if text.startswith("```"):
        linii = text.splitlines()
        if linii and linii[0].startswith("```"):
            linii = linii[1:]
        if linii and linii[-1].strip().startswith("```"):
            linii = linii[:-1]
        text = "\n".join(linii).strip()
    return text
 
 
def optimizeaza_text_experienta(text_brut):
    """Transformă o descriere brută în bullet-points profesionale pentru CV."""
    instructiuni = (
        "Ești un specialist HR și în recrutare tehnică. Primești o descriere brută, "
        "scrisă simplu de un student, despre ce a lucrat la proiectele de facultate. "
        "Rescrie textul în 3-5 bullet-points profesionale, potrivite pentru un CV. "
        "Fiecare punct începe cu un verb de acțiune puternic, evidențiază impactul "
        "tehnic și, unde se poate, un rezultat concret. Răspunde DOAR cu bullet-points "
        "(folosește prefixul '- '), fără introducere, fără concluzie și fără alte explicații. "
        "Scrie în limba română."
    )
    try:
        model = genai.GenerativeModel(model_name=MODEL, system_instruction=instructiuni)
        raspuns = model.generate_content(
            text_brut,
            generation_config=genai.types.GenerationConfig(temperature=0.7),
        )
        return _curata_raspuns(raspuns.text)
    except Exception as e:
        return f"[Eroare la apelul AI] {e}"
 
 
def analizeaza_cu_ai(text_cv, text_job):
    """Evaluare calitativă, în text, a potrivirii dintre CV și cerințele jobului."""
    instructiuni = (
        "Ești un evaluator ATS și specialist în recrutare. Primești un CV și descrierea "
        "unui job. Oferă o evaluare scurtă și nuanțată a potrivirii candidatului pe rol. "
        "Structurează răspunsul în trei secțiuni scurte, cu aceste titluri exacte: "
        "'Puncte forte', 'Ce lipsește' și 'Recomandări'. Fii concret și la obiect, "
        "maxim 3 idei per secțiune. Scrie în limba română."
    )
    continut = (
        "=== TEXT CV ===\n"
        f"{text_cv}\n\n"
        "=== CERINȚE JOB ===\n"
        f"{text_job}"
    )
    try:
        model = genai.GenerativeModel(model_name=MODEL, system_instruction=instructiuni)
        raspuns = model.generate_content(
            continut,
            generation_config=genai.types.GenerationConfig(temperature=0.4),
        )
        return _curata_raspuns(raspuns.text)
    except Exception as e:
        return f"[Eroare la apelul AI] {e}"