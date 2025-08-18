class Solution:
    def generate(self, numRows: int) -> List[List[int]]:
        Rs=[]
        for i in range(numRows):
            r=[]
            for j in range(i+1):
                r.append(math.comb(i,j))
            Rs.append(r)
        return Rs