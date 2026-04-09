# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def minDepth(self, root: Optional[TreeNode]) -> int:
        if root is None:
            return 0
        q = deque()
        q.append(root)
        depth = 1 
        while q:
            sz = len(q)
            for _ in range(sz):
                curr = q.popleft()
                if curr.left is None and curr.right is None:
                    return depth
                if curr.left is not None:
                    q.append(curr.left)
                if curr.right is not None:
                    q.append(curr.right)
            depth += 1
        return depth