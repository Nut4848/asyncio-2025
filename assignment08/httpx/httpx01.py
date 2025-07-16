import asyncio
import httpx

async def main():
    async with httpx.AsyncClient() as client:
        response = await client.get("https://www.example.com")
        print(response.status_code)
        print(response.text[:100])
        
asyncio.run(main())        
        