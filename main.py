import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, filters, ContextTypes
from PIL import Image
import pytesseract

# Logging
logging.basicConfig(level=logging.INFO)

TOKEN = os.getenv("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Benvenuto! Inviami una foto di un test.")

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    photo = update.message.photo[-1]
    file = await photo.get_file()
    image_path = "/tmp/image.jpg"
    await file.download_to_drive(image_path)

    text = pytesseract.image_to_string(Image.open(image_path), lang="ita")
    response = "Ecco il testo rilevato:\n\n" + text.strip()
    await update.message.reply_text(response)

if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    app.run_polling()
