# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
class Solution:
    def reverseKGroup(self, head: Optional[ListNode], k: int) -> Optional[ListNode]:
        dummy=ListNode(0,head)
        group_pre=dummy
        while True:
            kth=group_pre
            for _ in range(k):
                kth=kth.next
                if not kth:
                    return dummy.next
            group_next=kth.next
            group_start=group_pre.next
            kth.next=None
            group_pre.next=self.reverse(group_start)
            group_start.next=group_next
            group_pre=group_start
        return dummy.next
    def reverse(self,head:ListNode) ->ListNode:
        pre=None
        curr=head
        while curr:
            next_node=curr.next
            curr.next=pre
            pre=curr
            curr=next_node
        return pre
