import random
import threading
import time
import multiprocessing
import queue


class Producer:
    def __init__(self, passed_no_arrays):
        self.no_arrays = passed_no_arrays
        self.number_of_produced = 0
        self.arr_size = 10000      #TODO increasing arr_size spoils no consumed arrays
        self.random_array = list()

    def add_elements(self, my_queue, var_mutex, prod_mutex, cv_prod, cv_cons, printing_mutex):
        while True:
            if self.number_of_produced >= self.no_arrays:
                with printing_mutex:
                    print("Producent DONEEEWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWEEEE: ", self.number_of_produced)
                break

            self.generate_random_array();
            with var_mutex:
                if not my_queue.full():
                    # with printing_mutex:
                    #     print("Producent: ", self.random_array)
                    my_queue.put(self.random_array)
                    cv_cons.notify()
                    self.number_of_produced += 1
                else:
                    cv_cons.notify()
                #print("queue full ", self.number_of_produced," arrays ", "Im thread ", threading.get_ident())
                    with prod_mutex:
                        cv_prod.wait(timeout=2)


    def generate_random_array(self):
        self.random_array.clear()
        for i in range(0, self.arr_size):
            random_number = random.randint(-100000,100000)
            self.random_array.append(random_number)

class Consumer:
    def __init__(self):
        self.no_consumer_arrays = 0

    def sort_array(self, my_queue, var_mutex, prod_mutex, cv_prod, cv_cons, printing_mutex):
        checksum = 0
        my_copy = list()
        while True:
            with var_mutex:
                if not my_queue.empty():
                    my_copy = my_queue.get()
                    with prod_mutex:
                        cv_prod.notify()
            if len(my_copy) != 0:
                my_copy.sort()
                self.no_consumer_arrays += 1
                checksum = self.calculate_checksum(my_copy)
                my_copy.clear()
                # with printing_mutex:
                #     print("Consumer: ", checksum)
            else:
                #var_mutex.release()
                # with printing_mutex:
                #     print("queue empty")
                with cv_cons:
                    if not cv_cons.wait(timeout=2):
                        with print_mutex:
                           print("I consumed: ", self.no_consumer_arrays)
                        break
                # if self.no_consumer_arrays >= 15:
                #     break
    @staticmethod
    def calculate_checksum(my_list):
        sum = 0
        for number in my_list:
            sum=sum+number
        return sum/len(my_list)


basic_mutex = multiprocessing.Lock()
producer_mutex = multiprocessing.Lock()
print_mutex = multiprocessing.Lock()
consumer_cv = multiprocessing.Condition(basic_mutex)
producer_cv = multiprocessing.Condition(producer_mutex)
max_queue_length = 200
myQueue = multiprocessing.Queue(max_queue_length)
no_arrays_to_produce = 1000

start=time.clock_gettime(1)
my_producer = list()
producer_thread = list()
my_consumer = list()
consumer_thread = list()

if __name__ == '__main__':
    for i in range(1):
        my_producer.append(Producer(no_arrays_to_produce))
        producer_thread.append(multiprocessing.Process(target=my_producer[i].add_elements, args=(myQueue, basic_mutex, producer_mutex, producer_cv, consumer_cv, print_mutex,)))
    for i in range(4):
        my_consumer.append(Consumer())
        consumer_thread.append(multiprocessing.Process(target=my_consumer[i].sort_array, args=(myQueue, basic_mutex, producer_mutex, producer_cv, consumer_cv, print_mutex,)))
    for producer in producer_thread:
        producer.start()
    for consumer in consumer_thread:
        consumer.start()

    for producer in producer_thread:
        producer.join()
    for consumer in consumer_thread:
        consumer.join()

stop=time.clock_gettime(1)


print("czasjbjm ", stop-start)