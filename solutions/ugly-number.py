class Solution:
    def isUgly(self, n: int) -> bool:
        if n<=0:
            return False
        x,i=n,2
        while i*i<=n:
            if x%i==0:
                if i not in(2,3,5):
                    return False
                while x%i==0:
                    x//=i
            i+=1
        if x>1 and x not in(2,3,5):
            return False
        return True
            

                    
                    
