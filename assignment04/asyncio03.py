# Create 2 Tasks with High-Level API
import asyncio

async def download_image(name, delay):
    print(f"{name} กำลังโหลด...")
    await asyncio.sleep(delay)
    print(f"{name} โหลดเสร็จแล้ว!")

async def main():
    # สร้าง 2 tasks พร้อมกัน
    task1 = asyncio.create_task(download_image("ภาพที่ 1", 2))
    task2 = asyncio.create_task(download_image("ภาพที่ 2", 3))

    # รอให้ทั้งสอง task เสร็จ
    await task1
    await task2

asyncio.run(main())

