class Solution:
    def subsetsWithDup(self, nums: List[int]) -> List[List[int]]:
        rs=set()
        def dfs(index,path):
            if index==len(nums):
                rs.add(tuple(sorted(path)))
                return
            dfs(index+1,path)
            dfs(index+1,path+[nums[index]])
        dfs(0,[])
        return [list(x) for x in rs]