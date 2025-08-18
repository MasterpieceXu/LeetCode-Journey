class Solution:
    def countPrimes(self, n: int) -> int:
        if n<=2:
            return 0
        prime=[False]+[False]+[True]*(n-2)
        for i in range(2,isqrt(n)+1):
            if prime[i]==True:
                for j in range(i**2,n,i):
                    prime[j]=False
        return sum(prime)