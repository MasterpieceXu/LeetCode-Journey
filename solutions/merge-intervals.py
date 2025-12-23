class Solution:
    def merge(self, intervals: List[List[int]]) -> List[List[int]]:
        if not intervals:
            return []
        intervals.sort(key=lambda x:x[0])
        merge=[]
        for option in intervals:
            if not merge or option[0]>merge[-1][-1]:
                merge.append(option)
            else:
                merge[-1][-1]=max(merge[-1][-1],option[1])
        return merge