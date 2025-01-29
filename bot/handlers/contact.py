from aiogram import Router, types
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.utils.i18n import gettext as _
from config import settings
from database.controllers import user_is_admin

router = Router()


@router.message(Command("contact"))
async def contact(message: types.Message):
    admin_username = settings.TELEGRAM_ADMIN_USERNAME

    if not admin_username:
        await message.answer(
            "⚠️ The administrator's contact information is not available."
        )
        return

    contact_message = _(
        "📩 Need help? Contact the administrator:\n"
        "🔹 [@{adminUsername}](https://t.me/{adminUsername})"
    ).format(adminUsername=admin_username)

    await message.answer(contact_message, parse_mode=ParseMode.MARKDOWN)


@router.message(Command("get_token"))
async def get_token(message: types.Message):
    user_id = message.from_user.id

    if not await user_is_admin(user_id):
        await message.answer(_("❌ You do not have permission to use this command."))
        return

    api_token = settings.IMEI_SANDBOX_TOKEN

    if not api_token:
        await message.answer("⚠️ API token is not configured.")
        return

    await message.answer(
        _("🔑 Your API token:\n`{token}`").format(token=api_token),
        parse_mode=ParseMode.MARKDOWN,
    )
