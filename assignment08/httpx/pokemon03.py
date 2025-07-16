import httpx
import asyncio

async def fetch_pokemon():
    url = "https://pokeapi.co/api/v2/pokemon/pikachu"

    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        data = response.json()

        name = data['name'].title()
        pokemon_id = data['id']
        height = data['height']
        weight = data['weight']
        types = [t['type']['name'] for t in data['types']]

        print(f"Name: {name}")
        print(f"ID: {pokemon_id}")
        print(f"Height: {height}")
        print(f"Weight: {weight}")
        print(f"Types: {types}")

asyncio.run(fetch_pokemon())