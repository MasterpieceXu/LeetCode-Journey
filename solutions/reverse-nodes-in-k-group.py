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
            group_next=kth.next #下一组的开头
            group_start=group_pre.next # 反转列表的当前组的开头
            kth.next=None
            group_pre.next=self.reverse(group_start) #调用反转函数，对当前的进行反转
            group_start.next=group_next # 反转过后的开头到了末尾
            group_pre=group_start # 指针移动到下一组，继续做循环
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
