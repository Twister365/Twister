from builtins import next, iter

import requests
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from googletrans import Translator

from tgbot.config import load_config

translator = Translator()
async def get_person_info(person_name):
    try:
        url1 = f"https://en.wikipedia.org/w/api.php?action=query&format=json&formatversion=2&prop=pageimages|pageterms&piprop=original&titles={person_name}"
        url = f"https://en.wikipedia.org/w/api.php?action=query&format=json&prop=extracts&exintro&explaintext&titles={person_name}"
        response = requests.get(url)
        data = response.json()
        pages = data['query']['pages']
        page_id = next(iter(pages))
        extract = pages[page_id]['extract']
        text = translator.translate(extract, dest='uk').text[:1024]
        response = requests.get(url1)
        data = response.json()
        photo = data["query"]["pages"][0]["original"]["source"]
        return text, photo
    except Exception as e:
        print(e)
        return None




async def start_command(message: types.Message):
    await message.reply("Привет! Я бот, который может найти информацию о человеке. Просто напиши имя пользователя, и я попытаюсь найти его данные.")



async def handle_message(message: types.Message):
    person_name = message.text
    person_info = await get_person_info(person_name)

    if person_info is None:
        await message.reply('Не удалось найти информацию о человеке.')
    else:
        await message.answer_photo(photo=person_info[1],caption=person_info[0])



def register_user(dp: Dispatcher):
    dp.register_message_handler(start_command, commands=["start"])
    dp.register_message_handler(handle_message)
