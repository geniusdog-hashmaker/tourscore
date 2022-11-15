import json
from random import choice
import telebot


bot = telebot.TeleBot('5729238552:AAFOynh7kqMijoB5pEmOMudCJjvOMtcDz_Q')


@bot.message_handler(commands=['start'])
def start(message):

    mess1 = f'Привет, {message.from_user.first_name}! Я покажу тебе достопримечательности ' \
           f'Калининграда и расскажу о них что-нибудь интересное, а рейтинг пользователей ' \
           f'позволит тебе выбрать, куда отправиться сегодня же.'
    bot.send_message(message.chat.id, mess1, parse_mode='')
    mess2 = 'Напиши в чат "/help", и я объясню тебе, как я работаю'
    bot.send_message(message.chat.id, mess2, parse_mode='')


@bot.message_handler(commands=['help'])
def help(message):

    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    random_attract = telebot.types.KeyboardButton('случайно')
    score = telebot.types.KeyboardButton('оценить')
    markup.add(random_attract, score)
    mess = 'Отлично!\nЕсли хочешь, чтобы я выдал тебе случайную достопримечатльность, ' \
           'нажми на кнопку "случайно", а если захочешь оценить последнюю из просмотренных -' \
           ' "оценить".\nБыть может, ты ищешь что-то конкретное.' \
           ' В таком случае просто напиши мне название.'

    bot.send_message(message.chat.id, mess, reply_markup=markup)


@bot.message_handler()
def get_user_text(message):
    with open('data.json', 'r', encoding='utf-8') as file:
        data = json.load(file)

    if message.text == 'случайно':
        randomizer(message)
    elif message.text == 'оценить':
        attraction_for_scoring = name.lower()
        mess = bot.send_message(message.chat.id, 'Напиши свою оценку - целое число от 0 до 10.',
                                parse_mode='')
        bot.register_next_step_handler(mess, get_user_score, attraction_for_scoring)
    elif message.text.lower() in data.keys():
        users_attraction(message)


def randomizer(message):
    global name

    with open('data.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
    rand_attraction = choice(list(data))
    photo = open(f'{data[rand_attraction][0]["photo_name"]}', 'rb')
    name = data[rand_attraction][0]["name"]
    description = data[rand_attraction][0]["description"]
    score = data[rand_attraction][0]["score"]
    bot.send_photo(message.chat.id, photo, caption=f'{name} — {score}/10\n\n{description}')


def get_user_score(message, attraction_for_scoring):
    with open('data.json', 'r', encoding='utf-8') as file:
        data = json.load(file)

    user_score = message.text
    if not user_score.isdigit():
        mess = bot.send_message(message.chat.id, 'Оценка должна быть числом от 0 до 10.', parse_mode='')
        bot.register_next_step_handler(mess, get_user_score)
    user_score = int(user_score)
    user_id = message.from_user.id
    actual_score = data[attraction_for_scoring][0]["score"]
    ids_of_people_scored = data[attraction_for_scoring][0]["ids"]
    if user_id not in ids_of_people_scored:
        ids_of_people_scored[user_id] = user_score
    count_of_people_scored = len(ids_of_people_scored)

    # проблема где-то в этом блоке
    updated_score = round((actual_score + user_score) / count_of_people_scored, 1)
    data[attraction_for_scoring][0]["score"] = updated_score
    print(data[attraction_for_scoring])

    with open('data.json', 'r', encoding='utf-8') as file:
        data[attraction_for_scoring][0]["score"] = updated_score
        json.dumps(data)

    bot.send_message(message.chat.id, 'Спасибо за оценку!')


def users_attraction(message):
    global name

    with open('data.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
    attraction = message.text.lower()
    photo = open(f'{data[attraction][0]["photo_name"]}', 'rb')
    name = data[attraction][0]["name"]
    description = data[attraction][0]["description"]
    score = data[attraction][0]["score"]
    bot.send_photo(message.chat.id, photo, caption=f'{name} — {score}/10\n\n{description}')


bot.polling(none_stop=True)
