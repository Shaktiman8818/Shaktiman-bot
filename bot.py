import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

# Replace with your own admin user ID
ADMIN_USER_ID = 806863163

movie_data = {}

logging.basicConfig(level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🎬 Welcome to Movie Bot! Send a movie name to get its link.")

async def add_movie(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_USER_ID:
        return await update.message.reply_text("❌ You are not authorized to add movies.")
    try:
        parts = update.message.text.split(" ", 1)[1].split("|")
        name, link = parts[0].strip(), parts[1].strip()
        movie_data[name.lower()] = link
        await update.message.reply_text(f"✅ Added: {name}")
    except:
        await update.message.reply_text("❌ Format: /add Movie Name | https://link")

async def get_movie(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.message.text.lower().strip()
    link = movie_data.get(query)
    if link:
        await update.message.reply_text(f"🎥 {query.title()}: {link}")
    else:
        await update.message.reply_text("❌ Movie not found.")

async def list_movies(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_USER_ID:
        return
    if movie_data:
        await update.message.reply_text("🎞️ Movies:
" + "
".join(movie_data.keys()))
    else:
        await update.message.reply_text("No movies added yet.")

async def delete_movie(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_USER_ID:
        return
    try:
        name = update.message.text.split(" ", 1)[1].strip().lower()
        if name in movie_data:
            del movie_data[name]
            await update.message.reply_text(f"🗑️ Deleted: {name}")
        else:
            await update.message.reply_text("❌ Movie not found.")
    except:
        await update.message.reply_text("❌ Format: /delete Movie Name")

if __name__ == '__main__':
    import os
    TOKEN = os.getenv("BOT_TOKEN")
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("add", add_movie))
    app.add_handler(CommandHandler("list", list_movies))
    app.add_handler(CommandHandler("delete", delete_movie))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, get_movie))

    app.run_polling()
