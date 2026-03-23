class Solution:
    def longestPalindrome(self, s: str) -> str:
        res = ""
        for i in range(len(s)):
            s1 = self.check(s, i, i)
            s2 = self.check(s, i, i+1)
            res = max(res, s1, s2, key=len)
        return res
    
    def check(self, s: str, l, r):
        while l >=0 and r < len(s) and s[l] == s[r]:
            l -= 1
            r += 1
        return s[l+1 : r]