import asyncpg
import asyncio


class Database:
    def __init__(self):
        loop = asyncio.get_event_loop()
        self.pool = loop.run_until_complete(
            asyncpg.create_pool(
                user='op663246',
                database='neondb',
                password='5ELlvIaWx3JK',
                host='ep-empty-sea-524845.eu-central-1.aws.neon.tech',
                port='5432'
            )
        )

    async def register_user(self, first_name, last_name, username, telegram_id):
        sql = f"""
        INSERT INTO telegram_users (first_name, last_name, username, telegram_id) 
        VALUES ('{first_name}', '{last_name}', '{username}', '{telegram_id}')
        """
        await self.pool.execute(sql)

    async def check_user(self, telegram_id):
        sql = f"""
        SELECT * FROM telegram_users WHERE telegram_id = '{telegram_id}'
        """
        result = await self.pool.fetchrow(sql)
        return result
    
    async def insert_search_query(self, telegram_id, search_query):
        sql = f"""
        UPDATE telegram_users
        SET search_query = '{search_query}'
        WHERE telegram_id = '{telegram_id}'
        """
        await self.pool.execute(sql)
    async def save_dish_to_db(self, telegram_id, dish_name):
        sql = """
        INSERT INTO saved_dishes (telegram_id, dish_name)
        VALUES ($1, $2)
        """
        await self.pool.execute(sql, telegram_id, dish_name)
    async def get_saved_dishes_by_telegram_id(self, telegram_id):
        sql = """
        SELECT dish_name FROM saved_dishes
        WHERE telegram_id = $1
        """
        saved_dishes = await self.pool.fetch(sql, telegram_id)
        return [record['dish_name'] for record in saved_dishes]