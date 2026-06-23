import os
import google.generativeai as genai
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters

BOT_TOKEN = os.getenv("BOT_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-2.5-flash")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Hello! I am a Gemini-powered AI bot. Send me a message."
    )

async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text

    try:
        response = model.generate_content(user_message)
        await update.message.reply_text(response.text)
    except Exception as e:
        await update.message.reply_text(f"Error: {str(e)}")

def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))

    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
