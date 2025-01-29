from aiogram import Bot, Router, types
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.utils.i18n import gettext as _
from config import settings
from database.controllers import (
    set_user_is_admin,
    set_user_is_whitelisted,
    user_exists,
    user_is_admin,
)
from signals import notify_user_role_change, user_role_changed

router = Router()


async def validate_admin_command(message: types.Message) -> int | None:
    current_user_id = message.from_user.id
    args = message.text.split()

    if len(args) != 2:
        text = _("❌ Invalid command usage. Usage: `{command} <id>`")
        await message.answer(
            text=text.format(command=args[0]),
            parse_mode=ParseMode.MARKDOWN,
        )
        return

    if not await user_is_admin(current_user_id):
        await message.answer(_("❌ You do not have permission to use this command."))
        return

    try:
        tg_id = int(args[1])
        if not await user_exists(tg_id):
            text = _("❌ User with ID {tg_id} does not exist.")
            await message.answer(text=text.format(tg_id=tg_id))
            return
    except ValueError:
        await message.answer(
            _("❌ Invalid Telegram ID. Please provide a valid number.")
        )
        return

    return tg_id


@router.message(Command("add_admin", "remove_admin"))
async def manage_admin(message: types.Message, bot: Bot) -> None:
    tg_id = await validate_admin_command(message)
    if not tg_id:
        return

    if message.text.startswith("/remove_admin") and tg_id == settings.TELEGRAM_ADMIN_ID:
        await message.answer(_("❌ You cannot remove the main admin."))
        return

    is_admin: bool = message.text.startswith("/add_admin")
    await set_user_is_admin(tg_id, is_admin)
    status = "now an admin" if is_admin else "no longer an admin"
    await message.answer(f"✅ User with ID {tg_id} is {status}.")

    action = "Granted Admin Rights" if is_admin else "Revoked Admin Rights"
    await user_role_changed(bot, tg_id, action, message.from_user.id)
    await notify_user_role_change(bot, tg_id, action)


@router.message(Command("add_whitelist", "remove_whitelist"))
async def manage_whitelist(message: types.Message, bot: Bot) -> None:
    tg_id = await validate_admin_command(message)
    if not tg_id:
        return

    is_whitelisted: bool = message.text.startswith("/add_whitelist")
    await set_user_is_whitelisted(tg_id, is_whitelisted)
    status = "now whitelisted" if is_whitelisted else "no longer whitelisted"
    await message.answer(f"✅ User with ID {tg_id} is {status}.")

    action = "Added to Whitelist" if is_whitelisted else "Removed from Whitelist"
    await user_role_changed(bot, tg_id, action, message.from_user.id)
    await notify_user_role_change(bot, tg_id, action)
