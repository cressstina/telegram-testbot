import pytesseract
from PIL import Image
import openai
import os

def extract_text_from_image(image_path):
    image = Image.open(image_path)
    text = pytesseract.image_to_string(image, lang='ita')
    return text

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

    openai.api_key = os.getenv("OPENAI_API_KEY")
    response = openai.ChatCompletion.create(
        model="gpt-4",  # o "gpt-3.5-turbo"
        messages=[
            {"role": "system", "content": "Sei un assistente che restituisce solo le risposte corrette a un test."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2
    )

    return response.choices[0].message.content.strip()

def explain_answer_if_requested(image_path):
    text = extract_text_from_image(image_path)

    prompt = f"""Il seguente testo è stato estratto da un test. Per ogni domanda, fornisci la risposta corretta e una spiegazione sintetica.

TESTO:
\"\"\"
{text}
\"\"\"
"""

    openai.api_key = os.getenv("OPENAI_API_KEY")
    response = openai.ChatCompletion.create(
        model="gpt-4",  # o "gpt-3.5-turbo"
        messages=[
            {"role": "system", "content": "Sei un assistente che spiega brevemente le risposte corrette di un test."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3
    )

    return response.choices[0].message.content.strip()
