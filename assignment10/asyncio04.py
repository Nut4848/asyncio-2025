import asyncio
import time
import random

customer_names = [
    "Alice", "Bob", "Charlie", "David", "Eva",
    "Frank", "Grace", "Hannah", "Ivan", "Julia"
]

product_list = [
    "Apple", "Banana", "Milk", "Bread", "Cheese",
    "Eggs", "Juice", "Butter", "Rice", "Chicken"
]

# Customer
async def customer(name, queue):
    items = random.sample(product_list, random.randint(1, 5))
    await asyncio.sleep(random.uniform(0, 3))
    print(f"[{time.strftime('%c')}] [{name}] finished shopping: {items}")
    await queue.put((name, items))
    print(f"[{time.strftime('%c')}] [{name}] joined queue")

# Cashier
async def cashier(name, queue, process_time):
    while True:
        customer_data = await queue.get()
        if customer_data is None:
            print(f"[{time.strftime('%c')}] [{name}] closed")
            queue.task_done()
            break

        customer_name, items = customer_data
        print(f"[{time.strftime('%c')}] [{name}] processing {customer_name} with orders {items}")
        await asyncio.sleep(len(items) * process_time)
        print(f"[{time.strftime('%c')}] [{name}] finished {customer_name}")
        queue.task_done()

# Main
async def main():
    queue = asyncio.Queue(maxsize=5)
    cashier_tasks = [
        asyncio.create_task(cashier("Cashier-1", queue, 1)),
        asyncio.create_task(cashier("Cashier-2", queue, 2)),
    ]
    customer_tasks = [
        asyncio.create_task(customer(name, queue))
        for name in customer_names
    ]
    await asyncio.gather(*customer_tasks)
    await queue.join()
    for _ in cashier_tasks:
        await queue.put(None)
    await asyncio.gather(*cashier_tasks)
    print(f"[{time.strftime('%c')}] [Main] Supermarket closed!")

if __name__ == "__main__":
    asyncio.run(main())

