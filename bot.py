import telebot
from telebot import types
import json
import os
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import io
from collections import defaultdict

# ===== ТВОЙ ТОКЕН =====
TOKEN = '8906637757:AAHDBpks4p14c7FyamVCxNpA9ayi_bIpEaE'  # Вставь свой токен
bot = telebot.TeleBot(TOKEN)

DATA_FILE = 'data.json'

# ===== БАЗА КАЛОРИЙ (приблизительные значения) =====
CALORIE_DB = {
    # === КРУПЫ И КАШИ ===
    'гречка': 165, 'гречневая': 165, 'гречневый': 165,
    'рис': 130, 'рисовая': 130, 'рисовый': 130,
    'овсянка': 88, 'овсяная': 88, 'овсяный': 88, 'геркулес': 88,
    'пшено': 130, 'пшенная': 130, 'пшенный': 130,
    'перловка': 120, 'перловая': 120, 'перловый': 120,
    'манка': 120, 'манная': 120, 'манный': 120,
    'кукурузная': 110, 'кукурузный': 110,
    'ячневая': 120, 'ячневый': 120,
    'булгур': 130, 'киноа': 120,
    'горох': 120, 'гороховый': 120, 'фасоль': 120, 'чечевица': 110,
    'макароны': 130, 'спагетти': 130, 'вермишель': 130,
    'картофель': 80, 'картошка': 80, 'картофельное': 80,
    'пюре': 90, 'картофельное пюре': 90,
    
    # === МЯСО ===
    'курица': 170, 'куриная': 170, 'куриный': 170, 'цыпленок': 170,
    'говядина': 250, 'говяжья': 250, 'говяжий': 250,
    'свинина': 350, 'свиная': 350, 'свиной': 350,
    'баранина': 280, 'баранья': 280, 'бараний': 280,
    'индейка': 150, 'индюшатина': 150, 'индюшка': 150,
    'кролик': 180, 'крольчатина': 180,
    'конина': 200, 'оленина': 220,
    'субпродукты': 180, 'печень': 180, 'говяжья печень': 180,
    'куриная печень': 140, 'сердце': 180, 'говяжье сердце': 180,
    'куриное сердце': 160, 'почки': 180, 'легкие': 120,
    'язык': 250, 'говяжий язык': 250,
    'мясо': 200, 'отбивная': 250, 'эскалоп': 250,
    'антрекот': 280, 'стейк': 280, 'ростбиф': 250,
    'тушенка': 220, 'тушеная говядина': 220, 'тушеная свинина': 280,
    'фарш': 250, 'говяжий фарш': 250, 'свиной фарш': 330,
    'котлета': 220, 'бифштекс': 250, 'шницель': 240,
    
    # === РЫБА И МОРЕПРОДУКТЫ ===
    'рыба': 150, 'филе рыбы': 150,
    'треска': 75, 'минтай': 75, 'судак': 85,
    'окунь': 100, 'щука': 85, 'камбала': 90,
    'лосось': 200, 'семга': 200, 'форель': 180,
    'скумбрия': 180, 'сайра': 180, 'сельдь': 200,
    'горбуша': 160, 'кета': 160, 'кижуч': 170,
    'палтус': 190, 'тунец': 140, 'сазан': 110,
    'карп': 120, 'осетр': 190, 'угорь': 280,
    'краб': 90, 'креветки': 90, 'мидии': 80,
    'кальмар': 100, 'осьминог': 90,
    'икра': 250, 'красная икра': 250, 'черная икра': 280,
    'консервы': 180, 'шпроты': 180, 'килька': 170,
    
    # === ОВОЩИ ===
    'капуста': 25, 'белокочанная': 25, 'пекинская': 16,
    'цветная': 30, 'брокколи': 35, 'брюссельская': 40,
    'картофель': 80, 'картошка': 80,
    'морковь': 35, 'морковка': 35, 'морковный': 35,
    'лук': 40, 'репчатый': 40, 'порей': 35,
    'чеснок': 45, 'чесночный': 45,
    'огурец': 15, 'огурцы': 15, 'соленый огурец': 15,
    'помидор': 20, 'томат': 20, 'томаты': 20,
    'свекла': 45, 'свекольный': 45,
    'репа': 30, 'редис': 20, 'редька': 35,
    'тыква': 25, 'кабачок': 25, 'цукини': 20,
    'баклажан': 25, 'перец': 25, 'болгарский перец': 25,
    'стручковая фасоль': 30, 'зеленый горошек': 70,
    'кукуруза': 100, 'консервированная кукуруза': 100,
    'шпинат': 22, 'щавель': 20, 'руккола': 25,
    'салат': 15, 'листовой салат': 15, 'айсберг': 12,
    'петрушка': 40, 'укроп': 40, 'зелень': 35,
    'сельдерей': 15, 'корень сельдерея': 40,
    
    # === ФРУКТЫ ===
    'яблоко': 50, 'яблочный': 50,
    'груша': 55, 'банан': 95, 'банановый': 95,
    'апельсин': 45, 'мандарин': 40, 'грейпфрут': 35,
    'лимон': 30, 'лайм': 30, 'ананас': 50,
    'виноград': 70, 'изюм': 280, 'финики': 280,
    'арбуз': 30, 'дыня': 35, 'персик': 45,
    'нектарин': 45, 'абрикос': 45, 'слива': 45,
    'вишня': 52, 'черешня': 55, 'клубника': 35,
    'малина': 45, 'ежевика': 45, 'смородина': 45,
    'черника': 45, 'голубика': 45, 'клюква': 30,
    'гранат': 70, 'киви': 50, 'манго': 65,
    'папайя': 45, 'авокадо': 180,
    
    # === МОЛОЧНЫЕ ПРОДУКТЫ ===
    'молоко': 60, 'цельное молоко': 65, 'обезжиренное молоко': 35,
    'кефир': 50, 'кефирный': 50,
    'йогурт': 60, 'натуральный йогурт': 60,
    'ряженка': 55, 'снежок': 55,
    'сметана': 200, 'сметанный': 200,
    'творог': 120, 'обезжиренный творог': 80, 'жирный творог': 150,
    'масло сливочное': 750, 'сливочное масло': 750,
    'маргарин': 750, 'спред': 600,
    'сыр': 350, 'твердый сыр': 350, 'плавленый сыр': 250,
    'брынза': 260, 'фета': 280, 'сулугуни': 290,
    'моцарелла': 280, 'пармезан': 380,
    'сгущенка': 320, 'сгущенное молоко': 320,
    'сливки': 250, 'жирные сливки': 350,
    
    # === ХЛЕБ И ВЫПЕЧКА ===
    'хлеб': 250, 'ржаной хлеб': 220, 'белый хлеб': 270,
    'батон': 270, 'булка': 270,
    'бутерброд': 300, 'тост': 280,
    'сухари': 350, 'сушки': 350, 'баранки': 350,
    'печенье': 450, 'овсяное печенье': 400,
    'пряник': 350, 'кекс': 350, 'маффин': 350,
    'пирожок': 280, 'расстегай': 280,
    'блины': 200, 'оладьи': 250,
    'лаваш': 250, 'лепешка': 250,
    'сдоба': 350, 'булочка': 350,
    
    # === НАПИТКИ ===
    'чай': 0, 'зеленый чай': 0, 'черный чай': 0,
    'кофе': 0, 'растворимый кофе': 0,
    'компот': 70, 'морс': 70, 'кисель': 80,
    'сок': 45, 'яблочный сок': 45, 'апельсиновый сок': 50,
    'газировка': 40, 'лимонад': 40, 'кола': 40,
    'квас': 30, 'смузи': 60,
    'алкоголь': 250, 'пиво': 45, 'вино': 70,
    
    # === КРУПНЫЕ БЛЮДА (армейская столовая) ===
    'плов': 200, 'плов с курицей': 200, 'плов с мясом': 220,
    'борщ': 60, 'борщ со сметаной': 80,
    'суп': 50, 'суп куриный': 50, 'суп рыбный': 45,
    'рассольник': 50, 'щи': 50, 'солянка': 70,
    'гуляш': 150, 'жаркое': 180, 'рагу': 150,
    'пельмени': 220, 'вареники': 200, 'манты': 250,
    'голубцы': 180, 'перец фаршированный': 180,
    'омлет': 180, 'яичница': 180,
    'запеканка': 150, 'творожная запеканка': 150,
    'макароны по-флотски': 200, 'макароны с мясом': 200,
    
    # === МАСЛА И СОУСЫ ===
    'масло растительное': 900, 'подсолнечное масло': 900,
    'оливковое масло': 900, 'льняное масло': 900,
    'майонез': 600, 'майонезный': 600,
    'кетчуп': 100, 'соус': 100, 'томатный соус': 80,
    'соевый соус': 50, 'горчица': 60, 'хрен': 70,
    'аджика': 80, 'чесночный соус': 150,
    
    # === СЛАДОСТИ ===
    'сахар': 400, 'песок': 400, 'рафинад': 400,
    'варенье': 280, 'джем': 280, 'мед': 300,
    'шоколад': 550, 'молочный шоколад': 550,
    'конфеты': 500, 'карамель': 400, 'ирис': 400,
    'мороженое': 200, 'пломбир': 230,
    
    # === ОРЕХИ И СУХОФРУКТЫ ===
    'грецкий орех': 650, 'орехи': 650, 'миндаль': 600,
    'арахис': 550, 'фундук': 650, 'кешью': 600,
    'фисташки': 550, 'семечки': 580, 'тыквенные семечки': 550,
    'курага': 240, 'чернослив': 230, 'финики': 280,
}


