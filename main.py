from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackContext, MessageHandler, filters
from telegram.constants import ParseMode  # Оновлений імпорт для ParseMode
import config  # Імпортуємо файл з токеном

# Головне меню
main_menu_buttons = [['ℹ️ Інформація для профкому'], ['🎓 Інформація для студента']]

# Кнопки меню профкому
info_profkom_buttons = [['📝 Профспілкові питання', '💳 ISIC'], ['📋 Запити', '🎭 Актори'],
                        ['⚖️ Юридичні консультації', '🏥 Страховка'], ['🔙 Назад']]

# Кнопки меню для студента
info_student_buttons = [['📊 Рейтинговий список', '📚 Дисципліни для здачі'],
                        ['🌍 Академічна мобільність', '⚠️ Обмежена успішність'],
                        ['🌐 Для іноземців', '📖 Безкоштовні ресурси'], ['🔙 Назад']]


# Стартове повідомлення з привітанням та фото
async def start(update: Update, context: CallbackContext):
    print("Команда /start отримана")
    user_first_name = update.effective_user.first_name
    reply_markup = ReplyKeyboardMarkup(main_menu_buttons, resize_keyboard=True)

    greeting_message = (
        f"👋 Привіт, {user_first_name}!\n"
        "Вітаємо в офіційному Telegram-боті профкому ННІ 'Комп'ютерних наук та штучного інтелекту'!\n\n"
        "В нашому боті ви знайдете:\n\n"
        "1. 📢 Інформація від профкому: Додаткові бали, студентські карти, важлива інформація про діяльність профкому та інше.\n\n"
        "2. 📚 Інформація для студента: Рейтингові списки, вибіркові дисципліни, інформація для першокурсника та інші корисні ресурси."
    )

    # Відправка фотографії з привітальним текстом
    try:
        with open('ЧМ.jpg', 'rb') as photo:
            await context.bot.send_photo(chat_id=update.effective_chat.id, photo=photo, caption=greeting_message)
        await update.message.reply_text("Оберіть одну з опцій:", reply_markup=reply_markup)
    except FileNotFoundError:
        await update.message.reply_text("Фото не знайдено, але бот працює. Оберіть одну з опцій:", reply_markup=reply_markup)


# Головне меню та обробка відповідей
async def main_menu(update: Update, context: CallbackContext):
    text = update.message.text
    print(f"Отримано повідомлення: {text}")

    # Перевірка вибору в головному меню
    if text == 'ℹ️ Інформація для профкому':
        reply_markup = ReplyKeyboardMarkup(info_profkom_buttons, resize_keyboard=True)
        await update.message.reply_text("📌 Оберіть одну з категорій профкому:", reply_markup=reply_markup)
    elif text == '🎓 Інформація для студента':
        reply_markup = ReplyKeyboardMarkup(info_student_buttons, resize_keyboard=True)
        await update.message.reply_text("📚 Оберіть одну з категорій для студентів:", reply_markup=reply_markup)
    elif text == '🔙 Назад':
        reply_markup = ReplyKeyboardMarkup(main_menu_buttons, resize_keyboard=True)
        await update.message.reply_text("🔙 Повернення до головного меню.", reply_markup=reply_markup)
    else:
        # Якщо текст не відповідає жодній з опцій в меню, обробляємо як додатковий вибір
        await handle_response(update, context)


# Функція для обробки додаткових відповідей
async def handle_response(update: Update, context: CallbackContext):
    text = update.message.text
    print(f"Обробляється відповідь: {text}")

    if text == '📊 Рейтинговий список':
        # Відправка повідомлення з посиланням
        await update.message.reply_text(
            "📈 *Рейтинговий список студентів!*\n\n"
            "🔹 Перегляньте актуальні рейтинги студентів за спеціальностями, "
            "щоб дізнатися про свої досягнення та можливості.\n\n"
            "📎 [Натисніть тут, щоб переглянути рейтинг](https://karazin.ua/osvita/stipendialne-zabezpechennia/)\n\n",
            parse_mode=ParseMode.MARKDOWN
        )
    elif text in ['📚 Дисципліни для здачі', '🌍 Академічна мобільність', '⚠️ Обмежена успішність',
                  '🌐 Для іноземців', '📖 Безкоштовні ресурси']:
        await update.message.reply_text(f"✅ Ви обрали {text}. Зараз ця функція в розробці.")
    elif text in ['📝 Профспілкові питання', '💳 ISIC', '📋 Запити', '🎭 Актори',
                  '⚖️ Юридичні консультації', '🏥 Страховка']:
        await update.message.reply_text(f"✅ Ви обрали {text}. Зараз ця функція в розробці.")
    else:
        await update.message.reply_text("❗️ Оберіть дійсний пункт меню.")


if __name__ == '__main__':
    # Ініціалізуємо бот, використовуючи токен з config.py
    app = ApplicationBuilder().token(config.BOT_TOKEN).build()

    # Обробники команд
    app.add_handler(CommandHandler('start', start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, main_menu))

    print("Бот запущено...")
    app.run_polling()
