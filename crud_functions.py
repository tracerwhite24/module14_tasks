import sqlite3

def db_connect():
    return sqlite3.connect('products.db')

def create_table():
    with db_connect() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT NOT NULL,
                price REAL NOT NULL,
                image_url TEXT NOT NULL
            )
        ''')
        conn.commit()
def add_product(title, description, price, image_url):
    try:
        with db_connect() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO products (title, description, price, image_url)
                VALUES (?, ?, ?, ?)
            ''', (title, description, price, image_url))
            conn.commit()
    except Exception as e:
        print(f"An error occurred: {e}")

def get_all_products_from_db():
    try:
        with db_connect() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT title, description, price, image_url FROM products')
            products = cursor.fetchall()
            return [{'title': title, 'description': description, 'price': price, 'image_url': image_url} for title, description, price, image_url in products]
    except Exception as e:
        print(f"An error occurred: {e}")
        return []

create_table()

