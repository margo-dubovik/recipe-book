from django.core.management.base import BaseCommand
from telebot import TeleBot, types
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import os
from dotenv import load_dotenv

load_dotenv()

from django.shortcuts import get_object_or_404
from users.models import BotUser

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


# Handle '/start' and '/help'
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, """\
    Вітаю! Я -- Книжка рецептів. Давайте познайомимось.
    Введіть, будь ласка, своє ім'я.
    """)
    if not BotUser.objects.filter(tg_id=message.from_user.id).exists():
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
            bot.send_message(message.chat.id, f"Вітаю, {user.chosen_name}. Головне меню")
        elif user.state == states['RECIPES_MENU']:
            bot.send_message(message.chat.id, f"Вітаю, {user.chosen_name}. Меню рецептів")
        elif user.state == states['WAIT_FOR_GENDER']:
            bot.send_message(message.chat.id,
                             text=f"Приємно познайомитись, {message.text}! Будь ласка, оберіть свою стать:",
                             reply_markup=gender_markup())
        elif user.state == states['WAIT_FOR_NAME']:
            bot.send_message(message.chat.id, f"Вітаю! Введіть, будь ласка, своє ім'я.")



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


# Handle user inserting their name
@bot.message_handler(func=lambda message: get_current_state(message.from_user.id) == states["WAIT_FOR_NAME"])
def user_enters_name(message):
    user_id = message.from_user.id
    user = get_object_or_404(BotUser, tg_id=user_id)
    user.name = message.text
    user.save()

    bot.send_message(message.chat.id, text=f"Приємно познайомитись, {message.text}! Будь ласка, оберіть свою стать:",
                     reply_markup=gender_markup())
    set_state(user_id, states['WAIT_FOR_GENDER'])


# Handle user inserting gender
@bot.callback_query_handler(func=lambda call: call.data in ['m', 'f', 'o'])
def callback_query(call):
    user_id = call.message.chat.id
    user = get_object_or_404(BotUser, tg_id=user_id)
    user.gender = call.data
    user.save()
    bot.send_message(chat_id=call.message.chat.id, text='Дякую!')
    bot.send_message(chat_id=call.message.chat.id, text=f"Головне меню:",
                     reply_markup=main_menu_markup())
    set_state(user_id, states['MAIN_MENU'])


class Command(BaseCommand):
    help = 'Recipe Bot'

    def handle(self, *args, **kwargs):
        bot.infinity_polling()
