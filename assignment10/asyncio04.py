import asyncio
import time
import random

# รายการสินค้า ของลูกค้าแต่ละคน
customers = {
    "Alice": ["Apple", "Banana", "Milk"],
    "Bob": ["Bread", "Cheese"],
    "Charlie": ["Eggs", "Juice", "Butter"]
}

# Producer: ลูกค้าเข้าคิว
async def customer(name, items, queue):
    print(f"[{time.strftime('%c')}] [{name}] finished shopping: {items}")
    await queue.put((name, items))  # ส่งงานเข้า queue

# Consumer: แคชเชียร์คิดเงิน
async def cashier(name, queue, process_time):
    while True:
        customer_data = await queue.get()
        if customer_data is None:  # None = สัญญาณหยุดทำงาน
            print(f"[{time.strftime('%c')}] [{name}] closed")
            queue.task_done()
            break

        customer_name, items = customer_data
        print(f"[{time.strftime('%c')}] [{name}] processing {customer_name} with orders {items}")
        
        # ใช้เวลาตามจำนวนสินค้า * process_time
        await asyncio.sleep(len(items) * process_time)

        print(f"[{time.strftime('%c')}] [{name}] finished {customer_name}")
        queue.task_done()  # ✅ บอกว่าเสร็จงานแล้ว

async def main():
    queue = asyncio.Queue()

    # สร้าง Cashier (Consumers)
    cashier_tasks = [
        asyncio.create_task(cashier("Cashier-1", queue, 1)),  # 1 วินาที/สินค้า
        asyncio.create_task(cashier("Cashier-2", queue, 2)),  # 2 วินาที/สินค้า
    ]

    # ✅ ให้ Alice เข้าคิวก่อนเสมอ
    alice_task = asyncio.create_task(customer("Alice", customers["Alice"], queue))

    # ✅ Bob และ Charlie เข้าคิวแบบสุ่มลำดับ
    others = ["Bob", "Charlie"]
    random.shuffle(others)

    other_tasks = [
        asyncio.create_task(customer(name, customers[name], queue))
        for name in others
    ]

    # รอให้ลูกค้าทุกคนเข้าคิวเสร็จ
    await asyncio.gather(alice_task, *other_tasks)

    # ✅ รอจนกว่าสินค้าทุกชิ้นจะถูกคิดเงินเสร็จ
    await queue.join()

    # ส่งสัญญาณปิดให้ cashier
    for _ in cashier_tasks:
        await queue.put(None)

    # รอให้ cashier หยุดทำงาน
    await asyncio.gather(*cashier_tasks)

    print(f"[{time.strftime('%c')}] [Main] Supermarket closed!")

if __name__ == "__main__":
    asyncio.run(main())
