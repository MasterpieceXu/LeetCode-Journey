class Solution:
    def combine(self, n: int, k: int) -> List[List[int]]:
        result=[]
        def dfs(i,path):
            if len(path)==k:
                result.append(path)
                return
            if i>n:
                return
            dfs(i+1,path+[i])
            dfs(i+1,path)
        dfs(1,[])
        return result
        
        