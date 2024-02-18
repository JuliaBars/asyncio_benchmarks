import asyncio

import asyncpg


async def main():
    """Connection to db"""
    connection = await asyncpg.connect(
        host='127.0.0.1',
        port=5432,
        user='postgres',
        database='postgres',
        password='postgres',
    )
    version = connection.get_server_version()
    print(f'Подключено! Версия Postgres равна {version}')
    await connection.close()


asyncio.run(main())
