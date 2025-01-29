from aiogram import F, Router, types
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.utils.i18n import gettext as _
from aiogram.utils.i18n import lazy_gettext as __
from database.controllers import user_is_admin, user_is_whitelisted

router = Router()


@router.message(Command("help"))
@router.message(F.text == __("📖 Help"))
async def help(message: types.Message):
    user_id = message.from_user.id
    is_admin = await user_is_admin(user_id)
    is_whitelisted = await user_is_whitelisted(user_id)

    help_text = _(
        "🤖 <b>Bot Command Guide:</b>\n\n"
        "📌 <b>General Commands:</b>\n"
        "/start - Start interacting with the bot\n"
        "/help - Show this help message\n"
        "/language - Change the bot's language\n"
        "/myid - Get your Telegram ID\n\n"
    )

    if is_whitelisted:
        help_text += _(
            "📌 <b>IMEI Checking:</b>\n"
            "/check &lt;IMEI&gt; - Check device information using an IMEI number\n\n"
        )
    else:
        help_text += _(
            "📌 <b>IMEI Checking:</b>\n"
            "⛔️ You do not have access to check IMEI.\n"
            "Ask an administrator to add you to the whitelist.\n\n"
        )

    if is_admin:
        help_text += _(
            "📌 <b>Admin Commands:</b>\n"
            "/add_admin &lt;id&gt; - Grant admin rights to a user\n"
            "/remove_admin &lt;id&gt; - Revoke admin rights from a user\n"
            "/add_whitelist &lt;id&gt; - Add a user to the whitelist\n"
            "/remove_whitelist &lt;id&gt; - Remove a user from the whitelist\n"
            "/get_token - Get your API token\n\n"
        )

    help_text += _(
        "📌 <b>Navigation:</b>\n"
        "Use inline buttons for language selection and other interactions.\n\n"
        "🔹 If you experience any issues, use the /contact command to reach support."
    )

    await message.answer(help_text, parse_mode=ParseMode.HTML)


@router.message(Command("myid"))
async def get_my_id(message: types.Message):
    user_id = message.from_user.id

    response_text = _(
        "🆔 Your Telegram ID: <code>{user_id}</code>\n\n"
        "This unique ID is used to identify you in the bot system."
    ).format(user_id=user_id)

    await message.answer(response_text, parse_mode="HTML")
