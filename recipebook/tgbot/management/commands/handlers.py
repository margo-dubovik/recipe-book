import telebot
from django.shortcuts import get_object_or_404
from users.models import BotUser
# from bot import bot

# from django.apps import apps
# BotUser = apps.get_model('users', 'BotUser')


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
    user.update(state=state)


# Handle '/start' and '/help'
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, """\
    Hi there, I am RecipeBot. Enter your name, please.
    """)
    new_user = BotUser(
        tg_id=message.from_user.id,
        username=message.from_user.username,
        first_name=message.from_user.first_name,
        last_name=message.from_user.last_name,
        state=states["WAIT_FOR_NAME"],
    )
    new_user.save()


# Handle all other messages with content_type 'text' (content_types defaults to ['text'])
@bot.message_handler(func=lambda message: get_current_state(message.from_user.id) == states["WAIT_FOR_NAME"])
def user_enters_name(message):
    global inserted_info
    inserted_info['name'] = message.text
    bot.send_message(message.chat.id, "Nice to meet you! And what is your gender?")
    set_state(message.from_user.id, states['WAIT_FOR_GENDER'])


