from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto
from telegram.ext import Application,CommandHandler,CallbackQueryHandler, ContextTypes

async def start(update, context):
    w =(
    "Привет меня зовут 'Drakon41ik'!\n"
    "Я помогу тебе выбрать что ты хочешь купить.\n"
    "Попробуй следующие команды:\n"
    "/menu - покажет тебе все команды\n"
    "/buy_money - ты сможешь купить монеты\n"
    "/help - помогает тебе найти ту команду которая тебе нужна\n"
    )
    await update.message.reply_text(w)
async def button_handler(update, context):
    query=update.callback_query
    await query.answer()
    if query.data == "buy_money":
        await query.message.reply_text("какую суму ты хочешь купить")
    elif query.data == "menu":
        await query.message.reply_text("я тебе предлогаю посмотреть что ты можешь купить")
application = Application.builder().token('7917032400:AAEVGpD2MQ7y4e3ndYGZzAOWzXa5N3vQbGQ').build()
application.add_handler(CommandHandler("start", start))
#application.add_handler(CommandHandler("buy_money",buymoney)) немає такої команди

application.add_handler(CallbackQueryHandler(button_handler))


#InputMediaPhoto
async def send_photo(update,context):
    await update.message.replu_text(f"Виникла помилка:{str(e)}")

async def sales (update, context):
    room_image

   # Шляхи до локальних файлів
   photo_paths = ["img/для серва.png"]

   #Перевірка на існуваня файлів
   try:
       media_group = [InputMediaPhoto(open(photo, "rb")) for photo in photo_paths]
       await update.massege.reply_media_group(media_group)
   except FileNotFoundError as e:
       await update.massege.reply_text(f"Помилка: файл{e.filename} не знайдено.")
   except Exception as e:
       await update.massege.reply_text(f"Виникла помилка: {str(e)}")

application.add_handler(CommandHandler("sendphoto",send_photo))

if __name__ == '__main__':
    application.run_polling()
    
