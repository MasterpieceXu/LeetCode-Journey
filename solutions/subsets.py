class Solution:
    def subsets(self, nums: List[int]) -> List[List[int]]:
        rs=[]
        def dfs(index,path):
            if index==len(nums):
                rs.append(path)
                return
            #not choose
            dfs(index+1,path)
            #choose
            # if nums[index] not in path:
            dfs(index+1,path+[nums[index]])
        
        dfs(0,[])
        return rs