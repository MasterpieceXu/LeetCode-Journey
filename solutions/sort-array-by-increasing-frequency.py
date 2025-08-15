class Solution:
    def frequencySort(self, nums: List[int]) -> List[int]:
        dic={}
        for i in nums:
          if i not in dic:
            dic[i]=1
          else:
            dic[i]+=1
        d_sorted=sorted(dic.items() , key=lambda x: (x[1],-x[0]))
        result=[]
        for x in d_sorted:
          for i in range(x[1]):
            result.append(x[0])
        return result

