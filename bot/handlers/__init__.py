from .start import router as start_router
from .help import router as help_router
from .echo import router as echo_router


__all__ = [
    'start_router',
    'help_router',
    'echo_router',
]

routers = [start_router, help_router, echo_router]
