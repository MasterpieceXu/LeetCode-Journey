class Solution:
    def groupAnagrams(self, strs: List[str]) -> List[List[str]]:
        Groupcode={}
        for s in strs:
            code=self.encode(s)
            if code not in Groupcode:
                Groupcode[code]=[]
            Groupcode[code].append(s)
        res=[]
        for group in Groupcode.values():
            res.append(group)
        
        return res
    def encode(self,s : str) -> str:
        count=[0]*26
        for c in s:
            delta=ord(c)-ord('a')
            count[delta]+=1
        return str(count)
            