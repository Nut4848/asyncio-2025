# Using a ThreadPoolExecutor
# Using a ThreadPoolExecutor
import concurrent.futures
import logging
import time

def thread_function(name):
    logging.info("Thread %s: starting", name)
    time.sleep(2)
    logging.info("Thread %s: finishing", name)

if __name__ == "__main__":
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")

    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        executor.map(thread_function, range(3))

# The code creates a ThreadPoolExecutor as a context manager, telling it how many
# worker threads it wants in the pool. It then uses .map() to step through an iterable
# of things, in your case range(3), passing each one to a thread in the pool.

# The end of the with block causes the ThreadPoolExecutor to do a .join() on each of
# the threads in the pool. It is strongly recommended that you use ThreadPoolExecutor
# as a context manager when you can so that you never forget to .join() the threads
