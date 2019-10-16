"""
Create a Single Linked List using the OO principles thought in class. 
The Linked list should have the following:
- A START NODE and an END NODE which stores a single integer value
- Method to Append a New NODE to the END
- Method to Insert a New NODE after a given NODE in the list
- Method to Remove a given NODE from the list
"""

class NodeNotFoundException(Exception):
    pass
        

class Node:
    def __init__(self):
        self.__value = 0
        self.__NEXT = None

    @property
    def value(self):
        return self.__value
    
    @value.setter
    def value( self, x):
        self.__value = x

    @property
    def NEXT(self):
        return self.__NEXT
    
    @NEXT.setter
    def NEXT( self, x):
        if type(x) is Node:
            self.__NEXT = x
        else:
            raise TypeError("Invalid DataType provided for NEXT Pointer, needs to be of type Node")

    def __str__(self):
        return "{}".format(self.__value)



class LinkedList:

    def __init__ (self):
        self.__START = None
        self.__END = None
        self.__ITERATOR = None
        
    @property
    def START(self):
        return self.__START

    @property
    def END(self):
        return self.__END

    def __iter__(self):
        self._ITERATOR = self. __START
        return self
        
            
    def __next__(self):
        if self.__ITERATOR != None:
            node = self.__ITERATOR
            self.__ITERATOR = self.__ITERATOR.NEXT
            return node
        else:
            raise StopIteration

    def appendNode(self, node):
        # print(node)
        # print(type(node))
        if type(node) is not Node:
            raise TypeError("Invalid DataType provided for NEXT Pointer, needs to be of type Node")

        if self.__START is None:
            self.__START = node
            self.__END = node
            return

        self.__END.NEXT = node
        self.__END = node

        
    def insertAtBegining(self, node):
        if type(node) is not Node:
            raise TypeError("Invalid DataType provided for NEXT Pointer, needs to be of type Node")

        if self.__START is None:
            self.__START = node
            self.__END = node
            return

        node.NEXT = self.__START
        self.__START = node
        
    def insertAfter(self, targetNode, node):
        if type(node) is not Node:
            raise TypeError("Invalid DataType provided for NEXT Pointer, needs to be of type Node")
        if type(targetNode) is not Node:
            raise TypeError("Invalid DataType provided for targetNode, needs to be of type Node")
        if self.__START is None:
            raise NodeNotFoundException("The list is not initialized")
        
        traversingNode = self.__START
        found = False
        while traversingNode != None:
            if traversingNode is targetNode:
                #print("Found")
                found = True      
            if self.__END is targetNode:
                self.__END.NEXT = node
                self.__END = node 
                break          
            node.NEXT = targetNode.NEXT
            targetNode.NEXT = node
            break
        
        print(type(traversingNode.NEXT))
        traversingNode = traversingNode.NEXT
        if found is False:
            raise NodeNotFoundException("Not Found")




mylist = LinkedList()

node1 = Node()
node1.value = 1
node2 = Node()
node2.value = 2
node3 = Node()
node3.value = "hi"


mylist.appendNode(node1)
mylist.appendNode(node2)
mylist.appendNode(node3)


# node = mylist.START
# while  node != None :
#     print(node)
#     node = node.NEXT


node4 = Node()
node4.value = 4

# mylist.insertAtBegining(node4)
# node = mylist.START
# while  node != None :
#     print(node)
#     node = node.NEXT


node5 = Node()
node5.value = 1000

mylist.insertAfter(node1, node5)
node = mylist.START
while  node != None :
    print(node)
    node = node.NEXT





"""
for node in mylist:
    print(node.value)
myit = iter(mylist)
print(next(myit))
print(next(myit))
print(next(myit))
"""



















