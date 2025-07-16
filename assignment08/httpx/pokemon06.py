import httpx
import asyncio

async def fetch_abilities():
    url = "https://pokeapi.co/api/v2/ability/?limit=20"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        data = response.json()
        return [entry["url"] for entry in data["results"]]
    
async def fetch_ability_detail(url):
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        data = response.json()
        name = data["name"]
        pokemon_count = len(data["pokemon"])  
        return name, pokemon_count

async def main():
    ability_urls = await fetch_abilities()
    tasks = [fetch_ability_detail(url) for url in ability_urls]
    results = await asyncio.gather(*tasks)
    
    print(" Pokemon Abilities Usage Count ")
    for name, count in results:
        print(f"{name} > {count} Pokemon")
        
asyncio.run(main())        
    
