from datetime import datetime

from aiogram import F, Router, types
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.utils.i18n import gettext as _
from aiogram.utils.i18n import lazy_gettext as __
from config import settings
from database.controllers import user_is_whitelisted
from fastapi.exceptions import HTTPException

from src.api.v1.endpoints.imei import check_imei_endpoint
from src.schemas.check import CheckCreate, Property
from src.schemas.imei import IMEIRequest

router = Router()


class CheckIMEIState(StatesGroup):
    waiting_for_imei = State()


async def check_user_is_whitelisted(
    message: types.Message, user_id: int = None
) -> bool:
    if not await user_is_whitelisted(int(user_id)):
        text = _(
            "⛔️ You do not have access to the bot functionality. "
            "Please contact the administrator to be added to the whitelist.\n\n"
            "📩 Contact admin: @{adminUsername}"
        )
        await message.answer(
            text=text.format(
                adminUsername=settings.TELEGRAM_ADMIN_USERNAME,
            ),
        )
        return False
    return True


@router.message(F.text == __("🔍 Check IMEI"))
async def ask_for_imei(message: types.Message, state: FSMContext):
    if not await check_user_is_whitelisted(message, user_id=message.from_user.id):
        return

    await message.answer(_("🔢 Please enter the IMEI number (15 digits):"))
    await state.set_state(CheckIMEIState.waiting_for_imei)


@router.message(CheckIMEIState.waiting_for_imei)
async def handle_imei_input(message: types.Message, state: FSMContext):
    imei = message.text.strip()
    await state.clear()
    await process_imei(message, imei)


@router.message(Command("check"))
async def process_imei_command(message: types.Message):
    if not await check_user_is_whitelisted(message, user_id=message.from_user.id):
        return

    imei = message.text.replace("/check", "").strip()
    if not imei:
        await message.answer(
            _(
                "❗ Please enter the IMEI number after the command, like this:\n"
                "`/check 123456789012345`"
            ),
            parse_mode=ParseMode.MARKDOWN,
        )
        return

    await process_imei(message, imei)


async def process_imei(message: types.Message, imei: str):
    try:
        IMEIRequest.validate_imei(imei)
        text = _(
            "✅ The IMEI number {imei} is valid.\n"
            "Fetching information about the device..."
        )
        confirmation_message = await message.answer(text=text.format(imei=imei))

        check: CheckCreate = await check_imei_endpoint(
            IMEIRequest(imei=imei, token=settings.IMEI_SANDBOX_TOKEN)
        )

        device_info: Property = check.properties

        additional_data = (
            "\n".join(
                [
                    f"- <b>{key}</b>: <code>{value}</code>"
                    for key, value in device_info.additional_data.items()
                ]
            )
            if device_info.additional_data
            else "No additional data available."
        )

        text = _(
            "📱 <b>✅ Verification complete! "
            "Here is the information for your device:</b>\n"
            "🔹 <b>Name:</b> <b>{deviceName}</b>\n"
            "🔹 <b>Serial Number:</b> <code>{serial}</code>\n"
            "🔹 <b>Estimated Purchase Date:</b> {estPurchaseDate}\n"
            '🖼 <b>Image:</b> <a href="{image}">Image Link</a>\n\n'
            "📂 <b>Additional Data:</b>\n"
            "<pre>{additional_data}</pre>"
        )

        await confirmation_message.edit_text(
            text=text.format(
                deviceName=device_info.deviceName,
                serial=device_info.serial,
                estPurchaseDate=datetime.fromtimestamp(
                    device_info.estPurchaseDate
                ).strftime("%Y-%m-%d")
                if device_info.estPurchaseDate
                else "Unknown",
                image=device_info.image,
                additional_data=additional_data,
            ),
            parse_mode=ParseMode.HTML,
        )

    except ValueError:
        text = _(
            "❌ The IMEI number <code>{imei}</code> is invalid.\n"
            "Please enter a valid IMEI number.\n\n"
            "To find the IMEI on your device:\n"
            "🔹 <b>For Android:</b> Dial <code>*#06#</code> or go to <b>Settings</b> → "
            "<b>About Phone</b> → <b>Status</b> → <b>IMEI Information</b>.\n"
            "🔹 <b>For Apple (iPhone):</b> Dial <code>*#06#</code> or go to "
            "<b>Settings</b> → "
            "<b>General</b> → <b>About</b>, and scroll down to find the IMEI."
        )
        await message.answer(
            text=text.format(imei=imei),
            parse_mode=ParseMode.HTML,
        )
    except HTTPException as e:
        await confirmation_message.edit_text(
            _("❌ Device information could not be fetched. Reason: {reason}").format(
                reason=e.detail
            )
        )
    except Exception as e:
        await confirmation_message.edit_text(
            _("❌ An unexpected error occurred. Please try again later.")
        )
        print(f"Unexpected error: {str(e)}")
