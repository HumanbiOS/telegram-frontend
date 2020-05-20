import json

from telegram.ext import Updater, MessageHandler, Filters, CallbackQueryHandler

from webhook import OwnWebhook
from bot import text_handler, callbackquery_handler
import settings


def setup(bot):
    payload = {
        "security_token": settings.SERVER_TOKEN,
        "url": settings.INSTANCE_URL,
        "broadcast": settings.TELEGRAM_BROADCAST,
        "psychological_room": settings.TELEGRAM_PSYCHOLOGIST_ROOM,
        "doctor_room": settings.TELEGRAM_DOCTOR_ROOM
    }
    encoded_data = json.dumps(payload).encode('utf-8')
    response = bot.request._con_pool.request("POST", f"{settings.SERVER_URL}/api/setup", body=encoded_data)
    response_dict = json.loads(response.data)
    return response_dict["name"], response_dict["token"]


def main():
    updater = Updater(token=settings.BOT_TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(MessageHandler(Filters.text, text_handler))
    dp.add_handler(CallbackQueryHandler(callbackquery_handler))
    name, token = setup(dp.bot)
    dp.bot_data["infos"] = {"name": name, "token": token}
    webhook_thread = OwnWebhook(dp.bot)
    webhook_thread.start()
    updater.start_polling()
    updater.idle()
    webhook_thread.shutdown()


if __name__ == "__main__":
    main()
