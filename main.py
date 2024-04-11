import os

import telebot
from dotenv import load_dotenv
from telebot import types

# Load env
load_dotenv()

# Demo token, it will be removed soon
TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]

# Bot connection
bot = telebot.TeleBot(TOKEN)

WELCOME_MESSAGE = "Welcome to seb_tfa_bot, now you can start using our tools"
HELP_MESSAGE = """Sure, you there are a few commands that you can use: 
/start
/download {video url}
/horoscope
"""

MENU_OPTIONS = {
    "DOWNLOAD": "menu_download",
    "HOROSCOPE": "menu_horoscope",
}


@bot.message_handler(commands=['commands-info'])
def send_menu(message):
    markup = types.InlineKeyboardMarkup(row_width=2)

    button_download = types.InlineKeyboardButton("Download video", callback_data=MENU_OPTIONS["DOWNLOAD"])
    button_horoscope = types.InlineKeyboardButton("Get horoscope", callback_data=MENU_OPTIONS["HOROSCOPE"])

    markup.add(button_download, button_horoscope)

    bot.send_message(message.chat.id, "What do you want to do?", reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == MENU_OPTIONS["HOROSCOPE"]:
        return bot.answer_callback_query(call.id, "You can see horoscope using /horoscope {your sign}!")
    if call.data == MENU_OPTIONS["DOWNLOAD"]:
        return bot.answer_callback_query(call.id, "For download you need to put /download {url}")
    return bot.answer_callback_query(call.id, "Ops, something went wrong :/")


# Setting commands actions (start, help, download)
@bot.message_handler(commands=['start'])
def send_getting(message):
    bot.reply_to(message, WELCOME_MESSAGE)


@bot.message_handler(commands=['help'])
def send_help(message):
    bot.reply_to(message, HELP_MESSAGE)


@bot.message_handler(commands=['random-img'])
def send_random_img(message):
    img_url = "https://source.unsplash.com/random"
    bot.send_photo(chat_id=message.chat.id, photo=img_url, caption="Getting random image")


@bot.message_handler(func=lambda m: True)
def echo_all(message):
    bot.reply_to(message, message.text)


if __name__ == "__main__":
    bot.polling(none_stop=True)
