class Solution:
    def isPowerOfTwo(self, n: int) -> bool:
        num=bin(n)[2:]
        if num[0]=='1' and num.count('1')==1:
            return True
        return False