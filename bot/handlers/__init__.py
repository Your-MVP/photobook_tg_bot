from aiogram import Router

from .commands import router as commands_router
from .photos import router as photos_router

router = Router(name="main_handlers")

router.include_router(commands_router)
router.include_router(photos_router)

__all__ = ["router"]