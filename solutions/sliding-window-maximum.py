class Solution:
    def maxSlidingWindow(self, nums: List[int], k: int) -> List[int]:
        window = windowdequeue()
        res = []
        for i in range(len(nums)):
            if i < k-1:
                window.push(nums[i])
            else:
                window.push(nums[i])
                res.append(window.max())
                window.pop(nums[i-k+1])
        return res
class windowdequeue:
    def __init__(self):
        self.maxdeuqe = []
    
    def push(self, n):
        while self.maxdeuqe and self.maxdeuqe[-1] < n:
            self.maxdeuqe.pop()
        self.maxdeuqe.append(n)
    def max(self):
        return self.maxdeuqe[0]
    
    def pop(self, n):
        if n == self.maxdeuqe[0]:
            self.maxdeuqe.pop(0)