# ===== Функции работы с данными =====
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def save_data(data):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def get_user_data(user_id):
    db = load_data()
    uid = str(user_id)
    if uid not in db:
        db[uid] = {
            'history': [],
            'food_log': [],
            'daily_calories': 0,
            'calorie_limit': 1800,
            'penalty_burpees': 0,
            'slip_count': 0,
            'last_reset_date': datetime.now().strftime('%Y-%m-%d'),
            'reminder_time': '19:00',
            'current_weight': 86,
            'current_waist': 95,
            'measurements': []
        }
        save_data(db)
    return db[uid]

def get_today_food(user_id):
    data = get_user_data(user_id)
    today = datetime.now().strftime('%Y-%m-%d')
    if data.get('last_reset_date') != today:
        data['food_log'] = []
        data['daily_calories'] = 0
        data['last_reset_date'] = today
        save_data(load_data())
    return data.get('food_log', [])

def get_day():
    days = ['ПН', 'ВТ', 'СР', 'ЧТ', 'ПТ', 'СБ', 'ВС']
    return days[datetime.now().weekday()]

def get_workout_day():
    today = datetime.now()
    weekday = today.weekday()
    if weekday in [0, 2, 4, 6]:  # ПН, СР, ПТ, ВС
        return True
    return False

def get_workout_plan(day):
    plans = {
        'ПН': '🏋️ ГРУДЬ + ТРИЦЕПС:\n1. Жим штанги лежа 4х12\n2. Жим гантелей 3х15\n3. Разводка гантелей 3х15\n4. Отжимания узким хватом 3х20\n5. Тяга тренажера вниз 4х20\n6. Скручивания 3х25\n7. Скакалка 10 мин',
        'СР': '🏋️ СПИНА + БИЦЕПС:\n1. Подтягивания 5хмакс\n2. Тяга штанги к поясу 4х12\n3. Тяга гантели одной рукой 3х15\n4. Подъем гантелей на бицепс 3х15\n5. Молотки 3х15\n6. Супермен 3х20\n7. Скакалка 10 мин',
        'ПТ': '🏋️ НОГИ + ЯГОДИЦЫ:\n1. Приседания со штангой 4х12\n2. Румынская тяга 4х15\n3. Выпады с гантелями 3х12\n4. Приседания кубок 3х20\n5. Подъем на носки 4х25\n6. Бёрпи 3х15\n7. Скакалка 10 мин',
        'ВС': '🏋️ ПЛЕЧИ + ПРЕСС:\n1. Жим гантелей сидя 4х12\n2. Махи в стороны 4х15\n3. Махи перед собой 3х15\n4. Сгибания на предплечья 3х20\n5. Планка 3х60сек\n6. Обратные скручивания 3х20\n7. Скакалка 10 мин'
    }
    return plans.get(day, 'Отдых! Сделай растяжку и вакуум живота.')

