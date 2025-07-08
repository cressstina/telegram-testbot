import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from utils import extract_answer_from_image, explain_answer_if_requested

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
app = ApplicationBuilder().token(TOKEN).build()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Ciao! Inviami una foto del test e ti dirò le risposte.")

async def handle_image(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Sto elaborando l'immagine...")
    photo_file = await update.message.photo[-1].get_file()
    image_path = "temp_image.jpg"
    await photo_file.download_to_drive(image_path)

    answer = extract_answer_from_image(image_path)
    await update.message.reply_text(answer)

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if "/spiega" in update.message.text.lower():
        explanation = explain_answer_if_requested()
        await update.message.reply_text(explanation)

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.PHOTO, handle_image))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

if __name__ == "__main__":
    app.run_polling()
