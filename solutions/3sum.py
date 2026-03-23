class Solution:
    def threeSum(self, nums: list[int]) -> list[list[int]]:
        nums.sort()
        return self.nSumTarget(nums, 3, 0, 0)
    
    def nSumTarget (self, nums, n, start, target):
        #定义一个 n Sumtarget 的统一做法
        size = len(nums)
        res=[]
        if n < 2 or size < n:
            return res
        if n == 2:
            low  = start
            high = size - 1
            while low < high:
                sum_val = nums[low] + nums[high]
                left = nums[low]
                right = nums[high]                
                if sum_val < target:
                    while low < high and nums[low] == left:
                        low += 1
                elif sum_val > target:
                    while low < high and nums[high] == right:
                        high -= 1
                else:
                    res.append([left,right])
                    while low < high and nums[low] == left:
                        low += 1
                    while low < high and nums[high] == right:
                        high -= 1
        else:
            # n 大于 2 的时候，使用递归
            for i in range (start, size):
                if i > start and nums[i] == nums[i - 1]:
                    continue
                sub = self.nSumTarget(nums, n-1, i+1, target - nums[i])
                for arr in sub:
                    arr.append(nums[i])
                    res.append(arr)
        return res



    
