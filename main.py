import os
import logging
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
)

from utils import extract_answer_from_image, explain_answer_if_requested

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Ciao! Inviami un'immagine con domande a scelta multipla.")

async def handle_image(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Sto elaborando...")

    photo = update.message.photo[-1]
    file = await photo.get_file()
    image_path = "/tmp/temp.jpg"
    await file.download_to_drive(image_path)

    answer = extract_answer_from_image(image_path)
    await update.message.reply_text(answer)

async def handle_spiega(update: Update, context: ContextTypes.DEFAULT_TYPE):
    explanation = explain_answer_if_requested()
    await update.message.reply_text(explanation)

def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("spiega", handle_spiega))
    app.add_handler(MessageHandler(filters.PHOTO, handle_image))

    app.run_polling()

if __name__ == "__main__":
    main()
