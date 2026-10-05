# Description
You are given two integer arrays nums1 and nums2 sorted in non-decreasing order and an integer k.

Define a pair (u, v) which consists of one element from the first array and one element from the second array.

Return the k pairs (u1, v1), (u2, v2), ..., (uk, vk) with the smallest sums.

**Constraints:**
- 1 <= nums1.length, nums2.length <= 10^5
- -10^9 <= nums1[i], nums2[i] <= 10^9
- nums1 and nums2 both are sorted in non-decreasing order.
- 1 <= k <= 10^4
- k <= nums1.length * nums2.length

https://leetcode.com/problems/find-k-pairs-with-smallest-sums/description/

# step1
## 総当たりで全ペアを比較する方法
- nums1のサイズをn1、nums2のn2とすると、時間計算量はO(n1n2log(n1n2))
- 一つの配列が最大で10^5個の要素を持つから、最悪ケースでは総当たりだと10^10 = 10G 通りのペアができる。
- C言語が1秒で10G stepの命令を処理できると仮定すると、Python3の速さは100倍程度遅いから1秒で0.1G stepを処理できる。
- したがって、Python3だと10G 通りのペアの大小比較に、(10^10)*10log(10)/(10^8) ≒ 3000秒かかる。時間かかりすぎてるので採用できない

## plan1: トップkの候補になるペアだけを管理・保持する方法
- 入力される配列はソート済みなので、一方の配列を固定して(例えばnums1を固定)、もう一方の先頭要素(nums2[0])とのペアを作ればいい
- 順番が確定したペアがヒープから抜けたら(例えば[nums1[2], nums2[0]])、抜けた部分に次の候補のペア(nums1[2, nums2[1]])を補充する
- 時間計算量はO(klog(k))で、kは最大で10^4なので最悪ケースでの実行時間を雑に見積もると、(10^4)*4log(10)/(10^8) ≒ 1.2ミリ秒
```python
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

```

## plan2: n1×n2の表(行列)を考えて、幅優先探索でトップkを探す
- chat-GPTに教えてもらった方法
- C = [nums1[i], nums2[j]]という行列を考えると、今いる場所(i,j)から右か下に動くと必ずより大きなペアになる
- (0, 0)成分から探索を初めて、順次、右の要素と下の要素を管理用のヒープに追加していく
- 時間計算量O(klogk)なので、実行時間は雑に見積もって1.2ms程度
- 候補管理のヒープにプッシュする処理内容に重複があるので、当該処理を関数化した(push_to_heap())
```python
import heapq

class Solution:
    def kSmallestPairs(self, nums1: list[int], nums2: list[int], k: int) -> list[list[int]]:
        if not nums1 or not nums2:
            raise ValueError("input lists must contain at least 1 element")
        if k <= 0:
            raise ValueError("k must be positive integer")

        candidates = []
        visited = set()

        def push_to_heap(index1, index2):
            if index1 < len(nums1) and index2 < len(nums2) and (index1, index2) not in visited:
                candidate = (nums1[index1] + nums2[index2], index1, index2)
                heapq.heappush(candidates, candidate)
                visited.add((index1, index2))

        push_to_heap(0, 0)
        k_smallests = []
        while candidates and len(k_smallests) < k:
            _, index1, index2 = heapq.heappop(candidates)
            k_smallests.append([nums1[index1], nums2[index2]])
            push_to_heap(index1 + 1, index2)
            push_to_heap(index1, index2 + 1)

        return k_smallests

```

## plan3: generatorで候補を逐次生成する
- chat-GPTに教えてもらった方法
- generatorでnums1[i]とnums2の要素とのペアを作り、heapq.merge()で統合する
- 時間計算量O(klogk)なので、実行時間は雑に見積もって1.2ms程度
```python
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

```

# step2
## 総当たり法
https://github.com/KaoKao1233/LeetCodeArai60/pull/10#discussion_r4003132964
- 総当たりを実行するとメモリ制限に引っ掛かるらしい。メモリ使用量の見積もりはしてこなかったので、これからはメモリも意識する。

## plan2: n1×n2の表(行列)を使う
### コメント集
https://discord.com/channels/1084280443945353267/1200089668901937312/1222827848084099122
https://discord.com/channels/1084280443945353267/1192736784354918470/1220669329335648346
- 左と上の要素((i - 1, j)と(i, j - 1))がcandidateに追加されているときだけ新しい要素(i,j)を追加する((0,0)は例外)、というように条件を整理すれば、k_pairsの追加履歴だけを管理するだけでよくなる。気づいていなかったのでstep2でやってみる。

https://github.com/plushn/SWE-Arai60/pull/10#discussion_r2022084987
- 条件判定は一行ずつ分けたほうが読みやすい。これは採用する。

https://github.com/TORUS0818/leetcode/pull/12#discussion_r1623146530
- setを使わない方法。setとの良し悪しの違いが良く分からない。

## plan3: generatorを使う
### コメント集
https://discord.com/channels/1084280443945353267/1235829049511903273/1246118347863621652
https://discord.com/channels/1084280443945353267/1235829049511903273/1246303084435607682
https://discord.com/channels/1084280443945353267/1226508154833993788/1270734186713710614
https://github.com/nittoco/leetcode/pull/33#discussion_r1705956329
- コメント集のgeneratorを使った方法は理解に時間かかりそうなので、採用を見送る。

## Cpython ソース
https://github.com/python/cpython/blob/66df30d15c9052785ed6463663e70d38107a9edf/Lib/heapq.py#L330
- heapq.merge()の実装

## plan2 実装:candidateとして保持する条件を整理
```python
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

```


# step3
- step2から変更点:k_smallestsに追加済みかどうか判定する処理を関数化
```python
import heapq

class Solution:
    def kSmallestPairs(self, nums1: list[int], nums2: list[int], k: int) -> list[list[int]]:
        if not nums1 or not nums2:
            raise ValueError("input lists must not be empty")
        if k <= 0:
            raise ValueError("k must be positive integer")

        candidates = []
        added = set()

        def is_smallests(index1, index2):
            if (index1, index2) in added:
                return True
            return False

        def is_candidate(index1, index2):
            if index1 >= len(nums1):
                return False
            if index2 >= len(nums2):
                return False
            if index1 == 0 and index2 == 0:
                return True
            if index1 == 0 and is_smallests(index1, index2 - 1):
                return True
            if index2 == 0 and is_smallests(index1 - 1, index2):
                return True
            if is_smallests(index1, index2 - 1) and is_smallests(index1 - 1, index2):
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
            added.add((index1, index2))
            push_if_candidate(index1 + 1, index2)
            push_if_candidate(index1, index2 + 1)
        return k_smallests

```