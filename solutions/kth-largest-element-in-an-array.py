class Solution:
    def findKthLargest(self, nums: List[int], k: int) -> int:
        n = len(nums)
        target = n - k
        def partition(left, right):
            random_idx = randint(left, right) 
            nums[random_idx], nums[left] = nums[left], nums[random_idx]
            pivot = nums[left]
            le = left + 1
            ge = right
            
            while True:
                while le <= ge and nums[le] < pivot:
                    le += 1
                while le <= ge and nums[ge] > pivot:
                    ge -= 1
                
                if le >= ge:
                    break
                    
                nums[le], nums[ge] = nums[ge], nums[le]
                le += 1
                ge -= 1
                
            nums[left], nums[ge] = nums[ge], nums[left]
            return ge

        def quick_select(left, right):
            if left >= right:
                return nums[left]
            
            pivot_idx = partition(left, right)
            
            if pivot_idx == target:
                return nums[pivot_idx]
            elif pivot_idx < target:
                return quick_select(pivot_idx + 1, right)
            else:
                return quick_select(left, pivot_idx - 1)

        return quick_select(0, n - 1)

