import time
import random
import httpx
from flask import Blueprint, render_template, current_app

sync_bp = Blueprint("sync", __name__)

def get_pokemon(poke_id):
    url = f"https://pokeapi.co/api/v2/pokemon/{poke_id}"
    response = httpx.get(url)
    print(f"{time.ctime()} - get {url}")
    return response.json()

def get_pokemons():
    num = current_app.config.get("NUMBER_OF_XKCD", 30)
    rand_ids = [random.randint(1, 151) for _ in range(num)]

    pokemons = []
    for pid in rand_ids:
        try:
            data = get_pokemon(pid)
            pokemons.append(data)  
        except Exception as e:
            print(f"Failed to load Pokémon {pid}: {e}")
            continue

    return pokemons

@sync_bp.route('/')
def home():
    start_time = time.perf_counter()
    pokemons = get_pokemons()
    end_time = time.perf_counter()

    return render_template("sync.html",
                           title="Pokemon Flask Sync",
                           heading="Pokemon Flask Synchronous Version",
                           pokemons=pokemons,
                           start_time=start_time,
                           end_time=end_time)
