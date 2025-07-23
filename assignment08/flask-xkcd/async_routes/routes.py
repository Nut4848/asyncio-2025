import asyncio
import random
import time
import httpx
from flask import Blueprint, render_template, current_app

async_bp = Blueprint("async", __name__)

async def get_xkcd(client, url):
    try:
        response = await client.get(url)
        response.raise_for_status()
        print(f"{time.ctime()} - get {url}")
        return response.json()
    except httpx.HTTPError as e:
        print(f"Failed to fetch {url}: {e}")
        return None

async def get_xkcds():
    NUMBER_OF_XKCD = current_app.config["NUMBER_OF_XKCD"]
    rand_list = [random.randint(0, 300) for _ in range(NUMBER_OF_XKCD)]

    xkcd_data = []
    async with httpx.AsyncClient() as client:
        tasks = []
        for number in rand_list:
            url = f'https://xkcd.com/{number}/info.0.json'
            tasks.append(get_xkcd(client, url))

        results = await asyncio.gather(*tasks)
        xkcd_data = [res for res in results if res]

    return xkcd_data

@async_bp.route('/')
async def home():
    start_time = time.perf_counter()
    xkcds = await get_xkcds()
    end_time = time.perf_counter()

    print(f"{time.ctime()} - Get {len(xkcds)} xkcd. Time taken: {end_time-start_time:.4f} seconds")

    return render_template('sync.html',  
                           title="XKCD Asynchronous Flask",
                           heading="XKCD Asynchronous Version",
                           xkcds=xkcds,
                           end_time=end_time,
                           start_time=start_time)
