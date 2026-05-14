"""
Backward-compatible re-export: all settings now live in app.config.
"""

import warnings
warnings.warn(
    "Import from 'app.config' instead of 'config.settings'. "
    "This shim will be removed in a future version.",
    DeprecationWarning,
    stacklevel=2,
)

from app.config import get_settings

settings = get_settings()

__all__ = ["settings", "get_settings"]
