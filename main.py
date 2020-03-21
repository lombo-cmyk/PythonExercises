import random
import threading
from time import sleep
import secrets
class Queue:
    queue = list()
    max_queue_length = 0


class Producer:
    def __init__(self, passed_no_arrays):
        self.no_arrays = passed_no_arrays

    def add_elements(self, mutex, print_mutex):
        i=0
        sleep(2)
        while True:
            #print("producent")
            if len(Queue.queue) < Queue.max_queue_length:
                random_array = self.generate_random_array(1000);
                #with print_mutex:
                    #print("Producent: ", random_array)
                with mutex:
                    Queue.queue.append(random_array)
                    condition_variable.notify()
                i=i+1
                if i == self.no_arrays:
                    break
            else:
                with producer_mutex:
                    if not producer_cv.wait(timeout=1):
                        break

    @staticmethod
    def generate_random_array(ARR_SIZE):
        random_array=list()
        for i in range (0, ARR_SIZE):
            random_number=secrets.randbelow(10000)
            if secrets.randbelow(100) % 2 == 1:
                random_number=-random_number
            random_array.append(random_number)

        return  random_array

class Consumer:
    def __init__(self):
        self.no_consumer_arrays = 0

    def sort_array(self, mutex, print_mutex):
        checksum = 0
        while True:
            mutex.acquire()
            if len(Queue.queue) > 0:
                my_copy = Queue.queue.pop(0)
                mutex.release()
                with producer_mutex:
                    producer_cv.notify()
                my_copy.sort()
                self.no_consumer_arrays += 1
                with print_mutex:
                    print("Consumer: ", self.calculate_checksum(my_copy))
            else:
                mutex.release()
                with mutex:
                    if not condition_variable.wait(timeout=5):
                        with print_mutex:
                            print("I consumed: ", self.no_consumer_arrays, "arrays")
                        break
    @staticmethod
    def calculate_checksum(my_list):
        sum = 0
        for number in my_list:
            sum=sum+number
        return sum/len(my_list)


myMutex = threading.Lock()
print_mutex = threading.Lock()
producer_mutex = threading.Lock()
condition_variable = threading.Condition(myMutex)
producer_cv = threading.Condition(producer_mutex)
Queue.max_queue_length=200
no_arrays_to_produce=4000
myProducer=Producer(no_arrays_to_produce)
#myProducer.add_elements()
watek = threading.Thread(target=myProducer.add_elements, args=(myMutex, print_mutex,))
my_consumer = list()
consumer_thread= list()
for i in range(5):
    my_consumer.append(Consumer())
    consumer_thread.append(threading.Thread(target=my_consumer[i].sort_array, args=(myMutex,print_mutex,) ) )
watek.start()
for consumer in consumer_thread:
    consumer.start()
watek.join()
for consumer in consumer_thread:
    consumer.join()

print("Kolejka2: ", Queue.queue)