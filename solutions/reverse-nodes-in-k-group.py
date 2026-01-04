# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
class Solution:
    def reverseKGroup(self, head: Optional[ListNode], k: int) -> Optional[ListNode]:
        if head is None:
            return None
        a=b=head
        for _ in range(k):
            if b is None:
                return head
            b=b.next
        newhead=self.reverseN(a,k)
        a.next=self.reverseKGroup(b,k)
        return newhead
    def reverseN(self, head:Optional[ListNode], n:int) -> Optional[ListNode]:
        if head is None or head.next is None:
            return head
        pre,curr,nxt=None,head,head.next
        while n>0:
            curr.next=pre
            pre=curr
            curr=nxt
            if nxt is not None:
                nxt=nxt.next
            n-=1
        head.next=curr
        return pre