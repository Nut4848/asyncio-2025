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
        return {
            "name": data["name"].title(),
            "id": data["id"],
            "base_experience": data["base_experience"]
        }

def get_experience(pokemon):
    return pokemon["name"]

async def main():
    tasks = [fetch_pokemon(name) for name in pokemon_names]
    results = await asyncio.gather(*tasks)

    sorted_results = sorted(results, key=get_experience)

    print(" Pokemon Sorted by Base Experience ")
    for p in sorted_results:
        print(f"Name: {p['name']:<12} > ID: {p['id']:>3} , Base XP: {p['base_experience']}")

asyncio.run(main())


