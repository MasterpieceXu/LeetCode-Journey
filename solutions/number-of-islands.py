class Solution:
    def numIslands(self, grid: List[List[str]]) -> int:
        res=0
        m,n=len(grid),len(grid[0])
        for i in range(m):
            for j in range(n):
                if grid[i][j]=='1':
                    res+=1
                    self.dfs(grid,i,j)
        return res
    def dfs(self,grid,i,j):
        m,n=len(grid),len(grid[0])
        if i<0 or j<0 or i>=m or j>=n:
            return
        if grid[i][j]=='0':
            return 
        grid[i][j]='0'
        self.dfs(grid,i+1,j)
        self.dfs(grid,i-1,j)
        self.dfs(grid,i,j+1)
        self.dfs(grid,i,j-1)