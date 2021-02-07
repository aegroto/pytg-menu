import logging

LOGGER = logging.getLogger(__name__)

def cancel_callback_handler(update, context):
    bot = context.bot

    query = update.callback_query

    chat_id = query.message.chat_id
    message_id = query.message.message_id

    LOGGER.info("Handling cancel callback data from {}, {}".format(chat_id, message_id))

    bot.delete_message(chat_id=chat_id, message_id=message_id)
