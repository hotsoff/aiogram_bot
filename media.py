from aiogram.types import ContentType, Message

from bot import dp


@dp.message_handler(content_types=ContentType.PHOTO)
async def send_photo_id(message: Message):
	await message.reply(message.photo[-1].file_id)