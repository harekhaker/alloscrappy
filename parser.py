import asyncio
import json
import aiohttp
from aiohttp import ClientSession
from db_manager import sess, AlloTips, Query, Product, Category, get_or_create
from tips_generator import create_tips

URL = "https://allo.ua/ua/catalogsearch/ajax/suggest/"



async def response_process(tip_object, response):
    if response.status == 200:
        resp = json.loads(await response.text())

        if type(resp) == dict:

            queries = resp.get("query")
            products = resp.get("products")
            categories = resp.get("categories")

            if queries:
                for query in queries:
                    tip_object.queries.append(get_or_create(Query, {"query": query}))

            if products:
                for product in products:
                    tip_object.products.append(get_or_create(Product, product))

            if categories:
                for category in categories:
                    tip_object.categories.append(get_or_create(Category, category))

            tip_object.processed = True

            sess.commit()

async def fetch(url, tip_object, session):

    try:
        async with session.post(url, data={"q": tip_object.request}) as response:

            await response_process(tip_object, response)

        # return await response.read()

    except (aiohttp.client_exceptions.ClientConnectorError, asyncio.TimeoutError):
        pass


async def bound_fetch(sem, data, url, session):
    # Getter function with semaphore.
    async with sem:
        await fetch(url, data, session)


async def run():
    tasks = []
    # create instance of Semaphore
    sem = asyncio.Semaphore(1000)

    # Create client session that will ensure we dont open new connection
    # per each request.

    async with ClientSession() as session:
        for tip_object in sess.query(AlloTips).filter(AlloTips.processed.is_(False)).all():
            # pass Semaphore and session to every GET request
            task = asyncio.ensure_future(bound_fetch(sem, tip_object, URL, session))
            tasks.append(task)

        responses = asyncio.gather(*tasks)
        await responses


create_tips()
loop = asyncio.get_event_loop()
future = asyncio.ensure_future(run())
loop.run_until_complete(future)
loop.close()
