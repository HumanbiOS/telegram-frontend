from threading import Thread
import tornado.ioloop
import tornado.web
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Bot, KeyboardButton, ReplyKeyboardMarkup
from tornado.escape import json_decode
from tornado.web import url, RequestHandler
from telegram.utils.webhookhandler import WebhookServer

from utils import build_menu


class MainHandler(RequestHandler):

    def initialize(self, bot: Bot):
        self.bot = bot

    def prepare(self):
        self.args = json_decode(self.request.body)

    def post(self):
        print(self.args)
        chat_id = self.args["chat"]["chat_id"]
        if "message" in self.args:
            text = self.args["message"]["text"]
        else:
            text = False
        if "buttons" in self.args:
            if self.args["buttons_type"] == "inline":
                buttons = []
                for button in self.args["buttons"]:
                    buttons.append(InlineKeyboardButton(text=button["text"], callback_data=button["value"]))
                menu = InlineKeyboardMarkup(build_menu(buttons, 4))
            else:
                buttons = []
                for button in self.args["buttons"]:
                    buttons.append(KeyboardButton(text=button["text"]))
                menu = ReplyKeyboardMarkup(build_menu(buttons, 2))
        else:
            menu = False
        if text:
            if menu:
                self.bot.send_message(chat_id=chat_id, text=text, reply_markup=menu)
            else:
                self.bot.send_message(chat_id=chat_id, text=text)
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
        self.webhooks = WebhookServer("127.0.0.1", 8888, app, None)

    def run(self) -> None:
        self.webhooks.serve_forever()

    def shutdown(self):
        self.webhooks.shutdown()
