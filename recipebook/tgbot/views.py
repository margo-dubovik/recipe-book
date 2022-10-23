import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from telebot import types
from tgbot.management.commands.bot import bot


@csrf_exempt
def webhook(request):
    # print(request.body.decode('utf-8'))
    update = types.Update.de_json(json.loads(request.body.decode('utf-8')))
    bot.process_new_updates([update])
    return JsonResponse({'message': 'OK'}, status=200)
