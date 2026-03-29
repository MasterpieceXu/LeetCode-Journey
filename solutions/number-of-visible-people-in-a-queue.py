class Solution:
    def canSeePersonsCount(self, heights: List[int]) -> List[int]:
        n = len(heights)
        res = [0] * n
        s = []
        for i in range(n-1, -1, -1):
            count = 0
            while s and heights[i] >= s[-1]:
                s.pop()
                count += 1
            res[i] = count  if not s else count+1
            s.append(heights[i])
        return res
