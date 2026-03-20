class Solution:
    def longestConsecutive(self, nums: List[int]) -> int:
        set_nums=set(nums)
        res=0
        for num in set(nums):
            if num-1 in set_nums:
                continue
            curr_num=num
            curr_len=1
            while curr_num+1 in set_nums:
                curr_num+=1
                curr_len+=1
            res=max(res,curr_len)
        return res