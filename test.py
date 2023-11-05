import copy
class Stack:
    def __init__(self):
        self.list = []
        self.list.append([])
        self.headIndex = -1
    
    def append(self, item):
        if self.headIndex < len(self.list) - 1:
            self.list = self.list[0:self.headIndex + 1]
        self.list.append(copy.deepcopy(item))
        self.headIndex += 1
    
    def peek(self):
        return self.list[self.headIndex]

    def pop(self):
        if self.headIndex >= 0:
            self.headIndex -= 1
        return self.list[self.headIndex + 1]
        
    def unpop(self):
        if self.headIndex < len(self.list) - 1:
            self.headIndex += 1
        return self.list[self.headIndex]
    
    def print(self):
        print("############# Stack Contents #################")
        for i in range(self.headIndex + 1):
            print(self.list[i])
        print("##############################################")

    
stk = Stack()

stk.append(1)
stk.print()
stk.append(2)
stk.print()
stk.append(3)
stk.print()
stk.append(4)
stk.print()
stk.append(5)
stk.print()
print(f"Pop: {stk.pop()}")
stk.print()
print(f"Pop: {stk.pop()}")
stk.print()
print(f"unPop: {stk.unpop()}")
stk.print()
stk.append(6)
stk.print()

