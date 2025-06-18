# Multiprocessing 2 kitkens, 2 cooker, 2 dishes
# Multiprocessing 2 kitchens, 2 cookers, 2 dishes
import multiprocessing
import os
from time import sleep, ctime, time

def cooking(index):
    cooking_time = time()
    print(f"{ctime()} Kitchen–{index} : Begin cooking...PID {os.getpid()}")
    sleep(2)
    duration = time() - cooking_time
    print(f"{ctime()} Kitchen–{index} : Cooking done in {duration:0.2f} seconds!")

def kitchen(index):
    cooking(index)

if __name__ == "__main__":
    print(f"{ctime()} Main : Start Cooking...PID {os.getpid()}")
    start_time = time()

    # Multi kitchens with each chef
    kitchens = []
    for index in range(100):
        p = multiprocessing.Process(target=kitchen, args=(index,))
        kitchens.append(p)
        p.start()

    for p in kitchens:
        p.join()

    duration = time() - start_time
    print(f"{ctime()} Main : Finished Cooking duration in {duration:0.2f} seconds")
