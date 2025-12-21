class Solution:
    def maxSubArray(self, nums: List[int]) -> int:
        pre=0
        max_ans=nums[0]
        for num in nums:
            pre=max(pre+num,num)
            max_ans=max(max_ans,pre)
        
        return max_ans

