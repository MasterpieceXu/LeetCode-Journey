class Solution:
    def groupAnagrams(self, strs: List[str]) -> List[List[str]]:
        default_dic={}
        for s in strs:
            key="".join(sorted(s))
            if key in default_dic:
                default_dic[key].append(s)
            else:
                default_dic[key]=[s]
        return list(default_dic.values())