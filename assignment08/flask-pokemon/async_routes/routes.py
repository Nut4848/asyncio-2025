import asyncio
import random
import time
import httpx
from flask import Blueprint, render_template, current_app

async_bp = Blueprint("async", __name__)

async def fetch_pokemon(client, poke_id):
    url = f"https://pokeapi.co/api/v2/pokemon/{poke_id}"
    try:
        response = await client.get(url)
        response.raise_for_status()
        print(f"{time.ctime()} - get {url}")
        return response.json()
    except httpx.HTTPError as e:
        print(f"Failed to fetch Pokémon {poke_id}: {e}")
        return None

@async_bp.route('/')
async def home():
    start_time = time.perf_counter()
    number = current_app.config.get("NUMBER_OF_XKCD", 30)
    rand_ids = random.sample(range(1, 152), number)

    async with httpx.AsyncClient() as client:
        tasks = [fetch_pokemon(client, pid) for pid in rand_ids]
        results = await asyncio.gather(*tasks)

    pokemons = [poke for poke in results if poke]

    end_time = time.perf_counter()

    return render_template("sync.html",  
                           title="Pokemon Flask Async",
                           heading="Pokemon Flask Asynchronous Version",
                           pokemons=pokemons,
                           start_time=start_time,
                           end_time=end_time)
