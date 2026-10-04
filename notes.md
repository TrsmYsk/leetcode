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

## plan2: n1×n2の表(行列)を考えて、幅優先探索でトップkを探す
- chat-GPTに教えてもらった方法
- C = [nums1[i], nums2[j]]という行列を考えると、今いる場所(i,j)から右か下に動くと必ずより大きなペアになる
- (0, 0)成分から探索を初めて、順次、右の要素と下の要素を管理用のヒープに追加していく
- 時間計算量O(klogk)なので、実行時間は雑に見積もって1.2ms程度

## plan3: generatorで候補を逐次生成する
- chat-GPTに教えてもらった方法
- generatorでnums1[i]とnums2の要素とのペアを作り、heapq.merge()で統合する
- 時間計算量O(klogk)なので、実行時間は雑に見積もって1.2ms程度

# step2

# step3