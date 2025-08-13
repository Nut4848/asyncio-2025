import asyncio
import time
import random

async def save_to_db(sensor_id, value):
    await asyncio.sleep(1)  # จำลองการเขียน DB
    print(f"{time.ctime()} Saved {sensor_id} = {value}")

async def main():
    tasks = []  # เก็บ Task ไว้
    for sensor_id in range(5):
        value = random.randint(50, 100)
        print(f"{time.ctime()} Sensor {sensor_id} got value: {value}")
        task = asyncio.create_task(save_to_db(sensor_id, value))
        tasks.append(task)

    # ✅ รอให้ทุก Task เสร็จก่อนจบ
    await asyncio.gather(*tasks)

asyncio.run(main())
