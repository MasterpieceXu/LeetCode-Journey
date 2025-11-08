class Solution:
    def removeDuplicates(self, nums: List[int]) -> int:
        slow=0
        for fast in range(len(nums)):
            if fast==0 or fast==1:
                nums[slow]=nums[fast]
                slow+=1
            else:
                if nums[fast]!=nums[slow-2]:
                    nums[slow]=nums[fast]
                    slow+=1
        return slow
    
