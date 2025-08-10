class Solution:
    def largeGroupPositions(self, s: str) -> List[List[int]]:
        if len(s)<3:
            return []
        R=[]
        start=0
        for i in range(1,len(s)+1):
                if i==len(s) or s[i]!=s[i-1]:
                    if i-start>=3:
                        R.append([start,i-1])
                    start=i
        return R


