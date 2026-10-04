# plan1: トップkの候補になるペアだけを管理する方法
import heapq

class Solution:
    def kSmallestPairs(self, nums1: list[int], nums2: list[int], k: int) -> list[list[int]]:
        if not nums1 or not nums2:
            raise ValueError("input lists must contain at least 1 element")
        if k <= 0:
            raise ValueError("k must be positive integer")

        candidates = []
        for index in range(min(k, len(nums1))):
            candidate = (nums1[index] + nums2[0], index, 0)
            heapq.heappush(candidates, candidate)

        k_smallests = []
        while candidates and len(k_smallests) < k:
            _, index1, index2, = heapq.heappop(candidates)
            k_smallests.append([nums1[index1], nums2[index2]])
            if index2 + 1 >= len(nums2):
                continue
            candidate = (nums1[index1] + nums2[index2 + 1], index1, index2 + 1)
            heapq.heappush(candidates, candidate)

        return k_smallests

# plan2: nums1 × nums2 の表を作って幅優先探索する
import heapq

class Solution:
    def kSmallestPairs(self, nums1: list[int], nums2: list[int], k: int) -> list[list[int]]:
        if not nums1 or not nums2:
            raise ValueError("input lists must contain at least 1 element")
        if k <= 0:
            raise ValueError("k must be positive integer")

        candidates = [(nums1[0] + nums2[0], 0, 0)]
        visited = {(0, 0)}
        k_smallests = []
        while candidates and len(k_smallests) < k:
            _, index1, index2 = heapq.heappop(candidates)
            k_smallests.append([nums1[index1], nums2[index2]])

            next1 = index1 + 1
            if next1 < len(nums1) and (next1, index2) not in visited:
                candidate = (nums1[next1] + nums2[index2], next1, index2)
                heapq.heappush(candidates, candidate)
                visited.add((next1, index2))

            next2 = index2 + 1
            if next2 < len(nums2) and (index1, next2) not in visited:
                candidate = (nums1[index1] + nums2[next2], index1, next2)
                heapq.heappush(candidates, candidate)
                visited.add((index1, next2))

        return k_smallests

# plan3: generatorを使う方法
import heapq
import itertools

class Solution:
    def kSmallestPairs(self, nums1: list[int], nums2: list[int], k: int) -> list[list[int]]:
        def pair_generator(num1):
            for num2 in nums2:
                yield (num1 + num2, [num1, num2])

        if not nums1 or not nums2:
            raise ValueError("input lists must contain at least 1 element")
        if k <= 0:
            raise ValueError("k must be positive integer")

        pairs = (pair_generator(num1) for num1 in nums1[:k])
        candidates = heapq.merge(*pairs)
        return [pair for _, pair in itertools.islice(candidates, k)]
