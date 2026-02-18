from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram import html



router = Router()


@router.message()
async def echo_handler(message: Message) -> None:
    try:
        await message.send_copy(chat_id=message.chat.id)
        
    except TypeError:
        await message.answer("Nice try!")
