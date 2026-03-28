class MinStack:

    def __init__(self):
        self.stk = []
        self.minstk = []

    def push(self, val: int) -> None:
        self.stk.append(val)
        if not self.minstk or val <= self.minstk[-1]:
            self.minstk.append(val)
        else:
            self.minstk.append(self.minstk[-1])
    def pop(self) -> None:
        self.stk.pop()
        self.minstk.pop()
    
    def top(self) -> int:
        return self.stk[-1]

    def getMin(self) -> int:
        return self.minstk[-1]


# Your MinStack object will be instantiated and called as such:
# obj = MinStack()
# obj.push(val)
# obj.pop()
# param_3 = obj.top()
# param_4 = obj.getMin()