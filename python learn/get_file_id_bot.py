from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, ContextTypes
from telegram.ext import filters

# Обработчик для получения file_id фото
async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        if update.message.photo:  # Проверяем, что сообщение содержит фото
            file_id = update.message.photo[-1].file_id  # Берём самое большое фото (лучшее качество)
            await update.message.reply_text(f"File ID: {file_id}")
        else:
            await update.message.reply_text("Пожалуйста, отправьте фото.")
    except Exception as e:
        # Если произошла ошибка, сообщаем пользователю и логируем её
        await update.message.reply_text("Произошла ошибка при обработке фото.")
        print(f"Ошибка: {e}")

# Обработчик команды /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Отправь мне фото, и я пришлю тебе его file_id.")

# Обработчик текстовых сообщений
async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Я могу обрабатывать только фото. Попробуйте снова!")

def main():
    TOKEN = "7714309682:AAE1kUNUvT94MjH3SJvnOvJPdF_X1q2dlWA"  # Замените на токен вашего второго бота
    application = ApplicationBuilder().token(TOKEN).build()

    # Обработчик для команды /start
    application.add_handler(CommandHandler("start", start))

    # Обработчик для фотографий
    application.add_handler(MessageHandler(filters.PHOTO, handle_photo))

    # Обработчик для любых других сообщений
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

    application.run_polling()  # Запускаем бота

if __name__ == "__main__":
    main()
