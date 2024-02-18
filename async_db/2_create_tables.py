import asyncio

import asyncpg

from async_db.commands import *


async def main():
    connection = await asyncpg.connect(
        host='127.0.0.1',
        port=5432,
        user='postgres',
        database='products',
        password='postgres'
    )

    statements = [
        CREATE_BRAND_TABLE,
        CREATE_PRODUCT_TABLE,
        CREATE_PRODUCT_COLOR_TABLE,
        CREATE_PRODUCT_SIZE_TABLE,
        CREATE_SKU_TABLE,
        SIZE_INSERT,
        COLOR_INSERT
    ]
    print('Создаются таблицы в базе данных products...')
    for statement in statements:
        status = await connection.execute(statement)
        print(status)
    print('Таблицы созданы!')
    await connection.close()


asyncio.run(main())
