# Thread version of cooking 1 kitchen 1 chefs 1 dishes
import os
from time import time, ctime, sleep
import threading

def cooking(index):
    print(f'{ctime()} Kitchen–{index} : Begin cooking...PID {os.getpid()}')
    cooking_time = time()
    print(f'{ctime()} Kitchen–{index} : Begin cooking...')
    sleep(2)
    duration = time() - cooking_time
    print(f'{ctime()} Kitchen–{index} : Cooking done in {duration:0.2f} seconds!')

if __name__ == "__main__":
    # Begin of main thread
    print(f'{ctime()} Main : Starting cook.')
    start_time = time()
    print(f"{ctime()} Main : ID of main process: {os.getpid()}")

    # Multi thread cooking
    chefs = []
    for index in range(2):
        c = threading.Thread(target=cooking, args=(index,))
        chefs.append(c)
        c.start()

    for c in chefs:
        c.join()

    duration = time() - start_time
    print(f"{ctime()} Main : Finished Cooking duration in {duration:0.2f} seconds")
