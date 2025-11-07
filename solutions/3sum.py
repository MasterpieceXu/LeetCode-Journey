class Solution:
    def threeSum(self, nums: List[int]) -> List[List[int]]:
        sorted_nums=sorted(nums)
        answer_set=set()
        answer=[]
        for i in range(len(sorted_nums)):
            left=i+1
            right=len(sorted_nums)-1
            while left<right:
                sum_three=sorted_nums[i]+sorted_nums[left]+sorted_nums[right]
                if sum_three>0:
                    right-=1
                elif sum_three<0:
                    left+=1
                else:
                    answer_set.add((sorted_nums[i],sorted_nums[left],sorted_nums[right]))
                    left+=1
                    right-=1
        return list(answer_set)