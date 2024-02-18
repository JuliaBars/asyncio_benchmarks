import asyncio

import asyncpg
from asyncpg import Record


async def main():
    connection = await asyncpg.connect(
        host='127.0.0.1',
        port=5432,
        user='postgres',
        database='products',
        password='postgres')
    brand_query = 'SELECT product_id, product_name FROM product LIMIT 50'
    results: list[Record] = await connection.fetch(brand_query)
    for product in results:
        print(f'id: {product["product_id"]}, name: {product["product_name"]}')
    await connection.close()


asyncio.run(main())
