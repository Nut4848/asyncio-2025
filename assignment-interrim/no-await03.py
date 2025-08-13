# โค้ดภาพที่สอง
import asyncio, time

async def worker_long():
    print(f"{time.ctime()} [worker_long] Start")
    try:
        await asyncio.sleep(5)  # speed long delay
        print(f"{time.ctime()} [worker_long] Done")
    except asyncio.CancelledError:
        print(f"{time.ctime()} worker_long] Cancelled!")  # task is cancelled

async def main():
    print(f"{time.ctime()} Start Main loop...")
    asyncio.create_task(worker_long())
    await asyncio.sleep(1)  # main loop finished before work_long()
    print(f"{time.ctime()} Main loop finished...!")

asyncio.run(main())
