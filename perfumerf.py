import json
import telebot
import random
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

BOT_TOKEN = "7853990561:AAFKmJMQzNc9BlEKPKThJ1HRr3QSFpi6DYE"
bot = telebot.TeleBot(BOT_TOKEN)

with open('perfumer.json', "r", encoding="utf-8") as f:
    perfumes = json.load(f)

user_states = {}
user_answers = {}


questions = [
    {"text": "Хотите ли вы цитрусовые духи?", "key": "Цитрус", 'img': 'https://media.istockphoto.com/id/1044366990/ru/%D1%84%D0%BE%D1%82%D0%BE/%D1%86%D0%B8%D1%82%D1%80%D1%83%D1%81%D0%BE%D0%B2%D1%8B%D0%B5.jpg?s=612x612&w=0&k=20&c=PH--cEuYDAYqpvuLLf9GjOGwhjp5RTFOnVCbEPkewCA='},
    {"text": "Хотите ли вы свежие пряные духи?", "key": "Свежие пряные", 'img': 'https://lookbio.ru/wp-content/uploads/2015/09/Fresh-Herbs-and-spices.jpg'},
    {"text": "Хотите ли вы тёплые пряные духи?", "key": "Тёплые пряные", 'img': 'https://svoe-rodnoe.ru/blog/wp-content/uploads/2023/08/9969102f-db54-4f05-a0f0-a4fcec15ee01-1-e1691671754598.jpg'},
    {"text": "Хотите ли вы сладкие духи?", "key": "Сладкие", 'img': 'https://trikky.ru/wp-content/blogs.dir/1/files/2019/04/18/yarkie_sladosti.jpg'},
    {"text": "Хотите ли вы свежие духи?", "key": "Свежие", 'img': 'https://cameralabs.org/media/k2/items/cache/afeb3017892d3f743f6abee16b8db8d0_L.jpg'},
    {"text": "Хотите ли вы древесные духи?", "key": "Древесные", 'img': 'https://www.aroma-butik.ru/images/categories/articles/title_image_101.jpg'},
    {"text": "Хотите ли вы ванильные духи?", "key": "Ваниль", 'img': 'https://aromacode.ru/wa-data/public/blog/img/vanilnye-duhi1.jpg'},
    {"text": "Хотите ли вы кокосовые духи?", "key": "Кокос", 'img': 'https://aromacod.ru/wa-data/public/blog/images/1224/1584485813_731525.jpeg'},
    {"text": "Хотите ли вы зеленые духи?", "key": "Зеленые", 'img': 'https://i.pinimg.com/originals/c7/32/96/c7329618b0456cde86331667d82d2555.jpg'},
    {"text": "Хотите ли вы фужерные духи?", "key": "Фужерные", 'img': 'https://cdn.aromo.ru/upload/users_accounts_articles_pictures/777/hjqkmaot2fdvq0aphcnvmw85pvvgrsba/herbs-orig.jpeg'},
    {"text": "Хотите ли вы духи c тропическим запахом?", "key": "Тропик", 'img': 'https://get.wallhere.com/photo/great-green-jungle-1748991.jpg'},
    {"text": "Хотите ли вы духи c лавандовым запахом?", "key": "Лаванда", 'img': 'https://kamenca.ru/upload/iblock/bdc/bdc9b89bbe985fc28412b88f944663d2.jpg'},
    {"text": "Хотите ли вы фруктовые духи?", "key": "Фруктовые", 'img': 'https://fkniga.ru/media/product/02/020803/KA-00031858.jpg'}
]

def set_user_state(user_id, state):
    user_states[user_id] = state

def get_user_state(user_id):
    return user_states.get(user_id, None)

def save_user_answer(user_id, key, answer):
    if user_id not in user_answers:
        user_answers[user_id] = {}
    user_answers[user_id][key] = answer

@bot.message_handler(commands=["start"])
def start_command(message):
    user_id = message.chat.id
    bot.send_message(user_id, "Привет! Я помогу вам подобрать духи. Напишите /choice, чтобы начать выбор.")
    set_user_state(user_id, None)

@bot.message_handler(commands=["choice"])
def start_choice(message):
    user_id = message.chat.id
    set_user_state(user_id, "asking_questions")
    user_answers[user_id] = {}
    ask_next_question(user_id, 0)

def ask_next_question(user_id, question_index):
    if question_index < len(questions):
        question = questions[question_index]
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        keyboard.add(KeyboardButton("Да"), KeyboardButton("Нет"))
        bot.send_photo(user_id, question['img'], caption=question["text"], reply_markup=keyboard)
        set_user_state(user_id, f"question_{question_index}")
    else:
        find_matching_perfumes(user_id)

@bot.message_handler(func=lambda message: get_user_state(message.chat.id) and get_user_state(message.chat.id).startswith("question_"))
def handle_answer(message):
    user_id = message.chat.id
    state = get_user_state(user_id)
    question_index = int(state.split("_")[1])
    answer = message.text.lower() == "да"
    key = questions[question_index]["key"]
    save_user_answer(user_id, key, answer)
    ask_next_question(user_id, question_index + 1)

def find_matching_perfumes(user_id):
    max_matches = 0
    matching_perfumesf = []
    user_preferences = user_answers.get(user_id, {})
    matching_perfumes = []

    for perfume in perfumes:
        matches = 0
        for key, user_wants in user_preferences.items():
            if user_wants and key in perfume.get("notes", []):
                matches += 1
        if matches > 0:
            matching_perfumes.append((perfume, matches))
            if matches > max_matches:
                max_matches = matches
    matching_perfumes.sort(key=lambda x: x[1], reverse=True)
    for k in matching_perfumes:
        if int(k[1]) >= max_matches or (int(k[1]) + 1) >= max_matches:
            if k[1] != 0:
                matching_perfumesf.append(k)
    matching_perfumesf.sort(key=lambda x: x[1], reverse=True)

    if len(matching_perfumesf) >= 3:
        matching_perfumesff = random.sample(matching_perfumesf, 3)
    else:
        matching_perfumesff = random.sample(matching_perfumesf, len(matching_perfumesf))

    if matching_perfumesff:
        bot.send_message(user_id, "Вот лучшие варианты для вас:")
        for perfume, _ in matching_perfumesff:
            text = (
                f"Название: {perfume['name']}\n"
                f"Описание: {perfume['description']}\n"
                f"Сезон: {perfume['season']}\n"
                f"Ссылка на покупку: {perfume['link']}"
            )
            if "image_url" in perfume:
                bot.send_photo(user_id, photo=perfume["image_url"], caption=text)
            else:
                bot.send_message(user_id, text)
    else:
        bot.send_message(user_id, "Извините, но по вашему запросу ничего не найдено.")

    set_user_state(user_id, None)


bot.infinity_polling()
