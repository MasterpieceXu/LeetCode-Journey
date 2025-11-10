class Solution:
    def trap(self, height: List[int]) -> int:
        left=0
        right=len(height)-1
        left_max=height[left]
        right_max=height[right]
        totle_water=0
        while left<right:
            if left_max<right_max:
                left+=1
                water=left_max-height[left]
                if water>0:
                    totle_water+=water
                left_max=max(left_max,height[left])
            else:
                right-=1
                water = right_max - height[right]
                if water>0:
                    totle_water+=water
                right_max = max(right_max, height[right])
        return totle_water
