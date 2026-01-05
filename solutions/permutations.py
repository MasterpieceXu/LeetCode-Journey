class Solution:
    def permute(self, nums: List[int]) -> List[List[int]]:
        self.res=[]
        track=[]
        used_num=[False]*len(nums)
        self.backtrack(nums,track,used_num)
        return self.res
    def backtrack(self,nums,track,used_num):
        if len(track)==len(nums):
            self.res.append(track.copy())
            return 
        for i in range(len(nums)):
            if used_num[i]:
                continue
            track.append(nums[i])
            used_num[i]=True
            self.backtrack(nums,track,used_num)
            track.pop()
            used_num[i]=False