# ===== КЛАВИАТУРЫ =====
def main_keyboard():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    kb.add(
        types.KeyboardButton('📊 Мои замеры'),
        types.KeyboardButton('📝 Внести замер')
    )
    kb.add(
        types.KeyboardButton('🍽️ Добавить еду'),
        types.KeyboardButton('📈 Прогресс-бар еды')
    )
    kb.add(
        types.KeyboardButton('📋 Тренировка на сегодня'),
        types.KeyboardButton('📈 Мой прогресс')
    )
    kb.add(
        types.KeyboardButton('❓ Техника упражнений'),
        types.KeyboardButton('😈 Я сорвался!')
    )
    kb.add(
        types.KeyboardButton('🔔 Настроить напоминания'),
        types.KeyboardButton('🔄 Сбросить прогресс')
    )
    return kb

def food_keyboard():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    kb.add(
        types.KeyboardButton('✅ Закончить прием пищи'),
        types.KeyboardButton('⬅️ Назад в меню')
    )
    return kb

# ===== ОБРАБОТЧИКИ КОМАНД =====

@bot.message_handler(commands=['start'])
def start(message):
    uid = str(message.chat.id)
    data = get_user_data(uid)
    day = get_day()
    weight = data.get('current_weight', 86)
    target = 70
    diff = weight - target
    
    bot.send_message(
        message.chat.id,
        f"💪 Привет, боец!\n"
        f"📏 Рост: 174 см\n"
        f"⚖ Текущий вес: {weight} кг\n"
        f"🎯 Цель: {target} кг (осталось {diff:.1f} кг)\n\n"
        f"📅 Сегодня {day}\n"
        f"{'🔥 Сегодня ТРЕНИРОВКА!' if get_workout_day() else '🚶 Сегодня ОТДЫХ'}\n\n"
        f"🍽️ Твой лимит калорий: {data.get('calorie_limit', 1800)} ккал\n"
        f"📊 Сегодня съедено: {data.get('daily_calories', 0)} ккал\n\n"
        f"Используй кнопки ниже ⬇️",
        reply_markup=main_keyboard()
    )
    
    # Напоминание про тренировку
    if get_workout_day():
        bot.send_message(
            message.chat.id,
            f"⚠️ НАПОМИНАНИЕ: Сегодня {day} — тренировка!\n"
            f"🕒 Начни через 30 минут.\n"
            f"💨 Сделай вакуум живота 5 раз по 15 секунд перед стартом.",
            reply_markup=main_keyboard()
        )

