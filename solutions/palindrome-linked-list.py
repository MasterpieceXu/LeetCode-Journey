# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
class Solution:
    def isPalindrome(self, head: Optional[ListNode]) -> bool:
        if not head or not head.next:
            return True
        slow,fast=head,head
        while fast and fast.next:
            slow=slow.next
            fast=fast.next.next
        
        pre=None
        curr=slow
        while curr:
            next_node=curr.next
            curr.next=pre
            pre=curr
            curr=next_node
        left,right=head,pre
        while right:
            if left.val!=right.val:
                return False
            left=left.next
            right=right.next
        return True
