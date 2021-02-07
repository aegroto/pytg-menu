import logging

from pytg.load import manager

from .MenuManager import MenuManager

from .handlers.callbacks.menu import load_menu_callback_handlers

def connect():
    load_menu_callback_handlers(manager("bot").updater.dispatcher)

def initialize_manager():
    return MenuManager()

def depends_on():
    return ["bot"]