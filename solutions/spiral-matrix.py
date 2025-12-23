class Solution:
    def spiralOrder(self, matrix: List[List[int]]) -> List[int]:
        if not matrix:
            return []
        l,r,t,b=0,len(matrix[0])-1,0,len(matrix)-1
        res=[]
        while True:
            # 从左往右
            for i in range(l,r+1):
                res.append(matrix[t][i])
            t+=1
            if t > b: break
            # 从上往下
            for i in range(t,b+1):
                res.append(matrix[i][r])
            r-=1
            if l > r: break
            # 从右往左
            for i in range(r,l-1,-1):
                res.append(matrix[b][i])
            b-=1
            if b <t: break
            # 从下往上
            for i in range(b,t-1,-1):
                res.append(matrix[i][l])
            l+=1
            if l > r: break
        return res
