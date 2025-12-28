class Solution:
    def maxArea(self, height: List[int]) -> int:
        left=0
        right=len(height)-1
        max_area=0
        while left<right:
            width=right-left
            if height[left]<height[right]:
                current_height=height[left]
                left+=1
            else:
                current_height=height[right]
                right-=1
            current_area=width*current_height
            max_area=max(current_area,max_area)
        return max_area