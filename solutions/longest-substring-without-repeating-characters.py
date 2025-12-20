class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        if not s:
            return 0
        n=len(s)
        left=0
        lookup=set()
        max_len=0
        current_len=0
        for i in range(n):
            current_len+=1
            while s[i] in lookup:
                lookup.remove(s[left])
                left+=1
                current_len-=1
            else:
                lookup.add(s[i])
            
            if current_len>max_len:
                max_len=current_len
        return max_len