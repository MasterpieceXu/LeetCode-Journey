# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
class Solution:
    def deleteDuplicates(self, head: Optional[ListNode]) -> Optional[ListNode]:
        dummy1 = ListNode(101)
        dummy2 = ListNode(101)
        p1 = dummy1
        p2 = dummy2
        p = head
        while p:
            if (p.next is not None and p.val == p.next.val) or p.val ==  p2.val:
                p2.next = p
                p2 = p2.next
            else:
                p1.next = p
                p1 = p1.next
            p = p.next
            p1.next = None
            p2.next = None
        return dummy1.next