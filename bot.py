import json

import settings

H = {'content-type': 'application/json'}


def text_handler(update, context):
    # REQUIRED PAYLOAD
    process(update, context)


def callbackquery_handler(update, context):
    update.callback_query.answer()
    process(update, context)


def process(update, context):
    sender_id = update.effective_user.id
    user = update.effective_user
    if update.callback_query:
        text = str(update.callback_query.data)
    else:
        text = update.effective_message.text
    payload = {
        "security_token": context.bot_data["infos"]["token"],
        "via_instance": context.bot_data["infos"]["name"],
        "service_in": "telegram",
        "user": {
            "user_id": sender_id,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "username": user.username,
            "lang_code": user.language_code
        },
        "chat": {
            "chat_id": sender_id
        },
        "has_message": True,
        "message": {
            "text": text
        }
    }
    encoded_data = json.dumps(payload).encode('utf-8')
    print(payload)
    response = context.bot.request._con_pool.request("POST", f"{settings.SERVER_URL}/api/process_message",
                                                     body=encoded_data, headers=H)
    print(response.data)
    response_dict = json.loads(response.data)
    print(response_dict)
