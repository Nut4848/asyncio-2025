import asyncio
import time
import random

async def save_to_db(sensor_id, value):
    await asyncio.sleep(random.uniform(0.5, 1.5))
    if value > 80:
        raise ValueError(f"[{sensor_id}] value too high!")
    return f"[{sensor_id}] saved value {value}"

def task_done_callback(task: asyncio.Task):
    try:
        result = task.result()  # ดึงผลลัพธ์ ถ้ามี error จะ raise ที่นี่
        print(f"{time.ctime()} / Task completed: {result}")
    except Exception as e:
        print(f"{time.ctime()} x Task failed: {e}")

async def handle_sensor(sensor_id):
    value = random.randint(50, 100)
    print(f"{time.ctime()} Sensor {sensor_id} got value: {value}")

    task = asyncio.create_task(save_to_db(sensor_id, value))
    task.add_done_callback(task_done_callback)  # เพิ่ม callback

async def main():
    for i in range(5):
        await handle_sensor(i)
    await asyncio.sleep(2)  # ให้เวลา task ทำงานเสร็จ

asyncio.run(main())
