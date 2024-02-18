import asyncio
import asyncpg


async def connect_create_if_not_exists(user, database):
    try:
        await asyncpg.connect(
            user=user,
            password='postgres',
            database=database
        )
        print(f'БД {database} уже существует')
    except asyncpg.InvalidCatalogNameError:
        sys_conn = await asyncpg.connect(
            host='127.0.0.1',
            port=5432,
            user='postgres',
            database='postgres',
            password='postgres',
        )
        await sys_conn.execute(
            f'CREATE DATABASE "{database}"'
        )
        await sys_conn.close()
        print(f'Бд {database} создана')


asyncio.run(
    connect_create_if_not_exists(user='postgres', database='products')
)
