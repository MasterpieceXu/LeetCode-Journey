class Solution:
    def numPrimeArrangements(self, n: int) -> int:
      def is_prime(x):
        if x<2:
          return False
        if x==2:
          return True
        if x%2==0:
          return False
        for i in range(3,isqrt(x)+1,2):
          if x%i==0:
            return False
        return True
      total=0
      for i in range(1,n+1):
        if is_prime(i) is True:
          total+=1
      combin=n-total
      answer1=math.perm(total,total)
      answer2=math.perm(combin,combin)
      mod=10**9+7
      return (answer1*answer2)%mod

          
        
