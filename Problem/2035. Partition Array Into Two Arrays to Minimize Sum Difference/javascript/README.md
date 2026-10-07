![header](https://capsule-render.vercel.app/api?type=waving&color=0:F7DF1E,100:323330&height=190&section=header&text=2035.+Partition+Into+Two+Arrays&fontSize=34&fontColor=202325&fontAlign=50&fontAlignY=55&animation=fadeIn&desc=JavaScript+%7C+typed+arrays+%2B+native+numeric+sort&descAlign=50&descAlignY=72&descFontColor=202325)

```text
$ node -e "console.log(minimumDifference([2,-1,0,4,-2,-9]))"
0
$ node -e "console.log(minimum_difference([3,9,7,3]))"
2
$ node -e "console.log(minimumDifference([-36,36]))"
72
```

<div align="center">

| 🧪 Testcases | ⏱️ Runtime | 🚀 Beats |  Memory |  Buffers |
| :---: | :---: | :---: | :---: | :---: |
| **201 / 201** | **201 ms** | **100.00 %** | **89.26 MB** | **typed** |

<img src="https://user-images.githubusercontent.com/74038190/212897782-96581536-54a0-4b87-87b4-5e55f95e8a8b.gif" width="340" alt="banner">

<img src="https://readme-typing-svg.demolab.com?font=Fira+Code&weight=700&size=20&duration=1400&pause=500&color=B8860B&center=true&vCenter=true&width=440&lines=JavaScript+%7C+201+ms+%7C+beats+100.00%25;Int32Array+buckets,+native+numeric+sort;Tabulated+popcount,+staircase+settle" alt="animated typing title">

![JavaScript](https://img.shields.io/badge/JavaScript-323330?style=flat&logo=javascript&logoColor=F7DF1E) ![Status](https://img.shields.io/badge/Status-Accepted-00C853?style=flat&logo=leetcode&logoColor=white) ![Difficulty](https://img.shields.io/badge/Difficulty-Hard-C73E3E?style=flat) ![Sort](https://img.shields.io/badge/Sort-native%20typed-F7DF1E?style=flat)

</div>

<div align="center">

**[⚡ Fact](#-the-structural-fact) · [📉 Order Book](#-the-bucket-order-book) · [🌐 Pipeline](#-the-pipeline) · [🤖 Mechanism](#-mechanism) · [🎯 Traces](#-witness-traces) · [📦 Source](#-source) · [🔒 Notes](#-engineering-notes) · [🚀 Complexity](#-complexity)**

</div>

> [!NOTE]
> **Judge record:** Accepted 201 / 201, runtime 201 ms, beats 100.00 %, memory 89.26 MB.

> [!IMPORTANT]
> **Binding stance:** no JavaScript driver line observed; R1 fallback in force: kernel function plus camelCase and snake_case public aliases, zero duplication.

## ⚡ The Structural Fact

Signing bijection: n plus, n minus, objective |D|; halves report (k, d); D = d1 + d2 under k1 + k2 = n; bucket pairs are the whole market. The staircase settles each pair: record |x + y|, then move the pointer on the dominating side; every discarded pair is dominated by a value already banked.

## 📉 The Bucket Order Book

| k | depth C(3, k) | instrument | settle rule |
| :---: | :---: | :--- | :--- |
| 0 | 1 | all-minus quotes | staircase vs k2 = 3 |
| 1 | 3 | one-plus quotes | staircase vs k2 = 2 |
| 2 | 3 | two-plus quotes | staircase vs k2 = 1 |
| 3 | 1 | all-plus quotes | staircase vs k2 = 0 |

## 🌐 The Pipeline

```mermaid
flowchart TD
    M[masks] --> R[low-bit recurrence, Math.clz32 names the bit]
    R --> T[Uint8Array popcount table]
    T --> K[Int32Array buckets via fill cursors]
    K --> S[typed sort, numeric by default]
    S --> P[pair k with n - k]
    P --> Q[staircase settle]
    Q --> Z[best, zero returns at once]
    classDef a fill:#323330,stroke:#F7DF1E,color:#F7DF1E
    classDef b fill:#00695C,stroke:#333,color:#fff
    classDef c fill:#283593,stroke:#333,color:#fff
    class M,R,T a
    class K,S b
    class P,Q,Z c
```

## 🤖 Mechanism

* `pc` tabulates popcount once per call: pc[m] = pc[m >> 1] + (m & 1).
* Buckets are Int32Array of exact binomial depth; `sort()` on typed arrays is numeric without a comparator.
* The staircase walks each bucket pair with plain number arithmetic; all magnitudes below 2^53 keep doubles exact.
* `minimumDifference` and `minimum_difference` delegate to `minimumDifferenceKernel`.

## 🎯 Witness Traces

| Input | n | Certifying event | Answer |
| :--- | :---: | :--- | :---: |
| `[3,9,7,3]` | 2 | staircase banks 2 | **2** |
| `[-36,36]` | 1 | only signings exist | **72** |
| `[2,-1,0,4,-2,-9]` | 3 | zero met, immediate return | **0** |
| `[5,-5]` | 1 | single signing per side | **10** |

## 📦 Source

<details>
<summary><strong>🔓 Expand the accepted JavaScript source</strong></summary>

```javascript
var minimumDifferenceKernel = function(nums) {
    var n = nums.length >> 1;
    var masks = 1 << n;
    var d0 = new Int32Array(masks);
    var d1 = new Int32Array(masks);
    var sum0 = 0;
    var sum1 = 0;
    var i;
    for (i = 0; i < n; i++) sum0 += nums[i];
    for (i = n; i < nums.length; i++) sum1 += nums[i];
    d0[0] = -sum0;
    d1[0] = -sum1;
    for (var m = 1; m < masks; m++) {
        var low = m & -m;
        i = 31 - Math.clz32(low);
        var pm = m ^ low;
        d0[m] = d0[pm] + 2 * nums[i];
        d1[m] = d1[pm] + 2 * nums[n + i];
    }
    var pc = new Uint8Array(masks);
    for (m = 1; m < masks; m++) pc[m] = pc[m >> 1] + (m & 1);
    var comb = new Array(n + 1);
    comb[0] = 1;
    for (var k = 1; k <= n; k++) comb[k] = comb[k - 1] * (n - k + 1) / k;
    var bu0 = new Array(n + 1);
    var bu1 = new Array(n + 1);
    for (k = 0; k <= n; k++) {
        bu0[k] = new Int32Array(comb[k]);
        bu1[k] = new Int32Array(comb[k]);
    }
    var fill = new Array(n + 1).fill(0);
    for (m = 0; m < masks; m++) bu0[pc[m]][fill[pc[m]]++] = d0[m];
    fill = new Array(n + 1).fill(0);
    for (m = 0; m < masks; m++) bu1[pc[m]][fill[pc[m]]++] = d1[m];
    for (k = 0; k <= n; k++) {
        bu0[k].sort();
        bu1[k].sort();
    }
    var best = Infinity;
    for (k = 0; k <= n; k++) {
        var A = bu0[k];
        var B = bu1[n - k];
        var ia = 0;
        var jb = B.length - 1;
        while (ia < A.length && jb >= 0) {
            var s = A[ia] + B[jb];
            var v = s < 0 ? -s : s;
            if (v < best) best = v;
            if (best === 0) return 0;
            if (s < 0) ia++;
            else jb--;
        }
    }
    return best;
};

var minimumDifference = function(nums) {
    return minimumDifferenceKernel(nums);
};

var minimum_difference = function(nums) {
    return minimumDifferenceKernel(nums);
};
```

</details>

## 🔒 Notes

> [!NOTE]
> **Numeric exactness:** every magnitude stays below 2^53, so double arithmetic is integer arithmetic here; the typed sort needs no comparator because Int32Array.sort is numeric by specification.

> [!WARNING]
> **Bounds:** masks ≤ 32768 equals the typed buffer length; fill cursors stop at binomial depths; staircase pointers stay inside their typed arrays by loop condition.

* **Allocation:** typed arrays per call are the only traffic; no objects inside the staircase.
* **Performance honesty:** 201 ms is a harness label; the invariant is one recurrence pass, one bucketing pass, native sorts, and one staircase walk per pair.

## 🚀 Complexity

| Measure | Bound |
| :--- | :---: |
| Time | $O(2^n \log 2^n)$ sorts, staircase $O(2^n)$ |
| Space | $O(2^n)$ typed buffers |

<div align="center">

<img src="https://media.giphy.com/media/LmNwrBhejkK9EFP504/giphy.gif" width="200" alt="banner small">

*Built under the Tar0 registry: R1 binding from evidence, R2 proof-carrying pruning, R9 single kernel multi-alias.*

</div>

![footer](https://capsule-render.vercel.app/api?type=waving&color=0:323330,100:F7DF1E&height=120&section=footer&animation=fadeIn)
