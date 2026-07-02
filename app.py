import streamlit as st
from ui_components import afiseaza_interfata
# from ai_integration import optimizeaza_text_experienta
# from ats_scanner import calculeaza_scor_ats
from pdf_generator import genereaza_pdf_cv

date = afiseaza_interfata()
if date and "nume" in date and date["nume"]:
    pdf = genereaza_pdf_cv(
        {
            "nume": date["nume"],
            "email": date["email"],
            "status": date["status"],
            "educatie": date["educatie"],
            "tehnologii": date["tehnologii"]
        },
        date["experienta_bruta"] # trebuie schimbat cu textul optimizat de AI
    )
    
    st.download_button(
        "Descarcă CV",
        pdf,
        "CV.pdf",
        mime="application/pdf"
    )