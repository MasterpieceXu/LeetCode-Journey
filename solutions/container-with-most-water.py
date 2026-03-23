class Solution:
    def maxArea(self, height: List[int]) -> int:
        n = len(height)
        if n == 0:
            return 0
        left = 0
        right = n-1
        res = 0
        while left <= right:
            curr_area = (right-left) * min(height[right], height[left])
            res = max(res, curr_area)
            if height[left] <= height[right]:
                left += 1
            else:
                right -= 1
        return res