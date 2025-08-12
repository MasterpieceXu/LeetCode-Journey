class Solution:
    def hammingWeight(self, n: int) -> int:
        num=bin(n)[2:]
        nums_1=num.count('1')
        return nums_1