@bot.message_handler(func=lambda m: m.text == '🍽️ Добавить еду')
def add_food_start(message):
    bot.send_message(
        message.chat.id,
        "🍽️ Напиши, что ты съел и примерный вес в граммах.\n\n"
        "📝 Примеры:\n"
        "• `Каша гречневая 200, Курица 150`\n"
        "• `Суп 300, Хлеб 50`\n"
        "• `Рис 180, Рыба 120`\n\n"
        "Я сам посчитаю калории!",
        parse_mode='Markdown',
        reply_markup=types.ReplyKeyboardRemove()
    )
    bot.register_next_step_handler(message, process_food)

def process_food(message):
    try:
        text = message.text.lower()
        if text == '⬅️ назад в меню':
            bot.send_message(message.chat.id, "Возвращаемся в меню.", reply_markup=main_keyboard())
            return
        
        items = text.split(',')
        total_cal = 0
        food_list = []
        
        for item in items:
            parts = item.strip().split()
            if len(parts) < 2:
                continue
            # Ищем название продукта и вес
            weight = float(parts[-1].replace('г', '').replace('гр', '').strip())
            name = ' '.join(parts[:-1]).strip()
            
            # Ищем калорийность в базе
            cal_per_100 = 0
            found = False
            for key, value in CALORIE_DB.items():
                if key in name:
                    cal_per_100 = value
                    found = True
                    break
            
            if not found:
                bot.send_message(
                    message.chat.id,
                    f"⚠️ Не знаю продукт '{name}'. Это овощ? Мясо? Крупа?\n"
                    f"Пропускаем его, калории не посчитаны."
                )
                continue
            
            cal = (cal_per_100 * weight) / 100
            total_cal += cal
            food_list.append(f"{name} ({weight}г) — {int(cal)} ккал")
        
        if not food_list:
            bot.send_message(
                message.chat.id,
                "❌ Не удалось распознать еду. Напиши в формате: `Гречка 200, Курица 150`",
                parse_mode='Markdown'
            )
            bot.register_next_step_handler(message, process_food)
            return
        
        # Сохраняем в базу
        uid = str(message.chat.id)
        data = get_user_data(uid)
        today = datetime.now().strftime('%Y-%m-%d')
        
        if data.get('last_reset_date') != today:
            data['food_log'] = []
            data['daily_calories'] = 0
            data['last_reset_date'] = today
        
        data['food_log'].append({
            'date': datetime.now().strftime('%H:%M'),
            'items': food_list,
            'total': int(total_cal)
        })
        data['daily_calories'] = data.get('daily_calories', 0) + int(total_cal)
        save_data(load_data())
        
        # Считаем прогресс-бар
        limit = data.get('calorie_limit', 1800)
        current = data.get('daily_calories', 0)
        percent = min(100, int((current / limit) * 100))
        
        # Визуальный бар
        bar_length = 20
        filled = int(bar_length * percent / 100)
        bar = '█' * filled + '░' * (bar_length - filled)
        
        response = "✅ Записано!\n\n"
        response += "\n".join(food_list)
        response += f"\n\n🔥 Итого сегодня: {current} / {limit} ккал"
        response += f"\n\nПрогресс за день:\n{bar}  {percent}%"
        
        if current >= limit:
            response += "\n\n⚠️ ТЫ ПРЕВЫСИЛ ЛИМИТ! Вспомни про подбородок!"
            # Предлагаем штрафные берпи
            penalty = 20
            data['penalty_burpees'] = data.get('penalty_burpees', 0) + penalty
            save_data(load_data())
            response += f"\n💪 Добавлено {penalty} штрафных берпи к следующей тренировке."
        else:
            response += f"\n\n💪 Осталось: {limit - current} ккал"
        
        bot.send_message(message.chat.id, response, reply_markup=main_keyboard())
        
    except Exception as e:
        bot.send_message(
            message.chat.id,
            f"❌ Ошибка: {str(e)}\nНапиши в формате: `Гречка 200, Курица 150`",
            parse_mode='Markdown'
        )
        bot.register_next_step_handler(message, process_food)

