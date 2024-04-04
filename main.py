import telebot

TOKEN = "6754622015:AAGZjePDFaa0sAzRJqs0kftsh14G_8uLMOg"

# Bot connection
bot = telebot.TeleBot(TOKEN)

WELCOME_MESSAGE = "Welcome to seb_tfa_bot, now you can start using our tools"
HELP_MESSAGE = """Sure, you there are a few commands that you can use: 
/start
/download {video url}
/horoscope
"""


# Setting commands actions (start, help, download)
@bot.message_handler(commands=['start'])
def send_getting(message):
    bot.reply_to(message, WELCOME_MESSAGE)


@bot.message_handler(commands=['help'])
def send_help(message):
    bot.reply_to(message, HELP_MESSAGE)


@bot.message_handler(func=lambda m: True)
def echo_all(message):
    bot.reply_to(message, message.text)


if __name__ == "__main__":
    bot.polling(none_stop=True)