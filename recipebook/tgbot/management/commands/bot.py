from django.core.management.base import BaseCommand
from telebot import TeleBot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from django.shortcuts import get_object_or_404
from tgbot.models import BotUser, Recipe

from urllib.request import urlopen
from io import BytesIO

import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.environ.get('TELEGRAM_API_TOKEN')
bot = TeleBot(TOKEN)

states = {
    "WAIT_FOR_NAME": 0,
    "WAIT_FOR_GENDER": 1,
    "MAIN_MENU": 2,
    "RECIPES_MENU": 3,
}

inserted_info = {}


def get_current_state(user_id):
    user = get_object_or_404(BotUser, tg_id=user_id)
    return user.state


def set_state(user_id, state):
    user = get_object_or_404(BotUser, tg_id=user_id)
    user.state = state
    user.save()


def gender_markup():
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    markup.add(InlineKeyboardButton('Жіноча', callback_data='f'),
               InlineKeyboardButton('Чоловіча', callback_data='m'),
               InlineKeyboardButton('Інша', callback_data='o'),
               )
    return markup


def main_menu_markup():
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    markup.add(InlineKeyboardButton('Про мене', callback_data='about_me'),
               InlineKeyboardButton('Рецепти', callback_data='recipes'),
               )
    return markup


def recipes_markup():
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    recipes = Recipe.objects.all()
    for recipe in recipes:
        markup.add(InlineKeyboardButton(recipe.name, callback_data=f"recipe_{recipe.pk}"))
    return markup


# Handle '/start'
@bot.message_handler(commands=['start'])
def send_welcome(message):
    if not BotUser.objects.filter(tg_id=message.from_user.id).exists():
        bot.reply_to(message, """\
            Вітаю! Я -- Книжка рецептів. Давайте познайомимось.\
            Введіть, будь ласка, своє ім'я.
            """)
        new_user = BotUser(
            tg_id=message.from_user.id,
            username=message.from_user.username,
            first_name=message.from_user.first_name,
            last_name=message.from_user.last_name,
            state=states["WAIT_FOR_NAME"],
        )
        new_user.save()
    else:
        user = BotUser.objects.get(tg_id=message.from_user.id)
        if user.state == states['MAIN_MENU']:
            bot.send_message(message.chat.id, f"Вітаю, {user.chosen_name}. Головне меню",
                             reply_markup=main_menu_markup())
        elif user.state == states['RECIPES_MENU']:
            bot.send_message(message.chat.id, text=f"Вітаю, {user.chosen_name}. Рецепти:",
                             reply_markup=recipes_markup())
        elif user.state == states['WAIT_FOR_GENDER']:
            bot.send_message(message.chat.id,
                             text=f"Приємно познайомитись, {message.text}! Будь ласка, оберіть свою стать:",
                             reply_markup=gender_markup())
        elif user.state == states['WAIT_FOR_NAME']:
            bot.send_message(message.chat.id, f"Вітаю! Введіть, будь ласка, своє ім'я.")


# Handle '/menu'
@bot.message_handler(commands=['menu'])
def send_menu(message):
    user = BotUser.objects.get(tg_id=message.from_user.id)
    if user.state == states['WAIT_FOR_GENDER']:
        bot.send_message(message.chat.id,
                         text=f"Щоб побачити головне меню, оберіть, будь ласка, свою стать:",
                         reply_markup=gender_markup())
    elif user.state == states['WAIT_FOR_NAME']:
        bot.send_message(message.chat.id, f"Щоб побачити головне меню, введіть, будь ласка, своє ім'я.")
    else:
        bot.send_message(message.chat.id, f"Головне меню",
                         reply_markup=main_menu_markup())
        set_state(message.from_user.id, states['MAIN_MENU'])


# Handle '/recipes'
@bot.message_handler(commands=['recipes'])
def send_recipes(message):
    user = BotUser.objects.get(tg_id=message.from_user.id)
    if user.state == states['WAIT_FOR_GENDER']:
        bot.send_message(message.chat.id,
                         text=f"Щоб побачити рецепти, оберіть, будь ласка, свою стать:",
                         reply_markup=gender_markup())
    elif user.state == states['WAIT_FOR_NAME']:
        bot.send_message(message.chat.id, f"Щоб побачити рецепти, введіть, будь ласка, своє ім'я.")
    else:
        bot.send_message(message.chat.id, f"Рецепти:",
                         reply_markup=recipes_markup())
        set_state(message.from_user.id, states['RECIPES_MENU'])


# Handle user inserting their name
@bot.message_handler(func=lambda message: get_current_state(message.from_user.id) == states["WAIT_FOR_NAME"])
def user_enters_name(message):
    user_id = message.from_user.id
    user = get_object_or_404(BotUser, tg_id=user_id)
    user.chosen_name = message.text
    user.save()

    bot.send_message(message.chat.id, text=f"Приємно познайомитись, {message.text}! Будь ласка, оберіть свою стать:",
                     reply_markup=gender_markup())
    set_state(user_id, states['WAIT_FOR_GENDER'])


# Handle user inserting gender
@bot.callback_query_handler(func=lambda call: call.data in ['m', 'f', 'o'])
def gender_callback(call):
    user_id = call.message.chat.id
    user = get_object_or_404(BotUser, tg_id=user_id)
    user.gender = call.data
    user.save()
    bot.send_message(chat_id=call.message.chat.id, text='Дякую!')
    bot.send_message(chat_id=call.message.chat.id, text=f"Головне меню:",
                     reply_markup=main_menu_markup())
    set_state(user_id, states['MAIN_MENU'])


# Handle main menu choice
@bot.callback_query_handler(func=lambda call: call.data in ['about_me', 'recipes'])
def main_menu_callback(call):
    user_id = call.message.chat.id
    user = get_object_or_404(BotUser, tg_id=user_id)
    if call.data == 'about_me':
        bot.send_message(chat_id=call.message.chat.id,
                         text=f"Ім'я: {user.chosen_name},\nСтать: {user.gender_verbose}")
    else:
        bot.send_message(chat_id=call.message.chat.id,
                         text=f"Рецепти:", reply_markup=recipes_markup())
        set_state(user_id, states['RECIPES_MENU'])


# Handle recipe choice
@bot.callback_query_handler(func=lambda call: call.data.startswith('recipe_'))
def recipe_callback(call):
    recipe_pk = call.data[7:]
    recipe = get_object_or_404(Recipe, pk=recipe_pk)
    if recipe.photo:
        host_url = "http://localhost:8000"
        photo_url = host_url + recipe.photo_url
        bot.send_photo(chat_id=call.message.chat.id,
                       photo=BytesIO(urlopen(photo_url).read()))
    bot.send_message(chat_id=call.message.chat.id,
                     text=recipe.text)


class Command(BaseCommand):
    help = 'Recipe Bot'

    def handle(self, *args, **kwargs):
        # bot.infinity_polling()
        bot.set_webhook(url=f"https://recipebook-margodubovik.herokuapp.com/tgbot/telegram-webhook/")
