import sqlite3
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils import executor
from crud_functions import add_product, get_all_products_from_db

API = ''

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

def db_connect():
    conn = sqlite3.connect('products.db')
    return conn

def product_exists(title):
    conn = db_connect()
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) FROM products WHERE title = ?', (title,))
    exists = cursor.fetchone()[0] > 0
    conn.close()
    return exists

def add_product(title, description, price, image_url):
    if not product_exists(title):
        conn = db_connect()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO products (title, description, price, image_url)
            VALUES (?, ?, ?, ?)
        ''', (title, description, price, image_url))
        conn.commit()
        conn.close()

def initialize_products():
    add_product('Product1', 'Бананы', 100, 'https://raw.githubusercontent.com/tracerwhite24/module14_tasks/3cb7cb89779334ba4dae571821cdc51bea9933ac/pr01.jpg')
    add_product('Product2', 'Помидоры', 200, 'https://raw.githubusercontent.com/tracerwhite24/module14_tasks/3cb7cb89779334ba4dae571821cdc51bea9933ac/pr02.jpg')
    add_product('Product3', 'Ягоды', 300, 'https://raw.githubusercontent.com/tracerwhite24/module14_tasks/3cb7cb89779334ba4dae571821cdc51bea9933ac/pr03.jpg')
    add_product('Product4', 'Яблоки', 400, 'https://raw.githubusercontent.com/tracerwhite24/module14_tasks/3cb7cb89779334ba4dae571821cdc51bea9933ac/pr04.jpg')

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer('Привет! Я бот, помогающий с покупкой продуктов.')
    await get_buying_list(message)

@dp.message_handler(lambda message: message.text == "Купить")
async def get_buying_list(message: types.Message):
    products = get_all_products_from_db()

    for product in products:
        await bot.send_photo(chat_id=message.from_user.id, photo=product['image_url'])
        await bot.send_message(chat_id=message.from_user.id,
                               text=f"Название: {product['title']} | Описание: {product['description']} | Цена: {product['price']}")

@dp.callback_query_handler(lambda c: c.data.endswith('_buying'))
async def send_confirm_message(call: types.CallbackQuery):
    product_name = call.data[:-8]
    await call.answer(f"Вы успешно приобрели {product_name}!")
    await bot.send_message(call.from_user.id, f"Вы успешно приобрели {product_name}!")

@dp.message_handler()
async def all_messages(message: types.Message):
    await message.answer("Выберите опцию:")


if __name__ == '__main__':
    initialize_products()
    executor.start_polling(dp, skip_updates=True)


