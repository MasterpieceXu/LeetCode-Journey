class Solution:
    def findSubsequences(self, nums: List[int]) -> List[List[int]]:
        result=[]
        seen=set()
        def dfs(i, path):
            if i == len(nums):
                if len(path) >= 2:
                    t = tuple(path)
                    if t not in seen:
                        seen.add(t)
                        result.append(path[:])
                return
            if not path or nums[i] >= path[-1]:
                dfs(i + 1, path + [nums[i]])
            dfs(i+1,path)
        dfs(0,[])
        return result