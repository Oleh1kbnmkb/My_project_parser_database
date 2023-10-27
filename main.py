import os
import logging
import asyncio
from states import*
from dotenv import load_dotenv
from parse import get_vacancies
from aiogram import Bot, Dispatcher, types, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage

load_dotenv()

TOKEN = os.getenv('TOKEN')
logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN)
dp = Dispatcher(bot=bot, storage=MemoryStorage())
db = Database()







async def set_default_commands(dp):
     await bot.set_my_commands(
          [
          types.BotCommand('start', 'Запустити бота'),
          types.BotCommand('my_dish', 'Переглянути збережені страви')
          ]
     )




async def get_saved_dishes(telegram_id):
    user = await db.check_user(telegram_id)
    if user:
        saved_dishes = await db.get_saved_dishes_by_telegram_id(telegram_id)
        return saved_dishes
    else:
        return None




@dp.message_handler(commands=['my_dish'])
async def show_saved_dishes(message: types.Message):
    telegram_id = message.from_user.id
    saved_dishes = await get_saved_dishes(telegram_id)
    if saved_dishes:
        saved_dishes_str = "\n".join(saved_dishes)
        response = f"Ваші збережені страви:\n{saved_dishes_str}"
    else:
        response = "Ви ще не зберегли жодну страву."
    
    await message.answer(response)
    
    
    
    

@dp.message_handler(commands='start')
async def start_process(message: types.Message):
    user = await db.check_user(message.from_user.id)
    if not user:
        await db.register_user(
            message.from_user.first_name,
            message.from_user.last_name,
            message.from_user.username,
            message.from_user.id
        )
        await message.answer('Вітаю! 🌟 Ви успішно були зареєстровані.\nВведіть одним або двома словами у пошук будь-яку українську страву, яку хочете приготувати.🍲👨‍🍳')
    else:
        await message.answer('Вітаю! 🌟 Ви уже зареєстровані.\nВведіть одним або двома словами у пошук будь яку українську страву, яку хочете приготувати.🌶️🍴')




current_dish_index = 0
dishes = []

@dp.callback_query_handler(lambda query: query.data in ['save', 'next'])
async def handle_buttons(query: types.CallbackQuery):
    global current_dish_index, dishes

    query_data = query.data

    if query_data == 'save':
        if current_dish_index < len(dishes):
            dish = dishes[current_dish_index]
            await db.save_dish_to_db(query.from_user.id, dish['name'])
            await query.answer("Страву збережено!")
        else:
            await query.answer("Ви переглянули всі доступні страви.")
    elif query_data == 'next':
        current_dish_index += 1
        if current_dish_index < len(dishes):
            await send_dish_info(query.message.chat.id)
        else:
            await query.answer("Ви переглянули всі доступні страви.")

async def send_dish_info(chat_id):
    global current_dish_index, dishes

    if current_dish_index < len(dishes):
        dish = dishes[current_dish_index]

        keyboard = types.InlineKeyboardMarkup()
        save_button = types.InlineKeyboardButton(text="Зберегти страву", callback_data="save")
        next_button = types.InlineKeyboardButton(text="Перейти до наступної страви", callback_data="next")
        keyboard.add(save_button, next_button)

        name = dish['name']
        description = dish['description']
        url = dish['url']
        img = dish['img']

        msg = f'<b>Страва: </b> {name}\n<b>Посилання: </b> {url}\n\n<b>Опис: </b> {description}'

        if img:
            img_url = img[0]
            await bot.send_photo(chat_id, photo=img_url, caption=msg, parse_mode='html', reply_markup=keyboard)
        else:
            await bot.send_message(chat_id, text=msg, parse_mode='html', reply_markup=keyboard)
    else:
        await bot.send_message(chat_id, "Ви переглянули всі доступні страви.")

@dp.message_handler(content_types='text')
async def get_jobs(message: types.Message):
    global current_dish_index, dishes

    query = message.text.lower().strip()
    dishes = get_vacancies(query)
    current_dish_index = 0

    if dishes:
        await send_dish_info(message.chat.id)
    else:
        await message.answer("На жаль, не знайдено жодної страви за вашим запитом.")





@dp.message_handler(commands=['my_dish'])
async def get_my_dishes(message: types.Message):
    user_id = message.from_user.id
    saved_dishes = await db.get_user_saved_dishes(user_id)

    if saved_dishes:
        response = "Ваші збережені страви:\n"
        for dish in saved_dishes:
            response += f"- {dish}\n"
    else:
        response = "Ви ще не зберегли жодну страву."

    await message.answer(response)





async def on_startup(dp):
    loop = asyncio.get_event_loop()
    await set_default_commands(dp)


loop = asyncio.get_event_loop()
if __name__ == "__main__":
  executor.start_polling(dp, loop=loop, on_startup=on_startup)