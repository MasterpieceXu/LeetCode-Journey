class Solution:
    def longestConsecutive(self, nums: List[int]) -> int:
        num_set=set(nums)
        max_lenth=0
        for num in num_set:
            if num-1 not in num_set:
                current_number=num
                current_lenth=1
                while current_number+1 in num_set:
                    current_number+=1
                    current_lenth+=1
                max_lenth=max(max_lenth,current_lenth)
        return max_lenth
                    
