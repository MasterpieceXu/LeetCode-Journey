class Solution:
    def minSubArrayLen(self, target: int, nums: List[int]) -> int:
        result=len(nums)
        i=0
        sum_nums=0
        if sum(nums)<target:
            return 0
        for j in range(len(nums)):
            sum_nums+=nums[j]
            while sum_nums>=target:
                answer=j-i+1
                result=min(result,answer)
                sum_nums=sum_nums-nums[i]
                i+=1
            j+1
        return result