class Solution(object):
    def canConstruct(self, ransomNote, magazine):
        """
        :type ransomNote: str
        :type magazine: str
        :rtype: bool
        """
        magazine_list=list(magazine)
        ransomNote_list=list(ransomNote)
        if len(ransomNote_list)>len(magazine_list):
            return False
        else:
            for i in ransomNote_list:
                if i in magazine_list:
                    magazine_list.remove(i)
                else:
                    return False
            return True