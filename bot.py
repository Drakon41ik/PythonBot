from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
import sqlite3

application = Application.builder().token('7917032400:AAEVGpD2MQ7y4e3ndYGZzAOWzXa5N3vQbGQ').build()

# Функция для команды /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_message = (
        "Привет! Меня зовут 'Drakon41ik'!\n"
        "Я помогу тебе выбрать, что ты хочешь купить.\n"
        "Попробуй следующие команды:\n"
        "/menu - покажет все команды\n"
        "/buy_money - купить монеты\n"
        "/help - подсказка по доступным командам"
    )
    await update.message.reply_text(welcome_message)

# Настройка базы данных
def setup_database():
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        chat_id INTEGER NOT NULL UNIQUE,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS bookings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        start TEXT NOT NULL,
        buy_money TEXT NOT NULL,
        FOREIGN KEY(user_id) REFERENCES users(id)
    )
    """)

    connection.commit()
    connection.close()
    print("База данных успешно настроена")

# Добавление пользователя в базу данных
def add_user(username: str, chat_id: int):
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()
    try:
        cursor.execute("""
        INSERT OR IGNORE INTO users (username, chat_id)
        VALUES (?, ?)
        """, (username, chat_id))
        connection.commit()
        print(f"Пользователь {username} успешно добавлен.")
    except sqlite3.Error as e:
        print(f"Ошибка при добавлении пользователя: {e}")
    finally:
        connection.close()

# Добавление бронирования в базу данных
def add_booking(chat_id: int, start: str, buy_money: str):
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT id FROM users WHERE chat_id = ?", (chat_id,))
        user_id = cursor.fetchone()
        if user_id:
            user_id = user_id[0]
            cursor.execute("""
            INSERT INTO bookings (user_id, start, buy_money)
            VALUES (?, ?, ?)
            """, (user_id, start, buy_money))
            connection.commit()
            print("Бронирование успешно добавлено.")
        else:
            print("Пользователь с указанным chat_id не найден.")
    except sqlite3.Error as e:
        print(f"Ошибка при добавлении бронирования: {e}")
    finally:
        connection.close()

# Обработка кнопок
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.data == "buy_money":
        await query.message.reply_text("Какую сумму вы хотите купить?")
    elif query.data == "menu":
        await query.message.reply_text("Я предлагаю посмотреть, что вы можете купить.")

# Отправка фотографий
async def send_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    photo_paths = ["img/для_серва.png"]

    try:
        media_group = [InputMediaPhoto(open(photo, "rb")) for photo in photo_paths]
        await update.message.reply_media_group(media_group)
    except FileNotFoundError as e:
        await update.message.reply_text(f"Ошибка: файл {e.filename} не найден.")
    except Exception as e:
        await update.message.reply_text(f"Произошла ошибка: {str(e)}")



# Регистрация обработчиков
application.add_handler(CommandHandler("start", start))
application.add_handler(CallbackQueryHandler(button_handler))
application.add_handler(CommandHandler("sendphoto", send_photo))
# Настройка базы данных
setup_database()

if __name__ == "__main__":
    application.run_polling()
    
