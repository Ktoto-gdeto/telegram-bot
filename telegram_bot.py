import json
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters,
)

# Токен вашего бота
TOKEN = os.getenv("TOKEN")

# Прогресс пользователя сохраняется в файл
PROGRESS_FILE = "progress.json"

# Задания для шифров (первая часть)
tasks = {
    "384526": {
        "task": "В апреле 2006 беглый босс сицилийской мафии Бернардо Провенцано по кличке «Трактор Бинну» был пойман в окрестностях Корлеоне. Он обладал ценной информацией, которую от него пытались узнать полицейские в течение нескольких месяцев. Все было тщетно! Но в один из дней смотритель заметил, что в книгах, которые читал Бернардо, подчеркнуты определённые слова. Он решил выписать первые буквы этих слов. Теперь это твоё задание — расшифровать сообщение!",
        "cipher": "Фш ъсъчм црнвё!",
        "hints": [
            "Посмотри алфавит",
            "Похоже на шифр Цезаря",
            "Сдвиг на нашу семью вправо",
            "Попроси помощи у ближнего!"
        ],
        "answer": ["ты очень умная"]
    },
    "917543": {
        "task": "Первые люди успешно прилетели на Марс. Во время посадки их основной аппарат связи вышел из строя. Они смогли настроить резервное оборудование, но оно передаёт сообщения в странном формате. Последнее сообщение пришло именно к тебе. Расшифруй его и помоги экипажу!",
        "cipher": "d0a2d18b20d0bcd0bed0bbd0bed0b4d0b5d18621",
        "hints": [
            "Бывают не только десятичные системы счисления",
            "Это шестнадцатиричная система",
            "https://www.hextotext.com/ru/convert-hex-to-text"
        ],
        "answer": ["ты молодец"]
    },
    "231678": {
        "task": "Старый поэт однажды написал своей возлюбленной акростих, скрыв в нем тайное послание. Твоя задача — раскрыть это сообщение, пройдя сквозь строки его письма.",
        "cipher": "Яркий свет в окне мерцая,\nТеплотой наполняет меня.\nЕжедневно живешь ты не зная,\nБесконечно люблю лишь тебя.\nЯсный день мне напомнит о встрече, а\nЛюбовь не умрет никогда.\nЮной грудью расправила плечи.\nБесценна для меня ты всегда.\nЛучше вместе в обнимку вечер\nЮг, да хоть север. С тобою в любые места",
        "hints": [
            "Первые буквы"
        ],
        "answer": ["я тебя люблю"]
    },
    "852014": {
        "task": "Один человек умер, оставив в этом мире свою жену, которую он любил больше всего на свете. Будучи добрым человеком, он получил разрешение передать жене сообщение из загробного мира. Но его ограничили: всего 13 символов. Он подумал и нашел выход из ситуации: его жена обожала комедийные сериалы и он передал ей зашифрованное сообщение (ответ должен быть на английском):",
        "cipher": "ТБВ.5.1.20.48",
        "hints": [
            "Т — Теория",
            "Б — Большого",
            "В — Взрыва",
            "5 — Сезон",
            "1 — Серия",
            "20 — Минута",
            "48 — Секунда"
        ],
        "answer": ["i am proud of you", "i'm proud of you"]
    },
    "605839": {
        "task": "Ты — капитан исследовательского корабля в открытом космосе. Тебе удалось перехватить старинный сигнал, который путешествовал между звёздами более 1000 лет. Это сообщение оставили когда-то давно, чтобы поздравить кого-то с праздником. Расшифруй его, чтобы узнать, что именно тебе хотели сказать!",
        "cipher": "--... .--- . .-.. .- ..-. --- .-. / . -. --- .-.. . -.-. .-. . - / -.. . .-.-.- / \n- .-. .-. -.-- / .. -. ...- .. . - / .- .-. ..-. .. .-. --..-- / \n..-. --- .-. / -.-- --- ..- / -- -.-- .-.-.-",
        "hints": [
            "Азбука Морзе",
            "Воспользуйся онлайн сервисами"
        ],
        "answer": ["желаю тебе всего самого наилучшего в новом году"]
    },
    "492710": {
        "task": "Легенда гласит, что на вершине самой высокой горы жил мудрец, который умел находить слова истины даже в хаосе. Чтобы передать своё послание, он использовал метод, где все буквы перемешаны. Разбери хаос, чтобы найти истину в этом сообщении",
        "cipher": "юЖаел етбе аьстчяс!",
        "hints": [
            "Переставь буквы",
            "Напиши всё маленькими буквами с восклицательным знаком"
        ],
        "answer": ["желаю тебе счастья"]
    },
    "731546": {
        "task": "Жил мудрец, который верил, что важные моменты жизни можно выразить числами. Он сложил все самые ценные воспоминания и получил число, которое содержало тайное послание. Сможешь ли ты повторить его путь и найти это число?",
        "cipher": "Числа для сложения:\nКомната в шестом общежитии.\nКоличество лет, которое мы женаты.\nКоличество лет, сколько мы встречаемся.\nГод свадьбы.\nНомер вашей квартиры.\nГод появления Уны.\nГод появления Бумы и Барка.\nКоличество человек на праздновании Нового года (с подвохом*)",
        "hints": [
            "Кристина была беременна",
            "326",
            "6",
            "11",
            "2018",
            "268",
            "2020",
            "2021"
        ],
        "answer": ["6675"]
    },
    "268413": {
        "task": "Древний математик однажды решил зашифровать своё послание в числах. Считая, что каждая буква имеет своё место в алфавите, он закодировал текст и спрятал его. Твоя задача — расшифровать этот шифр и понять, что он хотел сказать.",
        "cipher": "23 16 25 21 25 22 16 1 18 16 22 5 20 29 16 25 1 21 12 1 19 25",
        "hints": [
            "Алфавит"
        ],
        "answer": ["хочу чтобы ты радовалась"]
    },
    "159738": {
        "task": "На далёкой планете жили двое. У них был свой секретный язык, который никто не понимал. Одно слово особенно выделялось среди других — им они ласково называли друг друга. Вспомни это слово и напиши его.",
        "cipher": "Какое слово вы друг друга ласково называли?",
        "hints": [
            "Появилось оно у них примерно в 2021, один из них неправильно написал слово, и оно забавно звучало",
            "Котенок*"
        ],
        "answer": ["конок"]
    },
    "407962": {
        "task": "Когда-то великий детектив Шерлок Холмс оставил тайное послание в одной из своих загадок. Говорят, что оно скрыто в книге, связанной с его приключениями. Твоя задача — найти это послание. Перед отъездом по важному делу Холмс успел написать подсказку на обрывке бумаги:",
        "cipher": "you are the '49/3/11(+12)'",
        "hints": [
            "Книга",
            "Замени цифры на слова из книги без кавычек (писать нужно на английском)"
        ],
        "answer": ["you are the most beautiful"]
    }
}

