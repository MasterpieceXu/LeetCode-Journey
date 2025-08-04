class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        reserve=[]
        for j in range(len(s)):
            check=set()
            option=[]
            for i in range(j,len(s)):
                if s[i] not in check:
                    check.add(s[i])
                    option.append(s[i])
                else:
                    break
            reserve.append(option)
        answer=max((len(i) for i  in reserve),default=0 )
        return answer