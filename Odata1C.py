import aiohttp
import asyncio
from aiohttp import BasicAuth


async def fetch_half_fabricates():
    url = 'http://s1.serverss.ru/unf01/odata/standard.odata/Document_ИнвентаризацияЗапасов_СС_Полуфабрикаты?$format=json'
    auth = BasicAuth('odata.user', 'ss24102023')

    async with aiohttp.ClientSession() as session:
        async with session.get(url, auth=auth) as res:
            if res.status == 200:
                data = await res.json()
                half_fabricates = data.get('value', [])
                return half_fabricates
            else:
                print(f"Ошибка: {res.status}, {await res.text()}")
                return []

async def main():
    half_fabricates = await fetch_half_fabricates()
    print("Полуфабрикаты:", half_fabricates)

asyncio.run(main())