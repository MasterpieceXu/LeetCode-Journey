# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
class Solution:
    def isPalindrome(self, head: Optional[ListNode]) -> bool:
        slow=head
        fast=head
        while fast and fast.next:
            slow=slow.next
            fast=fast.next.next
        if fast:
            slow=slow.next
        left=head
        right=self.reverse(slow)
        while right:
            if left.val!=right.val:
                return False
            left=left.next
            right=right.next
        
        return True
    def reverse(self,head: ListNode)->ListNode:
        pre=None
        curr=head
        while curr:
            next=curr.next
            curr.next=pre
            pre=curr
            curr=next
        return pre