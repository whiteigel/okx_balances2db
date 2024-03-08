import ccxt
import psycopg2
from secret import *
from config import *

# Установка соединения с базой данных
conn = psycopg2.connect(
    dbname=DB_NAME,
    user=DB_USER,
    password=DB_PASSWORD,
    host=DB_HOST,
    port=DB_PORT
)

cur = conn.cursor()

# Получение балансов с биржи OKX
okx = ccxt.okx({
    'apiKey': API_KEY,
    'secret': SECRET,
    'password': PASSWORD,
})
balances = okx.fetch_balance(params={'type': 'funding'})

# Получение текущей даты и времени
from datetime import datetime
transaction_date = datetime.now()

# Запись полученных данных в таблицу
eth_balance = balances['total'].get('ETH')
usdt_balance = balances['total'].get('USDT')
usdc_balance = balances['total'].get('USDC')

# Вывод балансов в консоль
print("Balances from OKX exchange:")
print(f"ETH Balance: {eth_balance}")
print(f"USDT Balance: {usdt_balance}")
print(f"USDC Balance: {usdc_balance}")

# Запись в базу данных
cur.execute("""
    INSERT INTO okx (eth_balance, usdt_balance, usdc_balance, transaction_date)
    VALUES (%s, %s, %s, %s)
""", (eth_balance, usdt_balance, usdc_balance, transaction_date))
conn.commit()

# Закрытие соединения с базой данных
cur.close()
conn.close()
