class Solution:
    def distinctPrimeFactors(self, nums: List[int]) -> int:
        reserve_ans=set()
        for i in nums:
            n=2
            while n*n<=i:
                if i%n==0:
                    reserve_ans.add(n)
                    i=i//n
                    while i%n==0:
                        i=i//n
                n+=1
            if i >1:
                reserve_ans.add(i)
        return len(reserve_ans)