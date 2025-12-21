class Solution:
    def setZeroes(self, matrix: List[List[int]]) -> None:
        """
        Do not return anything, modify matrix in-place instead.
        """
        m=len(matrix)
        n=len(matrix[0])
        row_has_zero=any(matrix[0][j]==0 for j in range(n))
        col_has_zero=any(matrix[i][0]==0 for i in range(m))
        for i  in range (1,m):
            for j in range(1,n):
                if matrix[i][j]==0:
                    matrix[i][0]=0
                    matrix[0][j]=0
        for i in range(1,m):
            for j in range(1,n):
                if matrix[i][0]==0 or matrix[0][j]==0:
                    matrix[i][j]=0
        
        if row_has_zero:
            for j in range (n):
                matrix[0][j]=0

        if col_has_zero:
            for i in range(m):
                matrix[i][0]=0

