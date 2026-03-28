class Solution:
    def nextGreaterElement(self, nums1: List[int], nums2: List[int]) -> List[int]:
        mapping = {}
        res = [-1] * (len(nums1))
        res_nums2 = self.greater(nums2)
        for i in range(len(nums2)):
            mapping[nums2[i]] = res_nums2[i]
        return [mapping[n] for n in nums1]

    def greater(self, nums: List[int]):
        n = len(nums)
        res = [-1] * n
        s = []
        for i in range(n-1, -1, -1):
            while s and s[-1] <= nums[i]:
                s.pop()
            res[i] = -1 if not s else s[-1]
            s.append(nums[i])
        return res