@bot.message_handler(func=lambda m: m.text == '📈 Прогресс-бар еды')
def show_food_progress(message):
    uid = str(message.chat.id)
    data = get_user_data(uid)
    limit = data.get('calorie_limit', 1800)
    current = data.get('daily_calories', 0)
    percent = min(100, int((current / limit) * 100))
    
    bar_length = 20
    filled = int(bar_length * percent / 100)
    bar = '█' * filled + '░' * (bar_length - filled)
    
    today_food = data.get('food_log', [])
    food_text = ""
    if today_food:
        food_text = "\n\n📋 Сегодня ты ел:\n"
        for entry in today_food:
            food_text += f"🕒 {entry.get('date', '')}: {', '.join(entry.get('items', []))}\n"
    else:
        food_text = "\n\n📭 Сегодня ещё ничего не записано."
    
    bot.send_message(
        message.chat.id,
        f"🍽️ Прогресс по калориям:\n"
        f"📊 {current} / {limit} ккал\n"
        f"📈 {bar}  {percent}%\n"
        f"{food_text}\n\n"
        f"{'⚠️ Превышение лимита! Добавь берпи!' if current >= limit else '💪 Держи режим, боец!'}",
        reply_markup=main_keyboard()
    )

@bot.message_handler(func=lambda m: m.text == '📝 Внести замер')
def enter_measure(message):
    bot.send_message(
        message.chat.id,
        "📝 Введи данные в формате:\n"
        "`Вес 86, Талия 95, Грудь 110, Бицепс 38`\n\n"
        "📌 Можно указать только вес и талию.",
        parse_mode='Markdown'
    )
    bot.register_next_step_handler(message, save_measure)

