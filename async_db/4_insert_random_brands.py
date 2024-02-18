import asyncio
from random import sample

import asyncpg


def load_common_words() -> list[str]:
    with open('common_words.txt', encoding='utf8') as common_words:
        return common_words.readlines()


def generate_brand_names(words: list[str]) -> list[tuple[str]]:
    return [(words[index],) for index in sample(range(100), 100)]


async def insert_brands(common_words, connection) -> int:
    brands = generate_brand_names(common_words)
    insert_command = "INSERT INTO brand VALUES(DEFAULT, $1)"
    return await connection.executemany(insert_command, brands)


async def main():
    common_words = load_common_words()
    connection = await asyncpg.connect(
        host='127.0.0.1',
        port=5432,
        user='postgres',
        database='products',
        password='postgres'
    )
    await insert_brands(common_words, connection)
    print('Вставка завершена')


asyncio.run(main())
