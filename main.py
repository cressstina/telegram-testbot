import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, ContextTypes, filters
from utils import extract_answer_from_image, explain_answer_if_requested
import os

# Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Variabili di ambiente
BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")

# Gestore dei messaggi con immagini
async def handle_image(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Sto elaborando…")
    photo_file = await update.message.photo[-1].get_file()
    image_path = "/tmp/temp.jpg"
    await photo_file.download_to_drive(image_path)

    answer = extract_answer_from_image(image_path)
    context.user_data["last_answer"] = answer
    await update.message.reply_text(answer)

# Comando /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Ciao! Inviami la foto di un test e ti dirò la risposta corretta. Scrivi /spiega se vuoi una spiegazione dopo la risposta.")

# Comando /spiega
async def spiega(update: Update, context: ContextTypes.DEFAULT_TYPE):
    last_answer = context.user_data.get("last_answer")
    if last_answer:
        explanation = explain_answer_if_requested(last_answer)
        await update.message.reply_text(explanation)
    else:
        await update.message.reply_text("Per favore invia prima una foto del test.")

# Main
if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("spiega", spiega))
    app.add_handler(MessageHandler(filters.PHOTO, handle_image))

    app.run_polling()
