from aiogram import Bot, F, Router, types
from aiogram.enums import ParseMode
from aiogram.filters import Command, CommandStart
from aiogram.utils.i18n import I18n
from aiogram.utils.i18n import gettext as _
from aiogram.utils.i18n import lazy_gettext as __
from config import settings
from database.controllers import add_user, update_user_language, user_exists
from enums.models import LanguageEmoji, LanguageEnum
from keyboards.markups import Keyboards
from signals import new_user_registered

router = Router()


async def get_bot_usage_guide() -> str:
    return _(
        "📖 Here's how to use the bot:\n\n"
        "1️⃣ Send me your IMEI (15 digits) and I will check it for validity.\n"
        "2️⃣ If IMEI is valid, I will provide information about your device.\n"
        "3️⃣ If something goes wrong, you can contact support via the /contact command."
        "\n\n"
        "You can also use the direct command.\n"
        "Example command: `/check 123456789012345`"
    )


@router.message(CommandStart())
async def start(message: types.Message) -> None:
    user_id: int = message.from_user.id

    if await user_exists(user_id):
        await message.answer(
            text=await get_bot_usage_guide(),
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=Keyboards.get_main_keyboard(),
        )
    else:
        text = _(
            "👋 Hi {userName}, I am a {namePlatform} for checking IMEI of devices.\n"
            "I can help you verify information about your device using its IMEI number."
            "\n\n"
            "Please select a language:"
        )
        await message.answer(
            text=text.format(
                namePlatform=settings.NAME_PLATFORM,
                userName=message.from_user.full_name,
            ),
            reply_markup=Keyboards.get_language(),
        )


@router.message(Command("language"))
@router.message(F.text == __("🌍 Change Language"))
async def language(message: types.Message):
    await message.answer(
        _("Please select a language:"), reply_markup=Keyboards.get_language()
    )


@router.callback_query(F.data.startswith("lang_"))
async def setLanguage(callback: types.CallbackQuery, bot: Bot):
    lang = LanguageEnum(callback.data[5:])
    user_id: int = callback.from_user.id

    if await user_exists(user_id):
        await update_user_language(user_id, lang)
        await callback.message.delete()
        I18n.current_locale = lang.value
        await callback.message.answer(
            _("Language changed to {lang}").format(lang=LanguageEmoji.get(lang)),
            reply_markup=Keyboards.get_main_keyboard(),
        )
    else:
        await add_user(user_id, lang)
        await callback.message.delete()
        I18n.current_locale = lang.value
        await new_user_registered(
            bot=bot,
            tg_id=user_id,
            username=callback.from_user.username,
            full_name=callback.from_user.full_name,
        )

    await callback.message.answer(
        text=await get_bot_usage_guide(),
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=Keyboards.get_main_keyboard(),
    )
