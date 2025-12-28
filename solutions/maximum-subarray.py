class Solution:
    def maxSubArray(self, nums: List[int]) -> int:
        n=len(nums)     
        current_sum=nums[0]
        max_sum=nums[0]
        for i in range (1,n):
            if current_sum<0:
                current_sum=nums[i]
            else:
                current_sum+=nums[i]
            max_sum=max(current_sum,max_sum)
        return max_sum



