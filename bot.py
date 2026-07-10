import telebot
from telebot import types
import json
import os
from datetime import datetime
import time
import threading

# ===== ТВОЙ ТОКЕН =====
TOKEN = '8906637757:AAHDBpks4p14c7FyamVCxNpA9ayi_bIpEaE'  # ЗАМЕНИ НА СВОЙ ТОКЕН
bot = telebot.TeleBot(TOKEN)

DATA_FILE = 'data.json'

# Загружаем или создаем базу данных
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def save_data(data):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# Получить день недели
def get_day():
    days = ['ПН', 'ВТ', 'СР', 'ЧТ', 'ПТ', 'СБ', 'ВС']
    return days[datetime.now().weekday()]

# Клавиатура
def main_keyboard():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(types.KeyboardButton('📊 Мои замеры'), types.KeyboardButton('📝 Внести замер'))
    kb.add(types.KeyboardButton('📋 Тренировка на сегодня'), types.KeyboardButton('📈 Прогресс'))
    kb.add(types.KeyboardButton('❓ Техника упражнений'), types.KeyboardButton('🔄 Сбросить прогресс'))
    return kb

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 
        f"💪 Привет, боец! Твой рост 174 см, цель — 70 кг с рельефом.\n"
        f"Сегодня {get_day()}. Используй кнопки ниже.\n\n"
        f"📌 Твой план на неделю:\n"
        f"ПН — Грудь + Трицепс + Пресс\n"
        f"СР — Спина + Бицепс + Задняя дельта\n"
        f"ПТ — Ноги + Ягодицы + Икры\n"
        f"ВС — Плечи + Предплечья + Пресс\n\n"
        f"⚡ Не забудь: 3.5 л воды, вакуум живота каждый день, без сахара и хлеба на ужин!",
        reply_markup=main_keyboard())

@bot.message_handler(func=lambda m: m.text == '📋 Тренировка на сегодня')
def today_workout(message):
    day = get_day()
    plan = {
        'ПН': '🏋️ ГРУДЬ + ТРИЦЕПС:\n1. Жим штанги лежа 4х12\n2. Жим гантелей 3х15\n3. Разводка гантелей 3х15\n4. Отжимания узким хватом 3х20\n5. Тяга тренажера вниз 4х20\n6. Скручивания 3х25\n7. Скакалка 10 мин',
        'СР': '🏋️ СПИНА + БИЦЕПС:\n1. Подтягивания 5хмакс\n2. Тяга штанги к поясу 4х12\n3. Тяга гантели одной рукой 3х15\n4. Подъем гантелей на бицепс 3х15\n5. Молотки 3х15\n6. Супермен 3х20\n7. Скакалка 10 мин',
        'ПТ': '🏋️ НОГИ + ЯГОДИЦЫ:\n1. Приседания со штангой 4х12\n2. Румынская тяга 4х15\n3. Выпады с гантелями 3х12\n4. Приседания кубок 3х20\n5. Подъем на носки 4х25\n6. Бёрпи 3х15\n7. Скакалка 10 мин',
        'ВС': '🏋️ ПЛЕЧИ + ПРЕСС:\n1. Жим гантелей сидя 4х12\n2. Махи в стороны 4х15\n3. Махи перед собой 3х15\n4. Сгибания на предплечья 3х20\n5. Планка 3х60сек\n6. Обратные скручивания 3х20\n7. Скакалка 10 мин'
    }
    if day in plan:
        bot.send_message(message.chat.id, f"📅 Сегодня {day}\n\n{plan[day]}\n\n🔥 После тренировки — круг для живота: вакуум + скалолаз + бёрпи + планка.")
    else:
        bot.send_message(message.chat.id, f"📅 Сегодня {day} — ОТДЫХ!\nСделай растяжку, прогулку и вакуум живота 3 раза по 15 сек.")

@bot.message_handler(func=lambda m: m.text == '📝 Внести замер')
def enter_measure(message):
    bot.send_message(message.chat.id, "Введи данные в формате:\n`Вес 86, Талия 95, Грудь 110, Бицепс 38`", parse_mode='Markdown')

