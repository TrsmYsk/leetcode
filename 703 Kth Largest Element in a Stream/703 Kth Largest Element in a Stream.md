703. Kth Largest Element in a Stream  <https://leetcode.com/problems/kth-largest-element-in-a-stream/>

# step 1
- Arai60のカテゴリー分けから、heapを使うと予想。
- 自力で実装するのは時間がかかりそうなのでheapqモジュールを使う。```heap[0]```で最小要素にアクセスできるので、heapのサイズがkを超えないようにしておけばよさそう。\
  https://docs.python.org/3.13/library/heapq.html
- initでheapのサイズをkに抑える書き方をすぐに思いつかなかった。AIに相談してaddで追加する方法を教えてもらった。
- 時間計算量: 初期リストサイズn, 定員k, 受験者数m
  - init: O(nlogk)
  - add: O((m-n)logk)
- 空間計算量:
  - init: O(n)
  - add: O(k)
```python3
import heapq

class KthLargest:

    def __init__(self, k: int, nums: List[int]):
        self.capacity = k
        self.scores = []
        for score in nums:
            self.add(score)

    def add(self, val: int) -> int:
        heapq.heappush(self.scores, val)
        if len(self.scores) > self.capacity:
            heapq.heappop(self.scores)
        return self.scores[0]

```

# step 2
- https://github.com/tokuhirat/LeetCode/pull/8/changes#r2072364808
  - 入力のnumsを破壊するか否か。step1の実装は壊さない方法だが、そこまで検討していなかった。今回の問題設定は入試の点数管理なので提出期限などが存在しているであろうことを考えると入力を壊さない方が安全か。
  - 破壊しないほうが原則的らしい。 https://github.com/rinost081/LeetCode/pull/9/changes#r1874734978

- https://github.com/syoshida20/leetcode/pull/13/changes#r2051729666
  - heapの命名について。top_kの方がscoresよりも中身が伝わる気がする。

- https://github.com/fuga-98/arai60/pull/9/changes#r1966485704
  - リストを使った方法。insortが最適化されているので、定数倍の違いが効くため速いらしい。この方法は選択肢に入っていなかった。
  - heapの方法も要素がkを超えたときはheappushpopを使うようにしてあり、参考になった。

- https://github.com/katataku/leetcode/pull/8/changes#r1856437996
  - kが負の場合の処理も考えていなかった。入学試験の合格者の管理が目的なら間違ったまま動き続けるよりは止まってくれた方がよさそう。

- https://github.com/Ryotaro25/leetcode_first60/pull/9/changes#r1619710596
  - C++だといきなりpriority queを検討するのは違和感があるらしい。pythonでもsorted listをまず検討すべきなのだろうか。
  
- https://discord.com/channels/1084280443945353267/1192736784354918470/1194613857046503444
  - 小田さんのheapの実装。

- https://github.com/python/cpython/blob/main/Lib/heapq.py
  - cpythonのheapqの実装。

## 2-1: heapq
```python3
import heapq
from typing import List

class KthLargest:

    def __init__(self, k: int, nums: List[int]):
        if not isinstance(k, int) or k < 1:
            raise ValueError("k must be positive integer")

        self.k = k
        self.top_k = []
        for score in nums:
            self.add(score)

    def add(self, val: int) -> int:
        if len(self.top_k) < self.k:
            heapq.heappush(self.top_k, val)
            return self.top_k[0]
        heapq.heappushpop(self.top_k, val)
        return self.top_k[0]


```

## 2-2: insort
```python3
import bisect
from typing import List

class KthLargest:

    def __init__(self, k: int, nums: List[int]):
        if not isinstance(k, int) or k < 1:
            raise ValueError("k must be positive integer")
        self.k = k
        self.top_k = sorted(nums)[-k:]

    def add(self, val: int) -> int:
        bisect.insort(self.top_k, val)
        if len(self.top_k) > self.k:
            del self.top_k[0]
        return self.top_k[0]

```


