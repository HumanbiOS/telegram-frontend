from threading import Thread
import tornado.ioloop
import tornado.web
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Bot, KeyboardButton, ReplyKeyboardMarkup, \
    ReplyKeyboardRemove
from tornado.escape import json_decode
from tornado.web import url, RequestHandler
from telegram.utils.webhookhandler import WebhookServer

from utils import build_menu

cache = {"file_ids": {}}


class MainHandler(RequestHandler):

    def initialize(self, bot: Bot):
        self.bot = bot

    def prepare(self):
        self.args = json_decode(self.request.body)

    def post(self):
        print(self.args)
        chat_id = self.args["chat"]["chat_id"]
        if chat_id not in cache:
            cache[chat_id] = {"buttons": False}
        text = False
        if "message" in self.args and not self.args["file"]:
            text = self.args["message"]["text"]
        file_urls = []
        if "file" in self.args:
            caption = False
            if "message" in self.args:
                caption = self.args["message"]["text"]
            for file_url in file_urls:
                file_urls.append(url["payload"])
        if self.args["buttons"]:
            if self.args["buttons_type"] == "inline":
                buttons = []
                for button in self.args["buttons"]:
                    buttons.append(InlineKeyboardButton(text=button["text"], callback_data=button["value"]))
                menu = InlineKeyboardMarkup(build_menu(buttons, 4))
            else:
                cache[chat_id]["buttons"] = True
                buttons = []
                for button in self.args["buttons"]:
                    buttons.append(KeyboardButton(text=button["text"]))
                menu = ReplyKeyboardMarkup(build_menu(buttons, 2), resize_keyboard=True)
        else:
            menu = False
        if text:
            if menu:
                self.bot.send_message(chat_id=chat_id, text=text, reply_markup=menu)
            else:
                if cache[chat_id]["buttons"]:
                    self.bot.send_message(chat_id=chat_id, text=text, reply_markup=ReplyKeyboardRemove())
                else:
                    self.bot.send_message(chat_id=chat_id, text=text)
        if file_urls:
            for f_url in file_urls:
                if f_url in cache["file_ids"]:
                    self.bot.send_photo(chat_id, cache["file_ids"][f_url], caption)
                else:
                    message = self.bot.send_photo(chat_id, f_url, caption)
                    cache["file_ids"][f_url] = message.photo[-1].file_id
        self.set_header('content-type', 'application/json')


def make_app(bot):
    return tornado.web.Application([
        url(r"/", MainHandler, dict(bot=bot)),
    ])


class OwnWebhook(Thread):

    def __init__(self, bot):
        super().__init__()
        app = make_app(bot)
        # TODO enter setting
        self.webhooks = WebhookServer("0.0.0.0", 8888, app, None)

    def run(self) -> None:
        self.webhooks.serve_forever()

    def shutdown(self):
        self.webhooks.shutdown()
