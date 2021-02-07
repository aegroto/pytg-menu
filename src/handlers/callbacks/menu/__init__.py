import telegram, yaml, logging

from telegram.ext import CallbackQueryHandler

from pytg.load import *

from .switch import switch_callback_handler
from .switchf import switchf_callback_handler
from .cancel import cancel_callback_handler

def load_menu_callback_handlers(dispatcher):
    module_id = get_module_id("menu")

    dispatcher.add_handler(CallbackQueryHandler(switch_callback_handler, pattern="menu,switch,*"), group=module_id)
    dispatcher.add_handler(CallbackQueryHandler(switchf_callback_handler, pattern="menu,switchf,*"), group=module_id)
    dispatcher.add_handler(CallbackQueryHandler(cancel_callback_handler, pattern="menu,cancel,*"), group=module_id)