"""
# Definition for a Node.
class Node:
    def __init__(self, val: Optional[int] = None, children: Optional[List['Node']] = None):
        self.val = val
        self.children = children
"""

class Solution:
    def levelOrder(self, root: 'Node') -> List[List[int]]:
        if root is None:
            return []
        res = []
        q = deque()
        q.append(root)
        while q:
            sz = len(q)
            levelres = []
            for _ in range(sz):
                curr = q.popleft()
                levelres.append(curr.val)
                for child in curr.children:
                    q.append(child)
            res.append(levelres)
        return res