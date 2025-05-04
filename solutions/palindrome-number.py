class Solution(object):
    def isPalindrome(self, x):
        """
        :type x: int
        :rtype: bool
        """
        if x<0:
            return False
        x_str=str(x)
        n=len(x_str)//2
        for i in range(0,n+1):
            if x_str[i]!=x_str[-1-i]:
                return False
        return True  