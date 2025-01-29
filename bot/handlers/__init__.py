from aiogram import Router

from handlers.admin import router as admin_router
from handlers.check import router as check_router
from handlers.contact import router as contact_router
from handlers.help import router as help_router
from handlers.start import router as start_router
from handlers.utils import router as utils_router

router = Router()

router.include_router(admin_router)
router.include_router(check_router)
router.include_router(contact_router)
router.include_router(help_router)
router.include_router(start_router)
router.include_router(utils_router)
