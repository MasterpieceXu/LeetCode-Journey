class Solution:
    def maxArea(self, height: List[int]) -> int:
        left=0
        right=len(height)-1
        max_water=0
        while left<right:
            width=right-left
            hei=min(height[left],height[right])
            current_water=width*hei
            max_water=max(current_water,max_water)
            if height[left]<height[right]:
                left+=1
            else:
                right-=1
        return max_water

        
