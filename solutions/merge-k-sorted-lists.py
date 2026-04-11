# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
class Solution:
    def mergeKLists(self, lists: List[Optional[ListNode]]) -> Optional[ListNode]:
        if lists is None:
            return []
        pq = []
        dummy = ListNode(-1)
        p = dummy
        # 将链表头结点加入到结果中
        for i, head in enumerate(lists):
            if head is not None:
                heapq.heappush(pq,(head.val, i, head))
        while pq:
            val, i, node = heapq.heappop(pq)
            p.next = node
            if node.next is not None:
                heapq.heappush(pq,(node.next.val, i, node.next))
            p = p.next
        return dummy.next