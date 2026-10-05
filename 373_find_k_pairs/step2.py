import heapq

class Solution:
    def kSmallestPairs(self, nums1: list[int], nums2: list[int], k: int) -> list[list[int]]:
        if not nums1 or not nums2:
            raise ValueError("input lists must not be empty")
        if k <= 0:
            raise ValueError("k must be positive integer")

        candidates = []
        added_as_smallests = set()

        def is_candidate(index1, index2):
            if index1 >= len(nums1):
                return False
            if index2 >= len(nums2):
                return False
            if index1 == 0 and index2 == 0:
                return True
            if index1 == 0 and (index1, index2 - 1) in added_as_smallests:
                return True
            if index2 == 0 and (index1 - 1, index2) in added_as_smallests:
                return True
            if (index1 - 1, index2) in added_as_smallests and (index1, index2 - 1) in added_as_smallests:
                return True
            return False

        def push_if_candidate(index1, index2):
            if not is_candidate(index1, index2):
                return
            candidate = (nums1[index1] + nums2[index2], index1, index2)
            heapq.heappush(candidates, candidate)

        push_if_candidate(0, 0)
        k_smallests = []
        while candidates and len(k_smallests) < k:
            _, index1, index2 = heapq.heappop(candidates)
            k_smallests.append([nums1[index1], nums2[index2]])
            added_as_smallests.add((index1, index2))
            push_if_candidate(index1 + 1, index2)
            push_if_candidate(index1, index2 + 1)
        return k_smallests
