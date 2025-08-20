import asyncio
import random
import matplotlib.pyplot as plt

# จำนวนตัวแทนในฝูง
N_AGENTS = 10
# จำนวนก้าวสูงสุดที่แต่ละตัวแทนสามารถเดินได้
N_STEPS = 200

# ตำแหน่งเป้าหมายแบบสุ่มในกริด (-20 ถึง 20)
TARGET = (random.randint(-20, 20), random.randint(-20, 20))

# เก็บร่องรอยการเดินของแต่ละตัวแทน
traces = {i: [(0, 0)] for i in range(N_AGENTS)}
# เก็บข้อมูลว่าตัวแทนใดพบเป้าหมายและในก้าวที่เท่าไร
found_by = {}

# ตัวแปรบอกว่าเป้าหมายถูกพบแล้วหรือยัง
target_found = False

async def explore(agent_id: int):
    """
    แต่ละตัวแทนจะเดินแบบสุ่มจนกว่าจะพบเป้าหมาย
    หรือมีตัวแทนอื่นพบเป้าหมายก่อน
    """
    global target_found
    x, y = traces[agent_id][0]  # จุดเริ่มต้น
    for step in range(1, N_STEPS + 1):
        if target_found:
            break

        # เดินแบบสุ่ม: ไปหนึ่งก้าวในทิศทางใดทิศทางหนึ่ง
        dx, dy = random.choice([(1, 0), (-1, 0), (0, 1), (0, -1)])
        x, y = x + dx, y + dy
        traces[agent_id].append((x, y))

        # ตรวจสอบว่าพบเป้าหมายหรือไม่
        if (x, y) == TARGET:
            found_by[agent_id] = step
            target_found = True
            print(f"Agent {agent_id} found the target at step {step}")
            break

        await asyncio.sleep(0.01)

async def main():
    print(f"Random target location: {TARGET}")
    tasks = [asyncio.create_task(explore(i)) for i in range(N_AGENTS)]
    await asyncio.gather(*tasks)

    # แสดงเส้นทางของแต่ละตัวแทน
    for agent_id, path in traces.items():
        xs, ys = zip(*path)
        plt.plot(xs, ys, marker=".", alpha=0.6, label=f"Agent {agent_id}")

    # แสดงตำแหน่งเป้าหมาย
    plt.scatter(*TARGET, c="red", s=100, marker="X", label="Target")
    plt.title("Swarm Exploration (Stop All on Target Found)")
    plt.legend()
    plt.grid(True)
    plt.show()

    # แสดงผลว่าใครพบเป้าหมาย
    if found_by:
        print("Target found by:")
        for agent, step in found_by.items():
            print(f" Agent {agent} at step {step}")
    else:
        print("No agent found the target.")

# เรียกใช้งานโปรแกรมหลัก
if __name__ == "__main__":
    asyncio.run(main())