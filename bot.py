import asyncio
import logging
from aiogram.types import ContentType, Message
from aiogram import Bot, types
from aiogram.utils import executor
from aiogram.utils.emoji import emojize
from aiogram.dispatcher import Dispatcher
from aiogram.types.message import ContentType
from aiogram.utils.markdown import text, bold, italic, code, pre
from aiogram.types import ParseMode, InputMediaPhoto, InputMediaVideo, ChatActions
from keyboards import kb

from config import TOKEN
#import keyboards as kb

logging.basicConfig(format=u'%(filename)s [ LINE:%(lineno)+3s ]#%(levelname)+8s [%(asctime)s]  %(message)s',
                    level=logging.INFO)

CAT_BIG_EYES = 'AgACAgIAAxkBAAO6YkmutzSNp8wuVw7-bUYT29JFuKYAAn-6MRvbEkhKomKqUOn4QHABAAMCAAN4AAMjBA'
KITTENS = [
    'AgADAgADN6kxG3hu6EqJjb2_dtnztAw4ABMPliaCdHTFDDxsCAAEC',
    'AgADAgADNakxG3hu6EpaqKVQcmEPqAw4ABKKK02zsSoEJtRwCAAEC',
    'AgADAgADNKkxG3hu6EoNCek5IUkeZQw4ABPbUDtX7JTIZmjwAAgI',
]
VOICE = 'AwADAgADXQEAAnhu6vqdylJRvBgI'
VIDEO = 'BAADAgADXAEAAnhuDHE-xNjIzMgI'
TEXT_FILE = 'BQADAgADWgEA6ErgyjSYkwOL6AI'
VIDEO_NOTE = 'DQADAgADWwEu6EoFqDa-fStSmgI'


bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(content_types=ContentType.PHOTO)
async def send_photo_id(message: Message):
    await message.reply(message.photo[-1].file_id)

@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    await message.reply('Привет!\nИспользуй /help, '
                        'чтобы узнать список доступных команд!',reply_markup=kb)


@dp.message_handler(commands=['help'])
async def process_help_command(message: types.Message):
    msg = text(bold('Я могу ответить на следующие команды:'),
               '/voice', '/photo', '/group', '/note', '/file, /testpre', sep='\n')
    await message.reply(msg, parse_mode=ParseMode.MARKDOWN)


@dp.message_handler(commands=['voice'])
async def process_voice_command(message: types.Message):
    await bot.send_voice(message.from_user.id, VOICE,
                         reply_to_message_id=message.message_id)


@dp.message_handler(commands=['photo'])
async def process_photo_command(message: types.Message):
    caption = 'Какие глазки! :eyes:'
    await bot.send_photo(message.from_user.id, CAT_BIG_EYES,
                         caption=emojize(caption),
                         reply_to_message_id=message.message_id)


@dp.message_handler(commands=['group'])
async def process_group_command(message: types.Message):
    media = [InputMediaVideo(VIDEO, 'ёжик и котятки')]
    for photo_id in KITTENS:
        media.append(InputMediaPhoto(photo_id))
    await bot.send_media_group(message.from_user.id, media)


@dp.message_handler(commands=['note'])
async def process_note_command(message: types.Message):
    user_id = message.from_user.id
    await bot.send_chat_action(user_id, ChatActions.RECORD_VIDEO_NOTE)
    await asyncio.sleep(1)  # конвертируем видео и отправляем его пользователю
    await bot.send_video_note(message.from_user.id, VIDEO_NOTE)


@dp.message_handler(commands=['file'])
async def process_file_command(message: types.Message):
    user_id = message.from_user.id
    await bot.send_chat_action(user_id, ChatActions.UPLOAD_DOCUMENT)
    await asyncio.sleep(1)  # скачиваем файл и отправляем его пользователю
    await bot.send_document(user_id, TEXT_FILE,
                            caption='Этот файл специально для тебя!')





@dp.message_handler()
async def echo_message(msg: types.Message):
    await bot.send_message(msg.from_user.id, msg.text)


@dp.message_handler(content_types=ContentType.ANY)
async def unknown_message(msg: types.Message):
    message_text = text(emojize('Я не знаю, что с этим делать :astonished:'),
                        italic('\nЯ просто напомню,'), 'что есть',
                        code('команда'), '/help')
    await msg.reply(message_text, parse_mode=ParseMode.MARKDOWN)


if __name__ == '__main__':
    executor.start_polling(dp)