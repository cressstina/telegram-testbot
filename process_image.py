def extract_and_answer(image_path):
    text = perform_ocr(image_path)
    answers, explanations = analyze_text_and_answer(text)
    result_string = "\n".join(answers)
    explanation_string = "\n".join(explanations)
    return result_string, explanation_string

def perform_ocr(image_path):
    import pytesseract
    from PIL import Image
    image = Image.open(image_path)
    text = pytesseract.image_to_string(image, lang='ita')  # o 'eng' se in inglese
    return text

def analyze_text_and_answer(text):
    # Analisi del testo e generazione risposte (logica temporanea)
    answers = []
    explanations = []

    # Esempio fittizio
    answers.append("1: C")
    explanations.append("La risposta corretta è C perché...")

    return answers, explanations
