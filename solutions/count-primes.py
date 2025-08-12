class Solution:
    def countPrimes(self, n: int) -> int:
        if n<=2:
            return 0
        is_prime=[True]*n
        is_prime[0]=is_prime[1]=False
        limit=isqrt(n)
        for i in range(2,limit+1):
            if is_prime[i]:
                start=i*i
                step=i
                count=(n-1-start)//i+1
                is_prime[start:n:step]=[False]*count
        return sum(is_prime)
