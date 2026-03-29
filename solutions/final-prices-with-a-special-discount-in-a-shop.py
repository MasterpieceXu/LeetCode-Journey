class Solution:
    def finalPrices(self, prices: List[int]) -> List[int]:
        n = len(prices)
        res = [0] * n
        next_smaller_prices = self.next_smaller(prices) 
        for i in range(n):
            if next_smaller_prices[i] == -1:
                res[i] = prices[i]
            else:
                res[i] = prices[i] - next_smaller_prices[i]
        return res
    
    def next_smaller(self, nums):
        n = len(nums)
        res = [-1] * n 
        s = []
        for i in range(n-1, -1, -1):
            while s and s[-1] > nums[i]:
                s.pop()
            res[i] = -1 if not s else s[-1]
            s.append(nums[i])
        return res
