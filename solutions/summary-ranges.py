class Solution:
    def summaryRanges(self, nums: List[int]) -> List[str]:
        if not nums:
            return []
        result=[nums[0]]
        R=[]
        for i in range(1,len(nums)):
            if nums[i-1]!=nums[i]-1:
                if len(result)==1:
                    R.append(f"{result[0]}")
                    result=[nums[i]]
                else:
                    R.append(f'{result[0]}->{result[-1]}')
                    result=[nums[i]]
            else:
                result.append(nums[i])
        if len(result)==1:
            R.append(f"{result[0]}")
        else:
            R.append(f'{result[0]}->{result[-1]}')
        return R
