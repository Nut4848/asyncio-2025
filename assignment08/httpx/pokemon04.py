import httpx
import asyncio

pokemon_names = [
    "pikachu", "rayquaza", "charizard", "greninja",
    "eevee", "snorlax", "zekrom", "mewtwo", "groudon", "zoroark"
]

async def fetch_pokemon(name):
    url = f"https://pokeapi.co/api/v2/pokemon/{name}"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        data = response.json()
        pokemon_id = data["id"]
        types = [t["type"]["name"] for t in data["types"]]
        print(f"{name.title()} > ID: {pokemon_id}, Types: {types}")

async def main():
    tasks = [fetch_pokemon(name) for name in pokemon_names]
    await asyncio.gather(*tasks)

asyncio.run(main())