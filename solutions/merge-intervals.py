class Solution:
    def merge(self, intervals: List[List[int]]) -> List[List[int]]:
        if not intervals:
            return []
        res=[]
        intervals.sort(key=lambda x:x[0])
        res.append(intervals[0])
        for i in range(len(intervals)):
            curr=intervals[i]
            last=res[-1]
            if curr[0]<=last[-1]:
                last[1]=max(last[1],curr[1])
            else:
                res.append(curr)
        return res
