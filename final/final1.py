"""
Program1
Write an Object Oriented Queue class that allows users to store different datatypes 
of information in it and access that data later on. The functionality of the Queue
should be on the basis of First in First out.
The following constraints should be met:
- Do not use any platform generic datatypes to design your Queue
- You need to implement the Queue like you did for the Single Linked List example and Stack
- The Queue should support the following constructs
    - append - allows the user to add an entry into the Queue
    - pop - allows the user to fetch an item from the Queue
    - Allow the user to iterate through the Queue one item at a time and display the elements in the order that they will be poped out
    - the Queue should support storing any datatype

Following psuedo code is expected to run
myQueue = Queue()
myQueue.add(1)
myQueue.add(2)
myQueue.add("hello")
for item in myQueue:
    print(item)
    # Expected output 1 2 hello
value = myQueue.pop()
print(value)
"""
class NodeNotFoundException(Exception):
    pass

class Node:
    def __init__(self, item):
        self.item = item
        self.next = None

    def __str__(self):
        return "{}".format(self.item)



class Queue:
    def __init__(self):
         self.head = None
         self.end = None

    def __iter__(self):
        self.__iterator = self.head
        return self

    def __next__(self):
        if self.__iterator != None:
            item = self.__iterator.item
            self.__iterator = self.__iterator.next
            return item
        else:
            raise StopIteration

    def add(self, item):
        temp = Node(item)
        if self.head is None:
            self.head = temp
            self.prev = temp
        else:   
            self.prev.next = temp
            self.prev = self.prev.next
                
    def pop(self):
        # temp = self.head
        # if self.head == None:
        #     raise NodeNotFoundException("Stack is Empty.")
        # while temp.next is not None:
        #     temp = temp.next
        # temp.next = None
        # return temp
        if self.head == None:
            raise NodeNotFoundException("Stack is Empty.")
        else:
            popped = self.head
            self.head = self.head.next
            return popped

myQueue = Queue()
myQueue.add(1)
myQueue.add(2)
myQueue.add("hello")
for item in myQueue:
    print(item)
    # Expected output 1 2 hello
value = myQueue.pop()
print(value) # the first input

