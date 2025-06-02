from db import init_db, add_note, get_notes
from db import delete_note_by_index, clear_notes
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import logging

# Для хранения заметок в оперативной памяти (пока без базы)
заметки = {}

# Включаем логирование (полезно)
logging.basicConfig(level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Я бот для заметок. Используй /add чтобы добавить, /list чтобы посмотреть.")

async def add(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    текст = " ".join(context.args)
    if not текст:
        await update.message.reply_text("❌ Ты не указал текст заметки.")
        return

    add_note(user_id, текст)
    await update.message.reply_text("✅ Заметка сохранена!")

async def list_notes(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_notes = get_notes(user_id)
    if not user_notes:
        await update.message.reply_text("У тебя пока нет заметок.")
    else:
        текст = "\n".join([f"{i+1}. {n}" for i, n in enumerate(user_notes)])
        await update.message.reply_text(f"📝 Твои заметки:\n{текст}")
        
async def delete_note(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if not context.args or not context.args[0].isdigit():
        await update.message.reply_text("❌ Укажи номер заметки. Пример: /delete 2")
        return

    index = int(context.args[0]) - 1
    success = delete_note_by_index(user_id, index)
    if success:
        await update.message.reply_text("🗑 Заметка удалена.")
    else:
        await update.message.reply_text("❌ Неверный номер заметки.")

async def clear_all_notes(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    clear_notes(user_id)
    await update.message.reply_text("🧹 Все твои заметки удалены.")
    
from db import init_db, add_note, get_notes

init_db()

from os import getenv
app = ApplicationBuilder().token(getenv("BOT_TOKEN")).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("add", add))
app.add_handler(CommandHandler("list", list_notes))
app.add_handler(CommandHandler("delete", delete_note))
app.add_handler(CommandHandler("clear", clear_all_notes))

app.run_polling()
