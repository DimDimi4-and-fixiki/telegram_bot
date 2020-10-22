from my_tele_bot import MyTeleBot
import threading
from news_sender import NewsSender
from flask import Flask, request
from post_requests import PostRequestMaker
import os
import telebot


"""
Put bot and news sender in separate threads using 'threading'
create class for News Sender
"""

news_sender = NewsSender()  # NewsSender object
server = Flask(__name__)
bot = MyTeleBot(token_path="secure_codes/token.txt")
TOKEN = bot.bot.token
HEROKU_APP_URL = "https://evening-mountain-99390.herokuapp.com/"
print("TOKEN", TOKEN)
# Heroku server connection

@server.route('/' + TOKEN, methods=['POST'])
def getMessage():
    bot.bot.process_new_updates([telebot.types.Update.de_json(
        request.stream.read().decode("utf-8")
    )])
    return "!", 200

@server.route("/")
def webhook():
    bot.bot.remove_webhook()
    bot.bot.set_webhook(url=HEROKU_APP_URL + TOKEN)
    return "!", 200


def send_news():
    """
    Starts polling news to the users
    """
    news_sender.send_news()


def send_post_requests():
    """
    Sends POST requests in time to awake the app
    """
    post_request_maker = PostRequestMaker(url=HEROKU_APP_URL + TOKEN,
                                          interval=300)


def bot_polling():
    #  configuring news_sender:
    news_sender.data_base_handler = bot.data_base_handler
    news_sender.news_api_handler = bot.news_api_handler
    news_sender.language_handler = bot.language_handler
    news_sender.bot = bot.bot
    server.run(host="0.0.0.0",
               port=int(os.environ.get('PORT', 47895)))


def main():
    thread1 = threading.Thread(target=bot_polling)
    thread2 = threading.Thread(target=send_news)
    thread3 = threading.Thread(target=send_post_requests)
    thread1.start()
    thread2.start()
    thread3.start()


if __name__ == "__main__":
    main()