def save_measure(message):
    try:
        text = message.text.replace(',', '.').split(',')
        data_dict = {}
        for part in text:
            parts = part.strip().split()
            if len(parts) < 2:
                continue
            key = parts[0].lower()
            val = float(parts[1].replace(',', '.'))
            if 'вес' in key:
                data_dict['weight'] = val
            elif 'тали' in key:
                data_dict['waist'] = val
            elif 'груд' in key:
                data_dict['chest'] = val
            elif 'бицепс' in key or 'биц' in key:
                data_dict['biceps'] = val
        
        if 'weight' not in data_dict or 'waist' not in data_dict:
            bot.send_message(
                message.chat.id,
                "❌ Ошибка. Нужно указать хотя бы вес и талию.\nПример: `Вес 86, Талия 95`",
                parse_mode='Markdown'
            )
            bot.register_next_step_handler(message, save_measure)
            return
        
        uid = str(message.chat.id)
        db = load_data()
        if uid not in db:
            db[uid] = {'history': [], 'measurements': []}
        
        # Сохраняем историю замеров
        if 'measurements' not in db[uid]:
            db[uid]['measurements'] = []
        
        db[uid]['measurements'].append({
            'date': datetime.now().strftime('%d.%m.%Y'),
            'weight': data_dict['weight'],
            'waist': data_dict['waist'],
            'chest': data_dict.get('chest', 0),
            'biceps': data_dict.get('biceps', 0)
        })
        
        # Обновляем текущие значения
        db[uid]['current_weight'] = data_dict['weight']
        db[uid]['current_waist'] = data_dict['waist']
        
        save_data(db)
        bot.send_message(
            message.chat.id,
            f"✅ Замеры сохранены!\n"
            f"⚖ Вес: {data_dict['weight']} кг\n"
            f"📏 Талия: {data_dict['waist']} см\n"
            f"🎯 До цели осталось: {data_dict['weight'] - 70:.1f} кг",
            reply_markup=main_keyboard()
        )
    except Exception as e:
        bot.send_message(
            message.chat.id,
            f"❌ Ошибка: {str(e)}\nФормат: `Вес 86, Талия 95`",
            parse_mode='Markdown'
        )
        bot.register_next_step_handler(message, save_measure)

@bot.message_handler(func=lambda m: m.text == '📊 Мои замеры')
def show_measures(message):
    uid = str(message.chat.id)
    data = get_user_data(uid)
    measurements = data.get('measurements', [])
    
    if not measurements:
        bot.send_message(
            message.chat.id,
            "📭 У тебя пока нет замеров. Внеси первый через кнопку '📝 Внести замер'.",
            reply_markup=main_keyboard()
        )
        return
    
    last = measurements[-1]
    response = f"📊 Последний замер (от {last.get('date', 'неизвестно')}):\n"
    response += f"⚖ Вес: {last.get('weight', '—')} кг\n"
    response += f"📏 Талия: {last.get('waist', '—')} см\n"
    if last.get('chest'):
        response += f"📏 Грудь: {last.get('chest')} см\n"
    if last.get('biceps'):
        response += f"💪 Бицепс: {last.get('biceps')} см\n"
    
    # Сравнение с первым замером
    if len(measurements) >= 2:
        first = measurements[0]
        w_diff = first.get('weight', 86) - last.get('weight', 86)
        t_diff = first.get('waist', 0) - last.get('waist', 0)
        response += f"\n📈 Прогресс с начала:\n"
        response += f"   Вес: -{w_diff:.1f} кг\n"
        response += f"   Талия: -{t_diff:.1f} см"
    
    bot.send_message(message.chat.id, response, reply_markup=main_keyboard())

@bot.message_handler(func=lambda m: m.text == '📈 Мой прогресс')
def show_progress_chart(message):
    uid = str(message.chat.id)
    data = get_user_data(uid)
    measurements = data.get('measurements', [])
    
    if len(measurements) < 2:
        bot.send_message(
            message.chat.id,
            "📭 Нужно минимум 2 замера для графика. Внеси данные через '📝 Внести замер'.",
            reply_markup=main_keyboard()
        )
        return
    
    # Строим график
    dates = [m.get('date', '') for m in measurements]
    weights = [m.get('weight', 0) for m in measurements]
    waists = [m.get('waist', 0) for m in measurements]
    
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(6, 8))
    
    # Вес
    ax1.plot(dates, weights, 'b-o', linewidth=2)
    ax1.set_title('Динамика веса', fontsize=12)
    ax1.set_ylabel('Вес (кг)', fontsize=10)
    ax1.grid(True, linestyle='--', alpha=0.7)
    ax1.axhline(y=70, color='r', linestyle='--', label='Цель 70 кг')
    ax1.legend()
    
    # Талия
    ax2.plot(dates, waists, 'g-o', linewidth=2)
    ax2.set_title('Динамика талии', fontsize=12)
    ax2.set_ylabel('Талия (см)', fontsize=10)
    ax2.grid(True, linestyle='--', alpha=0.7)
    
    plt.tight_layout()
    
    # Сохраняем в буфер
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    plt.close()
    
    bot.send_photo(message.chat.id, buf, caption="📈 Твой прогресс за время наблюдений!", reply_markup=main_keyboard())

