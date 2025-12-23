class Solution:
    def productExceptSelf(self, nums: List[int]) -> List[int]:
        n=len(nums)
        L,R,answer=[0]*n,[0]*n,[0]*n
        L[0]=1
        for i in range(1,n):
            L[i]=L[i-1]*nums[i-1]
        R[n-1]=1
        for i in range(n-2,-1,-1):
            R[i]=R[i+1]*nums[i+1]
        for i in range(n):
            answer[i]=L[i]*R[i]
        return answer