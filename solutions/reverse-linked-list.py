# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
class Solution:
    def reverseList(self, head: Optional[ListNode]) -> Optional[ListNode]:
        pre=None
        curr=head
        while curr:
            next_node=curr.next
            curr.next=pre
            pre=curr
            curr=next_node
        return pre