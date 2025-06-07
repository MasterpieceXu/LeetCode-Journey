class Solution:
    def countGoodTriplets(self, arr: List[int], a: int, b: int, c: int) -> int:
        res=0
        for i in range(len(arr)):
            for j in range(len(arr)):
                for k in range(len(arr)):
                    cpa=arr[i]-arr[j]
                    cpb=arr[j]-arr[k]
                    cpc=arr[i]-arr[k]
                    if abs(cpa)<=a and abs(cpb)<=b and abs(cpc)<=c and 0<=i<j<k:
                        res+=1
        return res