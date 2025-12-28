class Solution:
    def subarraySum(self, nums: List[int], k: int) -> int:
        n=len(nums)
        presum=[0]*(n+1)
        presum[0]=0
        count={0:1}
        res=0
        for i in range(n):
            presum[i]=presum[i-1]+nums[i]
            need=presum[i]-k
            if need in count:
                res+=count[need]
            if presum[i] not in count:
                count[presum[i]]=1
            else:
                count[presum[i]]+=1
        return res