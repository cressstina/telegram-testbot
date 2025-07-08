import pytesseract
from PIL import Image
import openai
import os
import io

def extract_text_from_image(file_bytes):
    image = Image.open(io.BytesIO(file_bytes))
    text = pytesseract.image_to_string(image, lang='ita')
    return text

def extract_answer_from_image(file_bytes):
    image_text = extract_text_from_image(file_bytes)

    prompt = f"""Ti fornisco il testo OCR di una foto con domande a scelta multipla.
Estrai solo le risposte corrette, in questo formato (e nient'altro):

1: A
2: C
3: B

TESTO OCR:
\"\"\"
{image_text}
\"\"\"
"""

    openai.api_key = os.getenv("OPENAI_API_KEY")

    response = openai.ChatCompletion.create(
        model="gpt-4",  # oppure "gpt-3.5-turbo" se preferisci
        messages=[
            {"role": "system", "content": "Sei un assistente che restituisce solo le risposte corrette a un quiz."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2
    )

    return response.choices[0].message.content.strip()

def explain_answer_if_requested(file_bytes):
    image_text = extract_text_from_image(file_bytes)

    prompt = f"""Ti fornisco il testo OCR di una foto con domande a scelta multipla.
Per ogni domanda, dammi la risposta corretta e spiega perché è quella giusta, in modo conciso.

TESTO OCR:
\"\"\"
{image_text}
\"\"\"
"""

    openai.api_key = os.getenv("OPENAI_API_KEY")

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "Sei un assistente che risponde a quiz con spiegazione delle risposte."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.5
    )

    return response.choices[0].message.content.strip()
