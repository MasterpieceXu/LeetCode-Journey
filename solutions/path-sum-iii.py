# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def pathSum(self, root: Optional[TreeNode], targetSum: int) -> int:
        prix_map={0:1}
        def dfs(node,curr_sum):
            if not node:
                return 0
            curr_sum+=node.val
            res=prix_map.get(curr_sum-targetSum,0)
            prix_map[curr_sum]=prix_map.get(curr_sum,0)+1
            res+=dfs(node.left,curr_sum)
            res+=dfs(node.right,curr_sum)
            prix_map[curr_sum]-=1
            return res
        return dfs(root,0)