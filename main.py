import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from utils import extract_answer_from_image, explain_answer_if_requested

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

# /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Ciao! Inviami una foto con le domande e ti darò le risposte.")

# riceve foto
async def handle_image(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Sto elaborando l'immagine...")
    photo = update.message.photo[-1]
    file = await photo.get_file()
    image_path = "last_image.jpg"
    await file.download_to_drive(image_path)

    context.user_data["last_image_path"] = image_path

    try:
        answers = extract_answer_from_image(image_path)
        await update.message.reply_text(answers)
    except Exception as e:
        await update.message.reply_text(f"Errore durante l'elaborazione: {str(e)}")

# /spiega
async def spiega(update: Update, context: ContextTypes.DEFAULT_TYPE):
    image_path = context.user_data.get("last_image_path")
    if not image_path:
        await update.message.reply_text("Invia prima un'immagine per usare /spiega.")
        return

    try:
        explanation = explain_answer_if_requested(image_path)
        await update.message.reply_text(explanation)
    except Exception as e:
        await update.message.reply_text(f"Errore durante la spiegazione: {str(e)}")

def main():
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    app = ApplicationBuilder().token(token).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("spiega", spiega))
    app.add_handler(MessageHandler(filters.PHOTO, handle_image))

    # 🔁 Webhook (invece di run_polling)
    port = int(os.environ.get("PORT", 8443))
    webhook_url = f"https://{os.environ['RENDER_EXTERNAL_HOSTNAME']}/{token}"

    app.run_webhook(
        listen="0.0.0.0",
        port=port,
        url_path=token,
        webhook_url=webhook_url
    )

if __name__ == "__main__":
    main()
