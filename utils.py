import pytesseract
from PIL import Image
import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

def extract_answer_from_image(image_path):
    image = Image.open(image_path)
    text = pytesseract.image_to_string(image, lang="ita")

    prompt = (
        "Individua solo le risposte corrette alle domande riportate di seguito. "
        "Scrivi soltanto il numero della domanda seguito da due punti e la lettera della risposta corretta. "
        "Esempio: '1: C'.\n\n"
        f"{text}"
    )

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )

    answer = response.choices[0].message.content.strip()
    return answer

def explain_answer_if_requested():
    return "Funzione di spiegazione attiva. A breve riceverai la spiegazione."
