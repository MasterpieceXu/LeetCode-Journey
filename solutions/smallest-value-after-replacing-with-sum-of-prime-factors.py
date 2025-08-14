class Solution:
    def smallestValue(self, n: int) -> int:
        while True:
            x,s,i=n,0,2
            while i*i<=x:
                while x%i==0:
                    s+=i
                    x//=i
                i+=1
            if x>1:
                s+=x
            if s==n:
                return n
            n=s
