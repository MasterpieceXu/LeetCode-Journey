class Solution:
    def sortedSquares(self, nums: List[int]) -> List[int]:
        nums2=[i**2 for i  in nums]
        return sorted(nums2)
        