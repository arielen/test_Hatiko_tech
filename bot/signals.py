from aiogram import Bot
from config import settings


async def user_role_changed(bot: Bot, tg_id: int, action: str, changed_by: int):
    admin_chat_id = settings.TELEGRAM_ADMIN_ID
    message = (
        f"🔔 <b>User Role Update</b>\n"
        f"👤 User ID: <code>{tg_id}</code>\n"
        f"⚡ Action: {action}\n"
        f"👮 Changed by: <code>{changed_by}</code>"
    )
    await bot.send_message(admin_chat_id, message, parse_mode="HTML")


async def new_user_registered(bot: Bot, tg_id: int, username: str, full_name: str):
    admin_chat_id = settings.TELEGRAM_ADMIN_ID
    username_text = f"@{username}" if username else "No username"

    message = (
        f"👋 <b>New User Joined</b>\n"
        f"👤 <b>Name:</b> {full_name}\n"
        f"🔹 <b>Username:</b> {username_text}\n"
        f"🆔 <b>ID:</b> <code>{tg_id}</code>\n"
    )
    await bot.send_message(admin_chat_id, message, parse_mode="HTML")


async def notify_user_role_change(bot: Bot, tg_id: int, action: str):
    messages = {
        "Granted Admin Rights": (
            "🎩 You have been granted admin rights! Use /help for commands."
        ),
        "Revoked Admin Rights": "🚫 Your admin rights have been revoked.",
        "Added to Whitelist": (
            "✅ You have been added to the whitelist! Now you can use the bot."
        ),
        "Removed from Whitelist": (
            "⚠️ You have been removed from the whitelist. "
            "You may lose access to some features."
        ),
    }

    message = messages.get(action, "ℹ️ Your permissions have been updated.")

    try:
        await bot.send_message(tg_id, message)
    except Exception as e:
        print(f"⚠️ Failed to notify user {tg_id}: {e}")
