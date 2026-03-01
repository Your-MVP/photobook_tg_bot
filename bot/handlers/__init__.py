"""Handlers package initializer for Photobook Bot MVP v0.1.0.

Aggregates all routers (commands, photos, etc.) into a single main router.
"""

from .commands import router

# If you have more handlers (e.g. photos.py), add them here:
# from .photos import router as photos_router
# router.include_router(photos_router)