class Solution:
    def threeSum(self, nums: List[int]) -> List[List[int]]:
        n=len(nums)
        nums.sort()
        answer=[]
        for i in range(n):
            option=[]
            if nums[i] > 0:
                break
            if i>0  and nums[i] == nums[i-1]:
                continue
            left=i+1
            right=n-1
            while left<right:
                if nums[left]+nums[right]+nums[i]>0:
                    right-=1
                elif nums[left]+nums[right]+nums[i]<0:
                    left+=1
                else:
                    answer.append([nums[left],nums[right],nums[i]])
                    while left<right and nums[left]==nums[left+1]:
                        left+=1
                    while left<right and nums[right]==nums[right-1]:
                        right-=1
                    left+=1
                    right-=1
        return answer