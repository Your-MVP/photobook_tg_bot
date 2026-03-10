from aiogram import Router

from bot.middlewares import CatchAllMiddleware

from .commands import router as commands_router
from .photos import router as photos_router

router = Router(name="main_handlers")

router.message.outer_middleware(CatchAllMiddleware())

router.include_router(commands_router)
router.include_router(photos_router)

__all__ = ["router"]