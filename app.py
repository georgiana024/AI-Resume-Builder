import streamlit as st

from ui_components import afiseaza_interfata

from ai_integration import optimizeaza_text_experienta

from ats_scanner import calculeaza_scor_ats

from pdf_generator import genereaza_pdf_cv


date = afiseaza_interfata()

if date and isinstance(date, dict) and date.get("nume") and date.get("experienta_bruta"):

    text_optimizat = optimizeaza_text_experienta(date["experienta_bruta"])
    

    if hasattr(text_optimizat, "text"):
        text_curat = text_optimizat.text
    else:
        text_curat = str(text_optimizat)


    pdf = genereaza_pdf_cv(
        {
            "nume": date["nume"],
            "email": date.get("email", ""),
            "status": date.get("status", "Student"),
            "educatie": date.get("educatie", []),
            "tehnologii": date.get("tehnologii", [])
        },
        text_curat
    )
    
    st.download_button(
        "Descarcă CV",
        pdf,
        "CV.pdf",
        mime="application/pdf"
    )