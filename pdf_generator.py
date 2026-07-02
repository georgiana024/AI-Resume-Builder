from fpdf import FPDF


class ResumePDF(FPDF):

    def header(self):
        pass

    def footer(self):
        self.set_y(-12)
        self.set_font("DejaVu", "I", 8)
        self.set_text_color(120, 120, 120)
        self.cell(0, 10, f"Pagina {self.page_no()}", align="C")


def genereaza_pdf_cv(date_utilizator, experienta_optimizata):

    pdf = ResumePDF()

    pdf.add_font("DejaVu", "", "AI-Resume-Builder-main/fonts/DejaVuSans.ttf")
    pdf.add_font("DejaVu", "B", "AI-Resume-Builder-main/fonts/DejaVuSans-Bold.ttf")
    pdf.add_font("DejaVu", "I", "AI-Resume-Builder-main/fonts/DejaVuSans-Oblique.ttf")

    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    # header

    pdf.set_font("DejaVu", "B", 24)
    pdf.set_text_color(35, 35, 35)
    pdf.cell(0, 12, date_utilizator["nume"], align="C", new_x="LMARGIN", new_y="NEXT")

    pdf.set_font("DejaVu", "", 12)
    pdf.set_text_color(90, 90, 90)
    pdf.cell(0, 8, date_utilizator["email"], align="C", new_x="LMARGIN", new_y="NEXT")

    status = date_utilizator.get("status", "")
    if status:
        pdf.cell(0, 8, status, align="C", new_x="LMARGIN", new_y="NEXT")

    pdf.ln(3)

    pdf.set_draw_color(40, 90, 170)
    pdf.set_line_width(0.8)
    pdf.line(20, pdf.get_y(), 190, pdf.get_y())

    pdf.ln(8)

    # profil

    pdf.set_text_color(40, 90, 170)
    pdf.set_font("DejaVu", "B", 15)
    pdf.cell(0, 8, "PROFIL", new_x="LMARGIN", new_y="NEXT")

    pdf.set_font("DejaVu", "", 11)
    pdf.set_text_color(0, 0, 0)

    profil = f"{status} interesat(ă) de dezvoltarea software, cu experiență în proiecte și dorința de dezvoltare profesională."

    pdf.multi_cell(0, 7, profil)

    pdf.ln(3)

    # educatie

    pdf.set_text_color(40, 90, 170)
    pdf.set_font("DejaVu", "B", 15)
    pdf.cell(0, 8, "EDUCAȚIE", new_x="LMARGIN", new_y="NEXT")

    pdf.set_text_color(0, 0, 0)
    pdf.set_font("DejaVu", "", 11)

    educatii = date_utilizator.get("educatie", [])

    if educatii:

        for studiu in educatii:

            if not studiu["institutie"]:
                continue

            pdf.set_x(pdf.l_margin)

            pdf.set_font("DejaVu", "B", 11)
            pdf.multi_cell(pdf.epw, 6, studiu["institutie"])

            pdf.set_font("DejaVu", "", 10)

            rand = ""

            if studiu["specializare"]:
                rand += studiu["specializare"]

            if studiu["perioada"]:

                if rand:
                    rand += " | "

                rand += studiu["perioada"]

            pdf.set_x(pdf.l_margin)
            pdf.multi_cell(pdf.epw, 6, rand)

            pdf.ln(2)

    pdf.ln(3)

   # competente

    pdf.set_text_color(40, 90, 170)
    pdf.set_font("DejaVu", "B", 15)
    pdf.cell(0, 8, "COMPETENȚE TEHNICE", new_x="LMARGIN", new_y="NEXT")

    pdf.set_text_color(0, 0, 0)
    pdf.set_font("DejaVu", "", 11)

    tehnologii = date_utilizator.get("tehnologii", [])

    if tehnologii:
        pdf.multi_cell(
            0,
            7,
            " • ".join(tehnologii)
        )
    else:
        pdf.multi_cell(0, 7, "Nu au fost introduse competențe.")

    pdf.ln(3)

    # experienta

    pdf.set_text_color(40, 90, 170)
    pdf.set_font("DejaVu", "B", 15)
    pdf.cell(0, 8, "EXPERIENȚĂ", new_x="LMARGIN", new_y="NEXT")

    pdf.set_text_color(0, 0, 0)
    pdf.set_font("DejaVu", "", 11)

    if experienta_optimizata.strip():

        linii = experienta_optimizata.split("\n")

        for linie in linii:

            linie = linie.strip()

            if linie:

                if linie.startswith("-") or linie.startswith("•"):

                    pdf.multi_cell(
                        0,
                        7,
                        linie
                    )

                else:

                    pdf.multi_cell(
                        0,
                        7,
                        f"• {linie}"
                    )

    else:

        pdf.multi_cell(
            0,
            7,
            "Nu a fost introdusă experiența."
        )

    pdf.ln(5)

    # declaratie
    
    pdf.set_draw_color(220, 220, 220)
    pdf.line(20, pdf.get_y(), 190, pdf.get_y())

    pdf.ln(5)

    pdf.set_font("DejaVu", "I", 9)
    pdf.set_text_color(120, 120, 120)

    pdf.multi_cell(
        0,
        5,
        "CV generat automat folosind aplicația AI Resume Builder & Optimizer."
    )

    pdf_bytes = pdf.output(dest="S")

    if isinstance(pdf_bytes, bytearray):
        pdf_bytes = bytes(pdf_bytes)

    if isinstance(pdf_bytes, str):
        pdf_bytes = pdf_bytes.encode("latin1")

    return pdf_bytes
