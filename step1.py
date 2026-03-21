import heapq
from typing import List

class Solution:
    def kSmallestPairs(self, nums1: List[int], nums2: List[int], k: int) -> List[List[int]]:
        sum_and_indices = []
        for index1 in range(min(len(nums1), k)):
            heapq.heappush(sum_and_indices, (nums1[index1] + nums2[0], index1, 0))
        k_smallests = []
        while sum_and_indices and len(k_smallests) < k:
            _, index1, index2 = heapq.heappop(sum_and_indices)
            k_smallests.append([nums1[index1], nums2[index2]])
            if index2 + 1 >= len(nums2):
                continue
            heapq.heappush(sum_and_indices, (nums1[index1] + nums2[index2 + 1], index1, index2 + 1))
        return k_smallests