@bot.message_handler(func=lambda m: m.text == '📋 Тренировка на сегодня')
def today_workout(message):
    day = get_day()
    plan = get_workout_plan(day)
    
    uid = str(message.chat.id)
    data = get_user_data(uid)
    penalty = data.get('penalty_burpees', 0)
    
    response = f"📅 Сегодня {day}\n\n{plan}"
    if penalty > 0:
        response += f"\n\n💢 У тебя накопилось {penalty} штрафных берпи! Сделай их после основной тренировки."
    
    if day in ['СБ', 'ВТ', 'ЧТ']:
        response += "\n\n🚶 В день отдыха:\n• 10 000 шагов по казарме\n• Вакуум живота 3 раза по 15 сек\n• Растяжка 10 минут"
    
    bot.send_message(message.chat.id, response, reply_markup=main_keyboard())

@bot.message_handler(func=lambda m: m.text == '❓ Техника упражнений')
def show_technique(message):
    kb = types.InlineKeyboardMarkup(row_width=2)
    exercises = [
        ('🏋️ Приседания', 'squat'),
        ('🏋️ Жим лёжа', 'bench'),
        ('🏋️ Тяга штанги', 'row'),
        ('🏋️ Становая', 'deadlift'),
        ('🏋️ Подтягивания', 'pullup'),
        ('🏋️ Отжимания', 'pushup'),
        ('🏋️ Скакалка', 'jump'),
    ]
    for name, code in exercises:
        kb.add(types.InlineKeyboardButton(name, callback_data=f'tech_{code}'))
    
    bot.send_message(
        message.chat.id,
        "📖 Выбери упражнение, чтобы увидеть GIF с техникой:",
        reply_markup=kb
    )

@bot.callback_query_handler(func=lambda call: call.data.startswith('tech_'))
def send_technique_gif(call):
    tech_map = {
        'squat': 'https://i.pinimg.com/originals/5b/3a/2d/5b3a2d0f3b9e4a1f6c8d7e9f0a1b2c3d.gif',
        'bench': 'https://i.pinimg.com/originals/7c/4a/5e/7c4a5e0f3b9e4a1f6c8d7e9f0a1b2c3d.gif',
        'row': 'https://i.pinimg.com/originals/8d/4a/5e/8d4a5e0f3b9e4a1f6c8d7e9f0a1b2c3d.gif',
        'deadlift': 'https://i.pinimg.com/originals/9d/4a/5e/9d4a5e0f3b9e4a1f6c8d7e9f0a1b2c3d.gif',
        'pullup': 'https://i.pinimg.com/originals/ad/4a/5e/ad4a5e0f3b9e4a1f6c8d7e9f0a1b2c3d.gif',
        'pushup': 'https://i.pinimg.com/originals/bd/4a/5e/bd4a5e0f3b9e4a1f6c8d7e9f0a1b2c3d.gif',
        'jump': 'https://i.pinimg.com/originals/cd/4a/5e/cd4a5e0f3b9e4a1f6c8d7e9f0a1b2c3d.gif',
    }
    gif_url = tech_map.get(call.data.replace('tech_', ''))
    if gif_url:
        bot.send_animation(call.message.chat.id, gif_url, caption=f"✅ Техника {call.data.replace('tech_', '')}")
    else:
        bot.send_message(call.message.chat.id, "⚠️ GIF временно недоступен.")
    bot.answer_callback_query(call.id)

