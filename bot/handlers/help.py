from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram import html


router = Router()


@router.message(Command("help"))
async def command_help_handler(message: Message) -> None:
    await message.answer(
        f"{html.bold('Available commands:')}\n"
        f"/start - Start the bot\n"
        f"/help - Show this help message\n")

