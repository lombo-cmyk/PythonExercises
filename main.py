import random
import threading

class Queue:
    queue = list()
    max_queue_length =0


class Producer:
    def __init__(self, passed_no_arrays):
        self.no_arrays = passed_no_arrays


    def add_elements(self, mutex):
        i=0
        while True:
            if len(Queue.queue) < Queue.max_queue_length:
                random_array = self.generate_random_array(20);
                with mutex:
                    Queue.queue.append(random_array)
                i=i+1
                if i == self.no_arrays:
                    break
            else:
                pass

    @staticmethod
    def generate_random_array(ARR_SIZE):
        random_array=list()
        for i in range (0, ARR_SIZE):
            random_array.append(random.randrange(-10000,10000,1))
        print("Producer: ", random_array)
        return  random_array

class Consumer:
    @classmethod
    def sort_array(self, mutex):
        while len(Queue.queue) > 0:
            with mutex:
                my_copy = Queue.queue.pop(0)
            my_copy.sort()
            with mutex:
                print("Consumer: ", my_copy)


myMutex = threading.Lock()
Queue.max_queue_length=2
myProducer=Producer(2)
#myProducer.add_elements()
watek = threading.Thread(target=myProducer.add_elements, args=(myMutex,))
watekconsumer = threading.Thread(target=Consumer.sort_array,args=(myMutex,))
watek.start()
watekconsumer.start()
with myMutex:
    print("Kolejka:", Queue.queue)

watek.join()
watekconsumer.join()

print("Kolejka2: ", Queue.queue)