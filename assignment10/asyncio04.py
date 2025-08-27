import asyncio
import time
import random

# Customer: Producer
async def customer(name, queue):
    # สุ่มจำนวนสินค้า (1-5)
    items = [f"Item-{i}" for i in range(1, random.randint(2, 6))]

    # สุ่มเวลาที่ลูกค้ามาถึง (0-3 วินาที)
    await asyncio.sleep(random.uniform(0, 3))
    print(f"[{time.strftime('%X')}] [{name}] finished shopping: {items}")

    # รอถ้ามีการ block เพราะ queue เต็ม (maxsize=5)
    await queue.put((name, items))
    print(f"[{time.strftime('%X')}] [{name}] joined queue")

# Cashier: Consumer
async def cashier(name, queue, process_time):
    while True:
        customer_data = await queue.get()
        if customer_data is None:  # None = stop signal
            print(f"[{time.strftime('%X')}] [{name}] closed")
            queue.task_done()
            break

        customer_name, items = customer_data
        print(f"[{time.strftime('%X')}] [{name}] processing {customer_name} with orders {items}")

        # เวลาประมวลผล = จำนวนสินค้า * process_time
        await asyncio.sleep(len(items) * process_time)

        print(f"[{time.strftime('%X')}] [{name}] finished {customer_name}")
        queue.task_done()

# Main
async def main():
    queue = asyncio.Queue(maxsize=5)  # จำกัดความจุสูงสุด 5

    # Cashiers
    cashier_tasks = [
        asyncio.create_task(cashier("Cashier-1", queue, 1)),  # 1 วินาที/สินค้า
        asyncio.create_task(cashier("Cashier-2", queue, 2)),  # 2 วินาที/สินค้า
    ]

    # Customers
    customer_tasks = [
        asyncio.create_task(customer(f"Customer-{i+1}", queue))
        for i in range(10)
    ]

    # รอให้ลูกค้าทุกคนเข้าคิวเสร็จ
    await asyncio.gather(*customer_tasks)

    # รอจนสินค้าทั้งหมดถูกคิดเงินเสร็จ
    await queue.join()

    # ส่งสัญญาณปิด cashier
    for _ in cashier_tasks:
        await queue.put(None)

    # รอ cashier หยุดทำงาน
    await asyncio.gather(*cashier_tasks)

    print(f"[{time.strftime('%X')}] [Main] Supermarket closed!")

if __name__ == "__main__":
    asyncio.run(main())
