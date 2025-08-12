class Solution:
    def countBits(self, n: int) -> List[int]:
        result=[]
        for i in range(n+1):
            bit=bin(i)[2:]
            nums=bit.count('1')
            result.append(nums)
        return result