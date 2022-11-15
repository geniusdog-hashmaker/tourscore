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
    random_attract = telebot.types.KeyboardButton('random')
    score = telebot.types.KeyboardButton('score')
    markup.add(random_attract, score)
    mess = 'Отлично!\nЕсли хочешь, чтобы я выдал тебе случайную достопримечатльность, ' \
           'нажми на кнопку "random", а если захочешь оценить её - "score".\n' \
           'Быть может, ты ищешь что-то конкретное. В таком случае просто напиши мне название.'

    bot.send_message(message.chat.id, mess, reply_markup=markup)


@bot.message_handler()
def get_user_text(message):

    with open('data.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
    attraction = message.text.lower()

    if message.text == 'random':
        rand_attract = choice(list(data))
        attraction = str(rand_attract)

    elif message.text == 'score':
        mess = 'Напиши свою оценку - целое число от 0 до 10.'
        bot.send_message(message.chat.id, mess, parse_mode='')


        def get_user_score(user_score):
            score = data[attraction][0]["score"]
            people_scored = data[attraction][0]["people_scored"]
            ids = data[attraction][0]["ids"]
            print('it works')

    if attraction in data.keys():
        photo = open(f'{data[attraction][0]["photo_name"]}', 'rb')
        name = data[attraction][0]["name"]
        description = data[attraction][0]["description"]
        score = data[attraction][0]["score"]
        bot.send_photo(message.chat.id, photo, caption=f'{name} — {score}/10\n\n{description}')


bot.polling(none_stop=True)
