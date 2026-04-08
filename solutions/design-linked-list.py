class Node:
    def __init__(self, val):
        self.val = val
        self.next = None
        self.prev = None

class MyLinkedList(object):
    def __init__(self):
        self.head = Node(None)
        self.tail = Node(None)
        self.tail.prev = self.head
        self.head.next = self.tail
        self.size = 0

    def get(self, index):
        """
        :type index: int
        :rtype: int
        """
        # 越界时按题意返回 -1
        if not self.is_element_index(index):
            return -1
        p = self.get_index(index)
        return p.val
    def addAtHead(self, val):
        """
        :type val: int
        :rtype: None
        """
        x = Node(val)
        temp = self.head.next
        temp.prev = x
        x.next = temp
        self.head.next = x
        x.prev = self.head
        self.size += 1

    def addAtTail(self, val):
        """
        :type val: int
        :rtype: None
        """
        x = Node(val)
        temp =  self.tail.prev
        temp.next = x
        x.prev = temp
        self.tail.prev = x
        x.next = self.tail
        self.size += 1

    def addAtIndex(self, index, val):
        """
        :type index: int
        :type val: int
        :rtype: None
        """
        # index <= 0: 在头部插入
        if index <= 0:
            self.addAtHead(val)
            return

        # index == size: 在尾部插入
        if index == self.size:
            self.addAtTail(val)
            return

        # 0 < index < size: 在中间插入；其它越界情况直接忽略
        if not self.is_element_index(index):
            return

        p = self.get_index(index)
        y = p.prev
        x = Node(val)
        x.next = p
        x.prev = y
        y.next = x
        p.prev = x
        self.size += 1

    def deleteAtIndex(self, index):
        """
        :type index: int
        :rtype: None
        """
        if not self.is_element_index(index):
            return
        p = self.get_index(index)
        temp1 = p.prev
        temp2 = p.next
        temp1.next = temp2
        temp2.prev = temp1
        p.next = None
        p.prev = None
        self.size -= 1

## 工具函数
    def is_empty(self):
        return self.size == 0
    
    def get_index(self, index):
        p = self.head.next
        for _ in range(index):
            p = p.next
        return p
    
    # 判断当前的索引是否有节点
    def is_element_index(self, index):
        return 0 <= index < self.size
    
    # 判断当前索引是否还可以接节点
    def is_position_element(self, index):
        return 0 <= index <= self.size

    def display(self):
        # 仅用于本地调试，不参与评测；避免使用 f-string 以兼容低版本解释器
        print("size = {}".format(self.size))
        p = self.head.next
        while p != self.tail:
            # Python2/3 都能跑的简单打印，不强求同一行输出
            print("{} <-> ".format(p.val))
            p = p.next
        print("null")
# Your MyLinkedList object will be instantiated and called as such:
# obj = MyLinkedList()
# param_1 = obj.get(index)
# obj.addAtHead(val)
# obj.addAtTail(val)
# obj.addAtIndex(index,val)
# obj.deleteAtIndex(index)