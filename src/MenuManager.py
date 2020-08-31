import telegram, yaml, logging, traceback

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup

from modules.pytg.Manager import Manager
from modules.pytg.ModulesLoader import ModulesLoader

class MenuManager(Manager):
    @staticmethod
    def initialize():
        MenuManager.__instance = MenuManager()

        return

    @staticmethod
    def load():
        return MenuManager.__instance

    def __init__(self):
        self.cached_reply_markup = { }

    ###################
    # Menus interface #
    ###################

    def create_reply_markup(self, module_name, menu_id, lang=None, meta={}):
        if not lang:
            config_manager = ModulesLoader.load_manager("config")
            lang_settings = config_manager.load_settings_file("menu", "lang")
            lang = lang_settings["default"]

        full_menu_id = "{}_{}".format(menu_id, lang)

        # Check if reply markup is cached
        if menu_id in self.cached_reply_markup.keys():
            return self.cached_reply_markup[full_menu_id]

        # Otherwise, create reply markup
        logging.info("Reply markup is not cached, loading...")

        module_folder = ModulesLoader.get_module_content_folder(module_name)

        menu_format = self.__load_format(module_name, menu_id)
        phrases = self.__load_phrases(module_name, menu_id, lang)

        menu_layout = []

        # Inline menu
        if menu_format["type"] == "inline":
            for row in menu_format["markup"]:
                menu_row = []

                for button in row:
                    # Retrieve phrase
                    text = phrases[button["phrase"]]

                    # Retrieving callback data
                    callback_data = None
                    if "callback_data" in button.keys():
                        callback_data = button["callback_data"]

                        # Replace meta keys
                        for meta_key in meta:
                            callback_data = callback_data.replace(meta_key, str(meta[meta_key]))

                    # Retrieving URL
                    url = None
                    if "url" in button.keys():
                        url = button["url"]

                        # Replace meta keys
                        for meta_key in meta:
                            url = url.replace(meta_key, str(meta[meta_key]))

                    menu_row.append(InlineKeyboardButton(text, callback_data = callback_data, url = url))

                menu_layout.append(menu_row)
                
            reply_markup = InlineKeyboardMarkup(menu_layout)
        else:
        # Reply menu
            for row in menu_format["markup"]:
                menu_row = []

                for button in row:
                    menu_row.append(KeyboardButton(button["text"]))

                menu_layout.append(menu_row)
                
            reply_markup = ReplyKeyboardMarkup(menu_layout, resize_keyboard=True)

        if menu_format["cacheable"]:
            logging.info("Saving reply markup in cache...")
            self.cached_reply_markup[full_menu_id] = reply_markup

        return reply_markup
    
    def __load_format(self, module_name, menu_id):
        module_folder = ModulesLoader.get_module_content_folder(module_name)

        return yaml.safe_load(open("{}/menu/formats/{}.yaml".format(module_folder, menu_id), "r", encoding="utf8"))

    def __load_phrases(self, module_name, menu_id, lang):
        module_folder = ModulesLoader.get_module_content_folder(module_name)

        return yaml.safe_load(open("{}/menu/phrases/{}/{}.yaml".format(module_folder, lang, menu_id), "r", encoding="utf8"))

    def switch_menu(self, bot, chat_id, module_name, menu_id, message_id=None, force=False):
        logging.info("Switching to menu {} for {} (message {})".format(menu_id, chat_id, message_id))

        reply_markup = self.create_reply_markup(module_name, menu_id)

        menu_headers = self.load_menu_headers()

        if message_id:
            try:
                bot.editMessageText(
                    chat_id = chat_id,
                    text = menu_headers["{}".format(menu_id)],
                    message_id = message_id,
                    reply_markup = reply_markup
                )
            except:
                if force:
                    bot.deleteMessage(
                        chat_id = chat_id,
                        message_id = message_id
                    )

                    bot.sendMessage(
                        chat_id = chat_id,
                        text = menu_headers["{}".format(menu_id)],
                        reply_markup = reply_markup
                    )
                else:
                    logging.error("Exception while switching menus")
                    traceback.print_exc()
        else:
            bot.sendMessage(
                chat_id = chat_id,
                text = menu_headers["{}".format(menu_id)],
                reply_markup = reply_markup
            )

    def load_menu_headers(self, lang=None):
        module_folder = ModulesLoader.get_module_content_folder("menu")

        if not lang:
            config_manager = ModulesLoader.load_manager("config")
            lang_settings = config_manager.load_settings_file("menu", "lang")
            lang = lang_settings["default"]

        return yaml.safe_load(open("{}/text/{}/menu_headers.yaml".format(module_folder, lang), "r", encoding="utf8"))