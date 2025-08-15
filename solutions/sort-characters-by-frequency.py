class Solution:
    def frequencySort(self, s: str) -> str:
        cnt=Counter(s)
        return ''.join(ch*freq for ch,freq in sorted(cnt.items(), key=lambda x :x[1], reverse=True))

        


        