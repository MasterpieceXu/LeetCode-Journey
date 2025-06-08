class Solution:
    def removeElement(self, nums: List[int], val: int) -> int:
        slow=0
        for i in range(len(nums)):
            if nums[i]!=val:
                nums[slow]=nums[i]
                slow+=1
        return slow 