import logging

from pytg.load import manager

LOGGER = logging.getLogger(__name__)

def switchf_callback_handler(update, context):
    bot = context.bot

    query = update.callback_query
    query_data = query.data.split(",")

    chat_id = query.message.chat_id
    message_id = query.message.message_id

    LOGGER.info("Handling switchf callback data from {}: {}".format(chat_id, query_data))

    module_name = query_data[2]
    menu_id = query_data[3]

    manager("menu").switch_menu(bot, chat_id, module_name, menu_id, message_id, force=True)