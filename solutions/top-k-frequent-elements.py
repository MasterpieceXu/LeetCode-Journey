class Solution:
    def topKFrequent(self, nums: List[int], k: int) -> List[int]:
      r={}
      for i in nums:
        if i not in r:
          r[i]=1
        else:
          r[i]+=1
      d=dict(sorted(r.items(),key=lambda x:x[1],reverse=True))
      result=[]
      a=d.keys()
      for i in range(k):
        result.append((list(a)[i]))
      return result