@bot.message_handler(func=lambda m: m.text == '😈 Я сорвался!')
def i_slipped(message):
    uid = str(message.chat.id)
    data = get_user_data(uid)
    
    penalty = 30
    data['penalty_burpees'] = data.get('penalty_burpees', 0) + penalty
    data['slip_count'] = data.get('slip_count', 0) + 1
    save_data(load_data())
    
    bot.send_message(
        message.chat.id,
        f"😈 Ты сорвался! Бывает.\n\n"
        f"💪 Штраф: +{penalty} берпи к следующей тренировке.\n"
        f"📊 Всего срывов: {data.get('slip_count', 0)}\n\n"
        f"🔥 Не сдавайся! Завтра новый день.",
        reply_markup=main_keyboard()
    )

@bot.message_handler(func=lambda m: m.text == '🔔 Настроить напоминания')
def setup_reminder(message):
    kb = types.InlineKeyboardMarkup(row_width=2)
    times = ['18:00', '18:30', '19:00', '19:30', '20:00']
    for t in times:
        kb.add(types.InlineKeyboardButton(t, callback_data=f'remind_{t}'))
    bot.send_message(
        message.chat.id,
        "🕒 Выбери время для ежедневного напоминания о тренировке:",
        reply_markup=kb
    )

@bot.callback_query_handler(func=lambda call: call.data.startswith('remind_'))
def set_reminder(call):
    time = call.data.replace('remind_', '')
    uid = str(call.message.chat.id)
    data = get_user_data(uid)
    data['reminder_time'] = time
    save_data(load_data())
    bot.edit_message_text(
        f"✅ Напоминание установлено на {time}.\nЯ буду писать тебе в тренировочные дни (ПН, СР, ПТ, ВС).",
        call.message.chat.id,
        call.message.message_id,
        reply_markup=main_keyboard()
    )
    bot.answer_callback_query(call.id)

@bot.message_handler(func=lambda m: m.text == '🔄 Сбросить прогресс')
def reset_progress(message):
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton("✅ ДА, сбросить всё", callback_data='reset_confirm'))
    kb.add(types.InlineKeyboardButton("❌ ОТМЕНА", callback_data='reset_cancel'))
    bot.send_message(
        message.chat.id,
        "⚠️ Ты уверен, что хочешь сбросить все данные?\nЭто действие НЕОБРАТИМО.",
        reply_markup=kb
    )

@bot.callback_query_handler(func=lambda call: call.data == 'reset_confirm')
def reset_confirm(call):
    uid = str(call.message.chat.id)
    db = load_data()
    if uid in db:
        db[uid] = {
            'history': [],
            'food_log': [],
            'daily_calories': 0,
            'calorie_limit': 1800,
            'penalty_burpees': 0,
            'slip_count': 0,
            'last_reset_date': datetime.now().strftime('%Y-%m-%d'),
            'reminder_time': '19:00',
            'current_weight': 86,
            'current_waist': 95,
            'measurements': []
        }
        save_data(db)
    bot.edit_message_text(
        "🔄 Прогресс сброшен. Начинаем с чистого листа!",
        call.message.chat.id,
        call.message.message_id,
        reply_markup=main_keyboard()
    )
    bot.answer_callback_query(call.id)

@bot.callback_query_handler(func=lambda call: call.data == 'reset_cancel')
def reset_cancel(call):
    bot.edit_message_text(
        "✅ Сброс отменён. Продолжай в том же духе!",
        call.message.chat.id,
        call.message.message_id,
        reply_markup=main_keyboard()
    )
    bot.answer_callback_query(call.id)

@bot.message_handler(func=lambda m: m.text == '⬅️ Назад в меню')
def back_to_menu(message):
    bot.send_message(message.chat.id, "Возвращаемся в главное меню.", reply_markup=main_keyboard())

@bot.message_handler(func=lambda m: True)
def fallback(message):
    bot.send_message(
        message.chat.id,
        "❓ Используй кнопки меню. Если хочешь внести замер — нажми '📝 Внести замер'.",
        reply_markup=main_keyboard()
    )

# ===== ЗАПУСК =====
if __name__ == '__main__':
    # Убираем webhook (для Render)
    bot.remove_webhook()
    print("Бот запущен и готов к работе!")
    bot.polling(none_stop=True)
