from .start import router as start_router
from .help import router as help_router
from .record import router as record_router
from .setup import router as setup_router


__all__ = [
    'start_router',
    'help_router',
    'record_router',
    'setup_router'
]

routers = [start_router, help_router, record_router, setup_router]
