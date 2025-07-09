import pytesseract
from PIL import Image
import openai
import os

# Imposta il percorso di Tesseract
pytesseract.pytesseract.tesseract_cmd = "/usr/bin/tesseract"

# Estrai testo da immagine
def extract_text_from_image(image_path):
    image = Image.open(image_path)
    text = pytesseract.image_to_string(image, lang='ita')
    return text

# Estrai solo le risposte corrette dal testo OCR
def extract_answer_from_image(image_path):
    text = extract_text_from_image(image_path)

    prompt = f"""Il seguente testo è stato estratto da un test a scelta multipla. 
Individua e restituisci SOLO le risposte corrette, in questo formato preciso:

1: A
2: C
3: B

TESTO:
\"\"\"
{text}
\"\"\"
"""

    client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Sei un assistente che restituisce solo le risposte corrette a un test."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2
    )

    return response.choices[0].message.content.strip()

# Spiega le risposte corrette
def explain_answer_if_requested(image_path):
    text = extract_text_from_image(image_path)

    prompt = f"""Il seguente testo è stato estratto da un test. Per ogni domanda, fornisci la risposta corretta e una spiegazione sintetica.

TESTO:
\"\"\"
{text}
\"\"\"
"""

    client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Sei un assistente che spiega brevemente le risposte corrette di un test."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3
    )

    return response.choices[0].message.content.strip()