@bot.message_handler(func=lambda m: m.text and 'Вес' in m.text and 'Талия' in m.text)
def save_measure(message):
    try:
        text = message.text.replace(',', '.').split(',')
        data = {}
        for part in text:
            key, val = part.strip().split()
            key = key.strip().lower()
            val = float(val.strip().replace(',', '.'))
            if 'вес' in key:
                data['weight'] = val
            elif 'тали' in key:
                data['waist'] = val
            elif 'груд' in key:
                data['chest'] = val
            elif 'бицепс' in key or 'биц' in key:
                data['biceps'] = val
        
        if 'weight' not in data or 'waist' not in data:
            bot.send_message(message.chat.id, "❌ Ошибка. Введи как в примере: `Вес 86, Талия 95, Грудь 110, Бицепс 38`", parse_mode='Markdown')
            return
        
        db = load_data()
        uid = str(message.chat.id)
        if uid not in db:
            db[uid] = {'history': []}
        db[uid]['history'].append({
            'date': datetime.now().strftime('%d.%m.%Y'),
            **data
        })
        save_data(db)
        bot.send_message(message.chat.id, f"✅ Замеры сохранены!\nВес: {data['weight']} кг\nТалия: {data['waist']} см", reply_markup=main_keyboard())
    except Exception as e:
        bot.send_message(message.chat.id, f"❌ Ошибка. Формат: `Вес 86, Талия 95, Грудь 110, Бицепс 38`", parse_mode='Markdown')

@bot.message_handler(func=lambda m: m.text == '📊 Мои замеры')
def show_measures(message):
    db = load_data()
    uid = str(message.chat.id)
    if uid not in db or not db[uid]['history']:
        bot.send_message(message.chat.id, "📭 У тебя пока нет замеров. Внеси первый через кнопку '📝 Внести замер'.")
        return
    last = db[uid]['history'][-1]
    bot.send_message(message.chat.id, 
        f"📊 Твой последний замер (от {last.get('date', 'неизвестно')}):\n"
        f"⚖ Вес: {last.get('weight', '—')} кг\n"
        f"📏 Талия: {last.get('waist', '—')} см\n"
        f"📏 Грудь: {last.get('chest', '—')} см\n"
        f"💪 Бицепс: {last.get('biceps', '—')} см\n\n"
        f"🎯 Цель: 70 кг и рельеф. До цели осталось: {last.get('weight', 86) - 70} кг.")

@bot.message_handler(func=lambda m: m.text == '📈 Прогресс')
def progress(message):
    db = load_data()
    uid = str(message.chat.id)
    if uid not in db or len(db[uid]['history']) < 2:
        bot.send_message(message.chat.id, "📭 Нужно минимум 2 замера для анализа прогресса.")
        return
    hist = db[uid]['history']
    first = hist[0]
    last = hist[-1]
    w_diff = first.get('weight', 86) - last.get('weight', 86)
    t_diff = first.get('waist', 0) - last.get('waist', 0)
    bot.send_message(message.chat.id, 
        f"📈 Прогресс:\n"
        f"⚖ Вес: {first.get('weight', '?')} → {last.get('weight', '?')} кг (изменение: {w_diff:.1f} кг)\n"
        f"📏 Талия: {first.get('waist', '?')} → {last.get('waist', '?')} см (изменение: {t_diff:.1f} см)\n\n"
        f"{'✅ Отлично, продолжай!' if w_diff > 0 else '⚠️ Вес не уходит — убери углеводы на ужин.'}")

@bot.message_handler(func=lambda m: m.text == '❓ Техника упражнений')
def technique(message):
    bot.send_message(message.chat.id, 
        "📖 Основные правила техники:\n"
        "1️⃣ Приседания — спина прямая, колени НЕ внутрь, таз назад.\n"
        "2️⃣ Жим лёжа — опускать к соскам, локти в стороны, не выключать локти.\n"
        "3️⃣ Тяга штанги — спина ровная (как доска!), тянуть к пупку.\n"
        "4️⃣ Становая/Румынская — ноги чуть согнуты, спина прямая, штанга по голеням.\n"
        "5️⃣ Подтягивания — тянуться грудью, а не подбородком.\n"
        "6️⃣ Пресс — поясницу прижимать, выдох на усилии.\n"
        "7️⃣ Скакалка — прыгать на носках, колени согнуты, 45/15 сек.\n\n"
        "⚠️ Если болит сустав — уменьши вес, не ломай технику!")

@bot.message_handler(func=lambda m: m.text == '🔄 Сбросить прогресс')
def reset(message):
    db = load_data()
    uid = str(message.chat.id)
    if uid in db:
        del db[uid]
        save_data(db)
    bot.send_message(message.chat.id, "🔄 Прогресс сброшен. Начинаем с чистого листа!", reply_markup=main_keyboard())

@bot.message_handler(func=lambda m: True)
def fallback(message):
    bot.send_message(message.chat.id, "❓ Используй кнопки меню. Если хочешь внести замер — нажми '📝 Внести замер'.")

# ===== ЗАПУСК =====
print("🚀 Бот запущен и работает на Render!")
bot.polling(none_stop=True)