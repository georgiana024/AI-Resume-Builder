
from ai_integration import optimizeaza_text_experienta
from ats_scanner import calculeaza_scor_ats

import streamlit as st

def afiseaza_interfata():
    st.title("AI Resume Builder & Optimizer")
    st.subheader("Transformă-ți experiența de facultate într-un CV profesional")
    tab1, tab2 = st.tabs(["Creator CV", "Scaner ATS"])

    rezultat = {}

    with tab1:
        st.header("1. Date Personale și Experiență")
        nume = st.text_input("Nume și Prenume")
        email = st.text_input("Adresă de Email")
        rezultat["nume"] = nume
        rezultat["email"] = email

        status = st.selectbox(
            "Statut",
            [
                "Student",
                "Masterand",
                "Absolvent",
                "Intern",
                "Angajat",
                "În căutarea unui loc de muncă",
            ]
        )

        rezultat["status"] = status

        st.subheader("Educație")

        if "educatie_count" not in st.session_state:
            st.session_state.educatie_count = 1

        educatii = []

        for i in range(st.session_state.educatie_count):
            st.markdown(f"**Studii #{i + 1}**")

            institutie = st.text_input(
                "Instituție",
                key=f"institutie_{i}"
            )

            perioada = st.text_input(
                "Perioadă",
                placeholder="Ex: 2021 - 2024",
                key=f"perioada_{i}"
            )

            specializare = st.text_input(
                "Specializare",
                key=f"specializare_{i}"
            )

            educatii.append({
                "institutie": institutie,
                "perioada": perioada,
                "specializare": specializare
            })

        if st.button("+ Adaugă altă instituție"):
            st.session_state.educatie_count += 1
            st.rerun()

        rezultat["educatie"] = educatii
        
        tehnologii = st.multiselect(
            "Selectează tehnologiile pe care le cunoști:",
            ["Python", "C++", "Java", "SQL", "Git", "HTML/CSS", "PHP"]
        )
        rezultat["tehnologii"] = tehnologii
        experienta_bruta = st.text_area(
            "Descrie pe scurt ce ai lucrat la proiectele de facultate (text brut):",
            placeholder="Ex: Am făcut un proiect în Python și SQLite..."
        )
        rezultat["experienta_bruta"] = experienta_bruta
        
        if st.button("Generează CV Profesional"):
            if experienta_bruta:
                st.info("Aici va apărea textul optimizat de AI și butonul de download PDF...")
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

    return rezultat
