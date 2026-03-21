https://leetcode.com/problems/find-k-pairs-with-smallest-sums/description/

## inputs
- nums1: integer list
- nums2: integer list
- k: positive integer

## constraints
- 1 <= nums1.length, nums2.length <= 10^5
- -10^9 <= nums1[i], nums2[i] <= 10^9
- nums1 and nums2 both are sorted in non-decreasing order.
- 1 <= k <= 10^4
- k <= nums1.length * nums2.length

# step1
- 最初に思いついた方法は、二重ループを回してnums1.length * nums2.length組の中から和が最小になるk組を探す方法。
  - k=10^4のときnums1とnums2がともに10^5個の数を格納している最悪ケースを考える。
  - 必要なメモリは 10^10 * sizeof(int) byte = sizeof(int) GB、leetcodeの環境ではおそらくメモリ制限でアウトになる。
  - ヒープを使う場合の実行時間は、step数が10^10 * log(10^4) (steps)で、pythonの実行速度が 1M ~ 10M (steps/秒)だから、920 ~ 9200 秒かかる。計算時間もアウト。
- 必要に応じてペアを作っていく方法にしないといけないが、思いつかなかったのでchat GPTに相談した。
  - 行の長さがnums1.length、列の長さがnums2.lengthの行列に数のペアの和が順番を維持して格納されているとする。つまり、(i,j)成分はnums1[i] + nums2[j]。
  - この行列は同一行内で右に行くほど値が大きくなっていく。そこで、行列の一番左の列だけを取り出してきたリストを作る。値が一番小さいものを探せば、それは最小の和である。
  - 最小値を格納したら、リストの最小値が格納されていた場所に、行列において最小値の1つ右隣にある値を格納する。そして、リストの値の大小を比較して2番目に小さいペアを探す。
  - これをk回繰り返せば、最小のk組が見つかる。
- 空間計算量: O(min{n1, k}), n1: nums1のサイズ
- 最悪時間計算量: O(klog(min{n1, k})), n1: nums1のサイズ
```python3
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

```