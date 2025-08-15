class Solution:
    def findShortestSubArray(self, nums: List[int]) -> int:
      first = {}
      last = {}
      cnt = defaultdict(int)
      for i, x in enumerate(nums):
        if x not in first:
            first[x] = i
        last[x] = i
        cnt[x] += 1

      degree = max(cnt.values())
      ans = len(nums)
      for x, c in cnt.items():
          if c == degree:
            ans = min(ans, last[x] - first[x] + 1)
      return ans










            