import asyncio
import httpx

servers = [
    "http://172.20.50.30:8000",
    "http://172.20.49.15:8000",
    "http://172.20.49.87:8000",
]

ENDPOINTS = ["/students", "/analytics/group", "/analytics/year"]

async def fetch(client, url, endpoint):
    try:
        resp = await client.get(f"{url}{endpoint}", timeout=5.0)
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        return {"error": str(e)}

async def fetch_server_data(client, url):
    students, group, year = await asyncio.gather(
        fetch(client, url, "/students"),
        fetch(client, url, "/analytics/group"),
        fetch(client, url, "/analytics/year")
    )

    # แสดงผลแบบ readable
    if isinstance(students, list):
        print(f"{url} - student_count: {len(students)}")
    else:
        print(f"{url} - student_count: {students}")

    print(f"{url} - group_analytics: {group}")
    print(f"{url} - year_analytics: {year}")
    print("-" * 50)

async def main():
    async with httpx.AsyncClient() as client:
        tasks = [fetch_server_data(client, s) for s in servers]
        await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())
  
