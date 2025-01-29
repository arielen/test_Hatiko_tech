from functools import wraps

from aiogram import F, Router, types
from aiogram.utils.i18n import gettext as _

previous_messages = {}


router = Router()


def save_previous_message(func):
    @wraps(func)
    async def wrapper(callback: types.CallbackQuery, *args, **kwargs):
        user_id = int(callback.from_user.id)
        if user_id not in previous_messages:
            previous_messages[user_id] = []

        previous_messages[user_id].append(
            {
                "text": callback.message.text,
                "reply_markup": callback.message.reply_markup,
            }
        )
        return await func(callback, *args, **kwargs)

    return wrapper


@router.callback_query(F.data == "go_back")
async def go_back(callback: types.CallbackQuery):
    user_id = int(callback.from_user.id)
    if user_id in previous_messages:
        prev_message = previous_messages[user_id].pop()
        await callback.message.edit_text(
            prev_message["text"], reply_markup=prev_message["reply_markup"]
        )
    else:
        await callback.message.answer(_("No previous message to return to."))
