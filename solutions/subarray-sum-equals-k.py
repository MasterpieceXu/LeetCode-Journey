class Solution:
    def subarraySum(self, nums: List[int], k: int) -> int:
        precount=defaultdict(int)
        precount[0]=1
        presum=0
        count=0
        for num in nums:
            presum+=num
            target=presum-k
            count+=precount.get(target,0)
            precount[presum]+=1
        return count