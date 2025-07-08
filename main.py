import os
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)
from process_image import extract_and_answer

TELEGRAM_BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
last_explanations = {}

# /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Ciao! Inviami una foto del test. Ti risponderò con le risposte corrette.")

# gestione immagini
async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Sto elaborando...")

    photo_file = await update.message.photo[-1].get_file()
    photo_path = await photo_file.download_to_drive()

    results, explanations = extract_and_answer(photo_path)

    chat_id = update.message.chat_id
    last_explanations[chat_id] = explanations

    await update.message.reply_text(results)

# /spiega
async def spiega(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    if chat_id in last_explanations:
        await update.message.reply_text(last_explanations[chat_id])
    else:
        await update.message.reply_text("Inviami prima una foto del test per ottenere una spiegazione.")

def main():
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("spiega", spiega))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    app.run_polling()

if __name__ == "__main__":
    main()
