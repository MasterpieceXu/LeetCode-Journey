# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
class Solution:
    def nextLargerNodes(self, head: Optional[ListNode]) -> List[int]:
        nums = []
        p  = head
        while p:
            nums.append(p.val)
            p = p.next
        
        n = len(nums)
        s = []
        res = [0] * n
        for i in range(n-1, -1, -1):
            while s and s[-1] <= nums[i]:
                s.pop()
            res[i] = 0 if not s else s[-1]
            s.append(nums[i])
        return res