import telegram, yaml, logging

from modules.pytg.ModulesLoader import ModulesLoader

def menu_callback_handler(update, context):
    bot = context.bot

    query = update.callback_query
    query_data = query.data.split(",")
    user_id = query.from_user.id

    username = query.message.chat.username
    chat_id = query.message.chat_id
    message_id = query.message.message_id

    logging.info("Handling menu callback data from {}: {}".format(chat_id, query_data))

    if query_data[1] == "switch":
        module_name = query_data[2]
        menu_id = query_data[3]

        menu_manager = ModulesLoader.load_manager("menu")
        menu_manager.switch_menu(bot, chat_id, module_name, menu_id, message_id)

        return

    if query_data[1] == "switchf":
        module_name = query_data[2]
        menu_id = query_data[3]

        menu_manager = ModulesLoader.load_manager("menu")
        menu_manager.switch_menu(bot, chat_id, module_name, menu_id, message_id, force=True)

        return