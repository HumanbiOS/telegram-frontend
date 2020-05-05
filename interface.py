from telegram.ext import Updater, MessageHandler, Filters, CallbackQueryHandler

from webhook import OwnWebhook
from bot import text_handler, callbackquery_handler
import settings


def main():
    updater = Updater(token=settings.BOT_TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(MessageHandler(Filters.text, text_handler))
    dp.add_handler(CallbackQueryHandler(callbackquery_handler))
    webhook_thread = OwnWebhook(dp.bot)
    webhook_thread.start()
    updater.start_polling()
    updater.idle()
    webhook_thread.shutdown()


if __name__ == "__main__":
    main()
