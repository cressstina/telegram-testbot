import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from utils import extract_answer_from_image, explain_answer_if_requested

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# Comando /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Ciao! Inviami una foto con domande a risposta multipla e ti dirò le risposte corrette.\nScrivi /spiega per avere spiegazioni.")

# Comando /spiega
async def spiega(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.user_data.get("last_image_text"):
        explanation = explain_answer_if_requested(context.user_data["last_image_text"])
        await update.message.reply_text(explanation)
    else:
        await update.message.reply_text("Non ho ancora ricevuto un'immagine. Inviamene una prima!")

# Quando arriva una foto
async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Sto elaborando l'immagine...")

    photo_file = await update.message.photo[-1].get_file()
    photo_path = await photo_file.download_to_drive()

    try:
        answers, full_text = extract_answer_from_image(photo_path)
        context.user_data["last_image_text"] = full_text

        if answers:
            formatted = '\n'.join(f"{k}: {v}" for k, v in answers.items())
            await update.message.reply_text(formatted)
        else:
            await update.message.reply_text("Non sono riuscito a trovare risposte nell'immagine.")
    except Exception as e:
        logging.exception("Errore durante l'elaborazione della foto")
        await update.message.reply_text("Si è verificato un errore durante l'elaborazione dell'immagine.")

if __name__ == '__main__':
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("spiega", spiega))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))

    app.run_polling()
