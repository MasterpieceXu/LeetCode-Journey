class Solution:
    def romanToInt(self, s: str) -> int:
        Roman={'I':1,'V':5,'X':10,'L':50,'C':100,'D':500,'M':1000}
        totle=0
        for x,y in pairwise(s):
            x=Roman[x]
            y=Roman[y]
            if x>=y:
                totle+=x
            else:
                totle+=-x
        return totle+Roman[s[-1]] 