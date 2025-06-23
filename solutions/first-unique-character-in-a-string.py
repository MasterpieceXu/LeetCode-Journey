class Solution:
    def firstUniqChar(self, s: str) -> int:
        dic={}
        for i in s:
            if i in dic:
                dic[i]+=1
            else:
                dic[i]=1
        for i,c in enumerate(s):
            if dic[c]==1:
                return i 
        return  -1
