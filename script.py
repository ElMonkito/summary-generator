import fitz  # PyMuPDF pour manipuler les fichiers PDF
import openai
import os
from tqdm import tqdm

# Récupération de la clé API depuis les variables d'environnement
API_KEY = os.getenv("OPENAI_API_KEY")
if API_KEY is None:
    raise ValueError("La clé API OpenAI n'est pas définie. Définissez OPENAI_API_KEY comme variable d'environnement.")

def extract_text_from_pdf(pdf_path):
    """Extrait le texte de toutes les pages d'un fichier PDF."""
    doc = fitz.open(pdf_path)
    text = ""
    for page in tqdm(doc, desc="Extraction du texte"):
        text += page.get_text("text") + "\n"
    return text

def summarize_text(text, model="gpt-3.5-turbo"):
    """Envoie une partie du texte à l'API OpenAI pour obtenir un résumé."""
    prompt = (
        "Voici une transcription de réunion Teams :\n\n"
        f"{text[:5000]}\n\n"
        "Fais-moi un résumé clair et concis des points importants."
    )

    client = openai.OpenAI(api_key=API_KEY)
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "Tu es un assistant qui résume des transcriptions de réunions dans la même langue que la transcription."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content

def save_summary_as_pdf(summary, output_path):
    """Crée un fichier PDF contenant le résumé fourni."""
    doc = fitz.open()
    page = doc.new_page()
    text_rect = fitz.Rect(50, 50, 550, 800)
    page.insert_textbox(text_rect, summary, fontsize=12, fontname="helv")
    doc.save(output_path)
    doc.close()

def process_pdf(pdf_path):
    """Traite un fichier PDF : extrait le texte, génère un résumé, et l'enregistre en PDF."""
    print("Extraction du texte...")
    text = extract_text_from_pdf(pdf_path)

    print("Génération du résumé...")
    summary = summarize_text(text)

    print("Résumé généré :\n")
    print(summary)

    output_dir = "C:/dev/epsic/testTranscription/resumes"
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, os.path.basename(pdf_path).replace(".pdf", "_resume.pdf"))

    save_summary_as_pdf(summary, output_path)
    print(f"Résumé sauvegardé dans : {output_path}")

if __name__ == "__main__":
    pdf_file = "Call_Valentin_Roth_Generated.pdf"
    process_pdf(pdf_file)
