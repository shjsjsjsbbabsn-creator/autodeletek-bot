import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, filters, ContextTypes
from flask import Flask
from threading import Thread

TOKEN = "8687782635:AAGmWfcX0y045kNql_WzS7_oa_HJIClI_0A"
DELETE_TIME = 60  # 1 minute

# -------- DELETE FUNCTION --------
async def delete_later(message):
    await asyncio.sleep(DELETE_TIME)
    try:
        await message.delete()
    except:
        pass

# -------- MESSAGE HANDLER --------
async def auto_delete(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message:
        asyncio.create_task(delete_later(update.message))

# -------- START COMMAND --------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "✅ Bot is online!\n\n"
        "⏳ Sab messages 1 minute me auto delete ho jayenge."
    )

# -------- KEEP ALIVE --------
app = Flask('')

@app.route('/')
def home():
    return "Bot Running"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    Thread(target=run).start()

# -------- MAIN --------
def main():
    keep_alive()

    app_bot = ApplicationBuilder().token(TOKEN).build()

    # handlers
    app_bot.add_handler(CommandHandler("start", start))
    app_bot.add_handler(MessageHandler(filters.ALL, auto_delete))

    print("Bot Started...")
    app_bot.run_polling()

if __name__ == "__main__":
    main()
