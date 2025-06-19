class Solution:
    def sortedSquares(self, nums: List[int]) -> List[int]:
        i=0
        k=len(nums)-1
        j=len(nums)-1
        result=[0]*len(nums)
        while i<=j:
            if nums[i]*nums[i]<nums[j]*nums[j]:
                result[k]=nums[j]*nums[j]
                j=j-1
                k=k-1
            else:
                result[k]=nums[i]*nums[i]
                i=i+1
                k=k-1
        return result