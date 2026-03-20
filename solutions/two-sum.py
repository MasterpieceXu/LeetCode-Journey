class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        hash_map={}
        for i, nums in enumerate(nums):
            com=target-nums
            if com in hash_map:
                return [hash_map[com],i]
            hash_map[nums]=i