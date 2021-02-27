import telegram, yaml, logging, traceback

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup

from pytg.Manager import Manager
from pytg.load import manager, get_module_content_folder

class MenuManager(Manager):
    def __init__(self):
        self.cached_reply_markup = { }

    def __load_default_lang(self):
        return manager("config").load_settings("menu", "lang")["default"]

    ###################
    # Menus interface #
    ###################

    def create_reply_markup(self, module_name, menu_id, lang=None, meta={}):
        if not lang:
            lang = self.__load_default_lang()

        full_menu_id = "{}_{}".format(menu_id, lang)

        # Check if reply markup is cached
        if menu_id in self.cached_reply_markup.keys():
            return self.cached_reply_markup[full_menu_id]

        # Otherwise, create reply markup
        logging.info("Reply markup is not cached, loading...")

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
                        callback_data = self.__meta_replace(button["callback_data"], meta)

                    # Retrieving URL
                    url = None
                    if "url" in button.keys():
                        url = self.__meta_replace(button["url"], meta)

                    menu_row.append(InlineKeyboardButton(text, callback_data = callback_data, url = url))

                menu_layout.append(menu_row)
                
            reply_markup = InlineKeyboardMarkup(menu_layout)
        else:
        # Reply menu
            for row in menu_format["markup"]:
                menu_row = []

                for button in row:
                    # Retrieve phrase
                    text = phrases[button["phrase"]]

                    menu_row.append(KeyboardButton(text))

                menu_layout.append(menu_row)
                
            reply_markup = ReplyKeyboardMarkup(menu_layout, resize_keyboard=True)

        if menu_format["cacheable"]:
            logging.info("Saving reply markup in cache...")
            self.cached_reply_markup[full_menu_id] = reply_markup

        return reply_markup
    
    def __load_format(self, module_name, menu_id):
        module_folder = get_module_content_folder(module_name)

        return yaml.safe_load(open("{}/menu/formats/{}.yaml".format(module_folder, menu_id), "r", encoding="utf8"))

    def __load_phrases(self, module_name, menu_id, lang):
        module_folder = get_module_content_folder(module_name)

        return yaml.safe_load(open("{}/menu/phrases/{}/{}.yaml".format(module_folder, lang, menu_id), "r", encoding="utf8"))

    def send_menu(self, bot, chat_id, module_name, menu_id, lang=None, meta={}):
        if not lang:
            lang = self.__load_default_lang()

        reply_markup = self.create_reply_markup(module_name, menu_id, meta=meta)

        header_text = self.__load_phrases(module_name, menu_id, lang)["_header"]
        header_text = self.__meta_replace(header_text, meta)

        sent_message = bot.sendMessage(
            chat_id = chat_id,
            text = header_text,
            reply_markup = reply_markup
        )

        return sent_message

    def switch_menu(self, bot, chat_id, module_name, menu_id, message_id=None, meta={}, force=False, lang=None):
        if not lang:
            lang = self.__load_default_lang()

        reply_markup = self.create_reply_markup(module_name, menu_id, meta=meta)

        phrases = self.__load_phrases(module_name, menu_id, lang)

        if "_header" in phrases:
            header_text = phrases["_header"]
            header_text = self.__meta_replace(header_text, meta)
        else:
            header_text = None

        if message_id:
            try:
                if header_text:
                    sent_message = bot.editMessageText(
                        chat_id = chat_id,
                        text = header_text,
                        message_id = message_id,
                        reply_markup = reply_markup
                    )
                else:
                    sent_message = bot.editMessageReplyMarkup(
                        chat_id = chat_id,
                        message_id = message_id,
                        reply_markup = reply_markup
                    )
            except Exception as e:
                if force:
                    bot.deleteMessage(
                        chat_id = chat_id,
                        message_id = message_id
                    )

                    sent_message = bot.sendMessage(
                        chat_id = chat_id,
                        text = header_text,
                        reply_markup = reply_markup
                    )
                else:
                    raise e
        else:
            sent_message = bot.sendMessage(
                chat_id = chat_id,
                text = header_text,
                reply_markup = reply_markup
            )

        return sent_message

    def __meta_replace(self, text, meta):
        return text.format(**meta)