from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils import executor
import logging
import os

API = ''

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()

inline_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton('Рассчитать', callback_data='calculate'),
            InlineKeyboardButton('Информация', callback_data='info')
        ]
    ]
)

main_kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
main_kb.add(types.KeyboardButton("Купить"))

product_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton('Product1', callback_data='product1_buying'),
            InlineKeyboardButton('Product2', callback_data='product2_buying')
        ],
        [
            InlineKeyboardButton('Product3', callback_data='product3_buying'),
            InlineKeyboardButton('Product4', callback_data='product4_buying')
        ]
    ]
)

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer('Привет! Я бот, помогающий твоему здоровью.', reply_markup=main_kb)

@dp.message_handler(lambda message: message.text == "Купить")
async def get_buying_list(message: types.Message):
    products = [
        ('https://raw.githubusercontent.com/tracerwhite24/module14_tasks/3cb7cb89779334ba4dae571821cdc51bea9933ac/pr01.jpg', "Название: Product1 | Описание: Бананы | Цена: 100"),
        ('https://raw.githubusercontent.com/tracerwhite24/module14_tasks/3cb7cb89779334ba4dae571821cdc51bea9933ac/pr02.jpg', "Название: Product2 | Описание: Помидоры| Цена: 200"),
        ('https://raw.githubusercontent.com/tracerwhite24/module14_tasks/3cb7cb89779334ba4dae571821cdc51bea9933ac/pr03.jpg', "Название: Product3 | Описание: Ягоды | Цена: 300"),
        ('https://raw.githubusercontent.com/tracerwhite24/module14_tasks/3cb7cb89779334ba4dae571821cdc51bea9933ac/pr04.jpg', "Название: Product4 | Описание: Яблоки | Цена: 400")
    ]

    for image_url, description in products:
        await bot.send_photo(chat_id=message.from_user.id, photo=image_url)
        await bot.send_message(chat_id=message.from_user.id, text=description)

    else:
        logging.warning(f"Файл не найден")

        await message.answer("Выберите продукт для покупки:", reply_markup=product_kb)

@dp.callback_query_handler(lambda c: c.data.endswith('_buying'))
async def send_confirm_message(call: types.CallbackQuery):
    product_name = call.data[:-8]
    await call.answer("Вы успешно приобрели продукт!")
    await bot.send_message(call.from_user.id, f"Вы успешно приобрели {product_name}!")

@dp.callback_query_handler(text="calculate")
async def set_age(call: types.CallbackQuery):
    await call.message.answer("Введите свой возраст:")
    await call.answer()
    await UserState.age.set()

@dp.callback_query_handler(lambda c: c.data == "info")
async def info_command(callback_query: types.CallbackQuery):
    await bot.send_message(callback_query.from_user.id,
                           "Этот бот поможет вам рассчитать вашу норму калорий. Нажмите 'Рассчитать', чтобы начать процесс расчета.")

@dp.message_handler(state=UserState.age)
async def set_growth(message: types.Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("Пожалуйста, введите корректный возраст (число).")
        return

    await state.update_data(age=int(message.text))

    await message.answer("Введите свой рост в сантиметрах:")
    await UserState.next()


@dp.message_handler(state=UserState.growth)
async def set_weight(message: types.Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("Пожалуйста, введите корректный рост (число).")
        return

    await state.update_data(growth=int(message.text))

    await message.answer("Введите свой вес в килограммах:")
    await UserState.next()

@dp.message_handler(state=UserState.weight)
async def finish_calculation(message: types.Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("Пожалуйста, введите корректный вес (число).")
        return

    await state.update_data(weight=int(message.text))

    user_data = await state.get_data()
    age = user_data['age']
    growth = user_data['growth']
    weight = user_data['weight']

    await message.answer(f"Ваш возраст: {age}, рост: {growth}, вес: {weight}.")

    await state.finish()

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
















