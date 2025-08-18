class Solution:
    def getRow(self, rowIndex: int) -> List[int]:
        r=[]
        for i in range(rowIndex+1):
            r.append(math.comb(rowIndex,i))
        return r
