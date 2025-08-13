class Solution:
    def distinctPrimeFactors(self, nums: List[int]) -> int:
        reserve_ans=set()
        result=1
        for i in nums:
            result=i*result
        n=2
        while result>1:
            if result%n==0:
                reserve_ans.add(n)
                result=result//n
            else:
                n+=1
        return len(reserve_ans)