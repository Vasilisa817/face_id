import time
import multiprocessing as mp

def generate(x):
    for j in range(x, x + 10):
        yield j
        time.sleep(1)

def init_queue(queue):
    globals()['queue'] = queue


def wrapper():
    q = queue
    for item in generate(10):
        q.put(item)


if __name__ == '__main__':

    POISON = 'POISON'

    queue = mp.SimpleQueue()

    with mp.Pool(processes=1, initializer=init_queue, initargs=(queue,)) as pool:
        pool.map_async(
            func=wrapper,
            iterable=range(0, 100, 10),
            chunksize=1,
            callback=lambda _: queue.put(POISON)
        )
        for res in iter(queue.get, POISON):
            print(res)