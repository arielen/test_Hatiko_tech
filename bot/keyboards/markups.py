from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
)
from aiogram.utils.i18n import gettext as _


class Keyboards:
    def get_language() -> InlineKeyboardMarkup:
        buttons = [
            [
                InlineKeyboardButton(text="🇷🇺 Русский", callback_data="lang_ru"),
                InlineKeyboardButton(text="🇬🇧 English", callback_data="lang_en"),
            ],
        ]
        return InlineKeyboardMarkup(inline_keyboard=buttons)

    def get_main_keyboard() -> ReplyKeyboardMarkup:
        buttons = [
            [
                KeyboardButton(text=_("🔍 Check IMEI")),
            ],
            [
                KeyboardButton(text=_("📖 Help")),
                KeyboardButton(text=_("🌍 Change Language")),
            ],
        ]
        return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)

    def get_admin_keyboard() -> ReplyKeyboardMarkup:
        buttons = [
            [
                KeyboardButton(text=_("➕ Add Admin (/add_admin)")),
                KeyboardButton(text=_("➖ Remove Admin (/remove_admin)")),
            ],
            [
                KeyboardButton(text=_("✅ Add to Whitelist (/add_whitelist)")),
                KeyboardButton(text=_("❌ Remove from Whitelist (/remove_whitelist)")),
            ],
            [
                KeyboardButton(text=_("🔑 Get API Token (/get_token)")),
                KeyboardButton(text=_("📖 Help (/help)")),
            ],
        ]

        return ReplyKeyboardMarkup(
            keyboard=buttons,
            resize_keyboard=True,
            input_field_placeholder=_("Admin options"),
        )

    def get_back_keyboard() -> InlineKeyboardMarkup:
        buttons = [[InlineKeyboardButton(text=_("🔙 Back"), callback_data="go_back")]]
        return InlineKeyboardMarkup(inline_keyboard=buttons)
