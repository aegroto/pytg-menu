import logging

from modules.pytg.ModulesLoader import ModulesLoader

from modules.menu.MenuManager import MenuManager

from telegram.ext import CallbackQueryHandler

from modules.menu.handlers.callback.menu import menu_callback_handler

def load_callback_handlers(dispatcher):
    module_id = ModulesLoader.get_module_id("menu")

    dispatcher.add_handler(CallbackQueryHandler(menu_callback_handler, pattern="menu,.*"), group=module_id)

def initialize():
    logging.info("Initializing menu module...")

    MenuManager.initialize()

def connect():
    logging.info("Connecting menu module...")

    bot_manager = ModulesLoader.load_manager("bot")

    load_callback_handlers(bot_manager.updater.dispatcher)

def load_manager():
    return MenuManager.load()

def depends_on():
    return ["bot"]