# step 3
## 3-1: heapq
```python3
import heapq
from typing import List

class KthLargest:

    def __init__(self, k: int, nums: List[int]):
        if not isinstance(k, int) or k < 1:
            raise ValueError("k must be a positive integer")
        self.k = k
        self.top_k = []
        for score in nums:
            self.add(score)

    def add(self, val: int) -> int:
        if len(self.top_k) < self.k:
            heapq.heappush(self.top_k, val)
            return self.top_k[0]

        heapq.heappushpop(self.top_k, val)
        return self.top_k[0]

```

## 3-2: insort

```python3
import bisect
from typing import List

class KthLargest:

    def __init__(self, k: int, nums: List[int]):
        if not isinstance(k, int) or k < 1:
            raise ValueError("k must be a positive integer")
        self.k = k
        self.top_k = sorted(nums)
        if len(self.top_k) > k:
            del self.top_k[:-k]

    def add(self, val: int) -> int:
        bisect.insort(self.top_k, val)
        if len(self.top_k) > self.k:
            del self.top_k[0]
        return self.top_k[0]

```

# 自作 min heap

```python3
from typing import List

class MinHeap:
    
    def __init__(self, data: List[int] = None):
        self.v = []
        if data is not None:
            self.heapify(data)

    def __len__(self) -> int:
        return len(self.v)

    def is_empty(self) -> bool:
        return len(self.v) == 0

    def get_min(self) -> int:
        if self.is_empty():
            raise IndexError("get min from empty heap")
        return self.v[0]

    def _first_child(self, index: int) -> int:
        return 2 * index + 1
    
    def _second_child(self, index: int) -> int:
        return 2 * index + 2

    def _parent(self, index: int) -> int:
        return (index - 1) // 2

    def _has_first_child(self, index: int) -> bool:
        return self._first_child(index) < len(self.v)

    def _has_second_child(self, index: int) -> bool:
        return self._second_child(index) < len(self.v)

    def _has_child(self, index: int) -> bool:
        return self._has_first_child(index)

    def _smaller_child(self, index: int) -> Optional[int]:
        if not self._has_child(index):
            return None

        smaller_child = self._first_child(index)
        if (self._has_second_child(index) and
                self.v[self._second_child(index)] < self.v[smaller_child]):
            smaller_child = self._second_child(index)
        return smaller_child

    def _swap(self, index1: int, index2: int) -> None:
        self.v[index1], self.v[index2] = self.v[index2], self.v[index1]

    def _shift_up(self, index: int) -> None:
        while index > 0:
            parent = self._parent(index)
            if self.v[index] >= self.v[parent]:
                break
            self._swap(index, parent)
            index = parent

    def _shift_down(self, index: int) -> None:
        while self._has_child(index):
            smaller_child = self._smaller_child(index)
            if self.v[index] <= self.v[smaller_child]:
                break
            self._swap(index, smaller_child)
            index = smaller_child

    def heappush(self, value: int) -> None:
        self.v.append(value)
        added_index = len(self.v)-1
        self._shift_up(added_index)

    def heappop(self) -> int:
        if self.is_empty():
            raise IndexError("pop from empty heap")

        min_value = self.v[0]
        self.v[0] = self.v[len(self.v)-1]
        self.v.pop()
        if self.is_empty():
            return min_value
        
        self._shift_down(0)
        return min_value

    def heapify(self, data: List[int]) -> None:
        self.v = data[:]
        last_parent = len(self.v) // 2 - 1
        for index in range(last_parent, -1, -1):
            self._shift_down(index)

class KthLargest:

    def __init__(self, k: int, nums: List[int]):
        if not isinstance(k, int) or k < 1:
            raise ValueError("k must be a positive integer")

        self.k = k
        self.top_k = MinHeap(data=nums)
        while len(self.top_k) > self.k:
            self.top_k.heappop()

    def add(self, val: int) -> int:
        self.top_k.heappush(val)
        if len(self.top_k) > self.k:
            self.top_k.heappop()
        return self.top_k.get_min()

```
