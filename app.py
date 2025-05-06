import streamlit as st
from script import extract_text_from_pdf, summarize_text, save_summary_as_pdf

st.title("Résumé de transcription Teams (PDF)")

uploaded_file = st.file_uploader("Téléversez un fichier PDF", type="pdf")

if uploaded_file:
    st.info("Extraction du texte...")
    with open("temp.pdf", "wb") as f:
        f.write(uploaded_file.read())

    text = extract_text_from_pdf("temp.pdf")

    st.info("Génération du résumé...")
    summary = summarize_text(text)

    st.subheader("Résumé généré :")
    st.write(summary)

    save_summary_as_pdf(summary, "resume_output.pdf")

    with open("resume_output.pdf", "rb") as pdf_file:
        st.download_button("Télécharger le résumé en PDF", pdf_file, file_name="resume.pdf")