# Вопросы второй части
QUESTIONS = {
    1: {
        "photo": "C:\\Users\\user\\Desktop\\Python\\1.1.jpg",
        "story": "Крысиный король держит в страхе деревушку...",
        "hints": [
            {"type": "text", "content": "Считать нужно дома."},
            {"type": "text", "content": "Подумай ещё раз!"},
            {"type": "photo", "content": "AgACAgIAAxkBAAMFZ2dF0SwqOyywQeJIxvyRHBRLiTQAAlLuMRuMbzhLzW_LyukKuTIBAAMCAAN5AAM2BA"},
        ],
        "answer": ["4", "четыре", "четыре дома", "4 дома"],
    },
    2: {
        "photo": "",
        "story": "",
        "hints": [
            {"type": "text", "content": "Считать нужно домА."},
            {"type": "text", "content": "Подумай ещё раз!"},
            {"type": "photo", "content": "AgACAgIAAxkBAAMFZ2dF0SwqOyywQeJIxvyRHBRLiTQAAlLuMRuMbzhLzW_LyukKuTIBAAMCAAN5AAM2BA"},
        ],
        "answer": ["4", "четыре", "четыре дома", "4 дома"],
    },
    # Добавьте остальные вопросы...
}

# Загрузка прогресса
def load_progress():
    try:
        with open(PROGRESS_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

# Сохранение прогресса
def save_progress(progress):
    with open(PROGRESS_FILE, "w", encoding="utf-8") as file:
        json.dump(progress, file, ensure_ascii=False, indent=4)

# Прогресс пользователей
progress = load_progress()

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    if user_id not in progress:
        progress[user_id] = {
            "stage": "DECODING",  # Начальный этап
            "completed_tasks": [],  # Выполненные задания
            "current_task": None,  # Текущее задание
            "current_question": 1,  # Текущий вопрос во второй части
            "hints_used": 0         # Количество использованных подсказок
        }
        save_progress(progress)
    await update.message.reply_text("Привет! Введи пароль из первого подарка, чтобы начать!")

# Обработка паролей и ответов
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    text = update.message.text.strip()

    if user_id not in progress:
        await update.message.reply_text("Используйте /start, чтобы начать!")
        return

    stage = progress[user_id]["stage"]

    if stage == "DECODING":
        if text in tasks:
            if text in progress[user_id]["completed_tasks"]:
                await update.message.reply_text("Ты уже выполнила это задание. Жду следующий пароль!")
            else:
                task = tasks[text]
                progress[user_id]["current_task"] = text
                save_progress(progress)

                # Отправляем задание с кнопкой "Подсказка"
                keyboard = [[InlineKeyboardButton("Подсказка", callback_data="hint")]]
                reply_markup = InlineKeyboardMarkup(keyboard)
                await update.message.reply_text(
                    f"{task['task']}\nШифр: {task['cipher']}",
                    reply_markup=reply_markup
                )
        elif progress[user_id]["current_task"]:
            current_task = progress[user_id]["current_task"]
            task = tasks[current_task]
            if text.lower() in [ans.lower() for ans in task["answer"]]:
                progress[user_id]["completed_tasks"].append(current_task)
                progress[user_id]["current_task"] = None
                save_progress(progress)

                await update.message.reply_text("Поздравляю! Ты справилась с заданием! Жду следующий пароль из подарка.")

                if len(progress[user_id]["completed_tasks"]) == len(tasks):
                    progress[user_id]["stage"] = "QUESTIONS"
                    save_progress(progress)
                    await update.message.reply_text("Отлично! Ты разгадала все шифры! Теперь начинается приключение!")
                    await send_question(update, context)
            else:
                await update.message.reply_text("Ответ неверный. Попробуй ещё раз!")
        else:
            await update.message.reply_text("Пароль неверный. Попробуй ещё раз!")

    elif stage == "QUESTIONS":
        await handle_question_answer(update, context)

# Подсказка
async def hint(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_id = str(query.from_user.id)
    stage = progress[user_id]["stage"]

    if stage == "DECODING":
        current_task = progress[user_id]["current_task"]
        if not current_task:
            await query.message.reply_text("Сначала введите пароль!")
            return

        task = tasks[current_task]
        hints_used = progress[user_id]["hints_used"]

        if hints_used < len(task["hints"]):
            hint_text = task["hints"][hints_used]
            progress[user_id]["hints_used"] += 1
            save_progress(progress)
            await query.message.reply_text(f"Подсказка: {hint_text}")
        else:
            await query.message.reply_text("Все подсказки уже использованы!")
    elif stage == "QUESTIONS":
        current_question = progress[user_id]["current_question"]
        question = QUESTIONS[current_question]
        hints = question["hints"]
        hints_used = progress[user_id]["hints_used"]

        if hints_used < len(hints):
            hint = hints[hints_used]
            if hint["type"] == "text":
                await query.message.reply_text(hint["content"])
            elif hint["type"] == "photo":
                await context.bot.send_photo(chat_id=query.message.chat_id, photo=hint["content"])
            progress[user_id]["hints_used"] += 1
            save_progress(progress)
        else:
            await query.message.reply_text("Все подсказки уже использованы!")

# Отправка вопросов из второй части
async def send_question(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    current_question = progress[user_id]["current_question"]
    question = QUESTIONS.get(current_question)

    if question:
        keyboard = [[InlineKeyboardButton("Подсказка", callback_data="hint")]]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await context.bot.send_photo(chat_id=update.effective_chat.id, photo=question["photo"])
        await update.message.reply_text(question["story"], reply_markup=reply_markup)
    else:
        await update.message.reply_text(
            "Поздравляю! Ты прошла этот квест! Поднимись к друзьям, назови пароль 'С Новым Годом' и получи подарок!"
        )

# Обработка ответов на вопросы
async def handle_question_answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    current_question = progress[user_id]["current_question"]
    question = QUESTIONS[current_question]
    user_answer = update.message.text.strip().lower()

    if user_answer in [ans.lower() for ans in question["answer"]]:
        progress[user_id]["current_question"] += 1
        save_progress(progress)
        if current_question + 1 > len(QUESTIONS):
            await update.message.reply_text("Поздравляю! Ты прошла этот квест! Поднимись к друзьям и получи подарок!")
        else:
            await send_question(update, context)
    else:
        await update.message.reply_text("Неправильно! Попробуй ещё раз или нажми 'Подсказка'.")

# Сброс прогресса
async def reset(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    if user_id in progress:
        del progress[user_id]
        save_progress(progress)
        await update.message.reply_text("Ваш прогресс был сброшен. Начнём заново! Отправьте /start.")
    else:
        await update.message.reply_text("У вас ещё нет сохранённого прогресса.")

# Основной запуск
def main():
    application = ApplicationBuilder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(hint, pattern="hint"))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.add_handler(CommandHandler("reset", reset))

    print("Бот запущен!")
    application.run_polling()

if __name__ == "__main__":
    main()
