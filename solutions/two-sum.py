class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
      for i in range(len(nums)):
        add_number=target-nums[i]
        if add_number in nums and nums.index(add_number)!=i:
            return [i,nums.index(add_number)]
    
