class Solution:
    def longestConsecutive(self, nums: List[int]) -> int:
        S=set(nums)
        longest_streak=0
        for nums in S:
            if nums-1 not in S:
                current_num=nums
                current_streak=1
                while current_num+1 in S:
                    current_num+=1
                    current_streak+=1
                
                longest_streak=max(longest_streak,current_streak)
        
        return longest_streak