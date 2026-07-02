from ai_integration import optimizeaza_text_experienta
import streamlit as st

def afiseaza_interfata():
    st.title("AI Resume Builder & Optimizer")
    st.subheader("Transformă-ți experiența de facultate într-un CV profesional")
    tab1, tab2 = st.tabs(["Creator CV", "Scaner ATS"])
    
    with tab1:
        st.header("1. Date Personale și Experiență")
        nume = st.text_input("Nume și Prenume")
        email = st.text_input("Adresă de Email")
        
        tehnologii = st.multiselect(
            "Selectează tehnologiile pe care le cunoști:",
            ["Python", "C++", "Java", "SQL", "Git", "HTML/CSS", "PHP"]
        )
        
        experienta_bruta = st.text_area(
            "Descrie pe scurt ce ai lucrat la proiectele de facultate (text brut):",
            placeholder="Ex: Am făcut un proiect în Python și SQLite..."
        )
        
        if st.button("Generează CV Profesional"):
            if experienta_bruta:
                with st.spinner("Inteligența Artificială îți analizează și optimizează textul..."):
                    rezultat_ai = optimizeaza_text_experienta(experienta_bruta)
                    st.subheader("Experiența Ta Optimizată:")
                    st.write(rezultat_ai)
            else:
                st.warning("Te rog să introduci o scurtă descriere!")

    with tab2:
        st.header("2. Verificare compatibilitate ATS")
        text_cv = st.text_area("Lipește aici textul din CV-ul tău:")
        text_job = st.text_area("Lipește aici cerințele jobului (Job Description):")
        
        if st.button("Scanează Compatibilitate"):
            if text_cv and text_job:
                st.info("Se calculează scorul de potrivire...")
            else:
                st.warning("Asigură-te că ai completat ambele zone de text!")