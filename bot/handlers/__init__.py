from aiogram import Router

from bot.middlewares import CatchAllMiddleware

from .commands import router as commands_router
from .photos import router as photos_router
from .guide import router as guide_router
from .ask_email import router as ask_email_router
from .private_chat import router as private_chat_router
from .unhandled import router as unhandled_router

router = Router(name="main_handlers")

router.message.outer_middleware(CatchAllMiddleware())

router.include_router(ask_email_router)
router.include_router(guide_router)
router.include_router(commands_router)
router.include_router(photos_router)
router.include_router(private_chat_router)
router.include_router(unhandled_router)

__all__ = ["router"]