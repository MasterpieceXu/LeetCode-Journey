class Solution:
    def moveZeroes(self, nums: List[int]) -> None:
        """
        Do not return anything, modify nums in-place instead.
        """
        left_index=0
        for i in range(len(nums)):
            if nums[i]!=0:
                nums[left_index]=nums[i]
                left_index+=1
        for j in range(left_index,len(nums)):
            nums[j]=0
        return nums