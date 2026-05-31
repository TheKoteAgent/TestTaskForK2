Simple ERP API
Тестове завдання. Мінімальна бекенд-частина ERP системи для управління клієнтами, товарами та замовленнями.
Написано на Flask + SQLAlchemy. База даних — SQLite.

Запуск проєкту
Клонувати репозиторій та перейти в папку проєкту.

Створити та активувати віртуальне середовище:
python -m venv .venv
source .venv/Scripts/activate

Встановити залежності:
pip install -r requirements.txt

Запустити сервер:
python app.py

Примітка: Файл бази даних (erp.db) разом з усіма таблицями згенерується автоматично при першому запуску.


API Ендпоінти

1. Клієнти
GET /api/clients — отримати список усіх клієнтів.
POST /api/clients/create — створити нового клієнта.
Body: {"name": "string", "phone": "string"}



2. Товари (Склад)
GET /api/products — список усіх товарів та їх залишків.
POST /api/product/create — додати товар на склад.
Body: {"product_name": "string", "product_amount": 10, "product_price": 100.0}



3. Замовлення
GET /api/orders — історія всіх замовлень.
GET /api/order/client/<client_id> — список замовлень конкретного клієнта.
POST /api/order/create — створення замовлення. Сума розраховується автоматично, а товари списуються зі складу.
Body (приклад):
{"client_id": 1, "items": [{"product_id": 1, "quantity": 2}, {"product_id": 2, "quantity": 1}]}