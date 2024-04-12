import os
from shutil import rmtree

import requests
import telebot
from dotenv import load_dotenv
from telebot import types

from youtube import VideoDownloader

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

DEFAULT_FORMAT = 1


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


#         Video Downloader
@bot.message_handler(commands=['download'])
def download_video(message):
    # Getting url from user msg
    user_input = message.text.split()

    if len(user_input) < 2:
        return bot.send_message(message.chat.id, "Remind, you need to put your url after command /download")

    video_url = user_input[1]
    video = VideoDownloader()

    try:
        video.set_video(video_url)
    except NameError:
        return bot.send_message(message.chat.id, "We had a problem getting your video")
    else:
        video.set_format(DEFAULT_FORMAT)
        video.download_video()
        info = video.get_video_info()
        bot.reply_to(message, f"Downloading video: {info["title"]}")

        def send_message():
            videos = os.listdir('./downloads')
            user_video = videos[0]
            response = requests.get(info["thumbnail_url"])

            try:
                bot.send_video(message.chat.id, open(f"./downloads/{user_video}", "rb"),
                               thumbnail=response.content,
                               caption=info["title"], width=1280, height=720)
                rmtree('./downloads')
            except NameError:
                bot.send_message(message.chat.id, "ups, maybe your file is too large")
                rmtree('./downloads')

        video.current_format.on_complete(send_message())


@bot.message_handler(func=lambda m: True)
def echo_all(message):
    bot.reply_to(message, message.text)


if __name__ == "__main__":
    bot.polling(none_stop=True)
