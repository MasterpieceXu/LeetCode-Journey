class Solution:
    def spiralOrder(self, matrix: List[List[int]]) -> List[int]:
        m=len(matrix)
        n=len(matrix[0])
        upper_bond, lower_bond=0,m-1
        left_bond, right_bond=0,n-1
        res=[]
        while len(res)<m * n:
            if upper_bond<=lower_bond:
                for j in range(left_bond,right_bond+1):
                    res.append(matrix[upper_bond][j])
                upper_bond+=1
            if left_bond<=right_bond:
                for i in range(upper_bond,lower_bond+1):
                    res.append(matrix[i][right_bond])
                right_bond-=1
            if upper_bond<=lower_bond:
                for j in range(right_bond,left_bond-1,-1):
                    res.append(matrix[lower_bond][j])
                lower_bond-=1
            if left_bond<=right_bond:
                for i in range(lower_bond,upper_bond-1,-1):
                    res.append(matrix[i][left_bond])
                left_bond+=1
        return res