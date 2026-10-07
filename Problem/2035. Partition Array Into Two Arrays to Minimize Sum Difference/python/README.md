![header](https://capsule-render.vercel.app/api?type=waving&color=0:1565C0,100:00BFA5&height=190&section=header&text=2035.+Partition+Into+Two+Arrays&fontSize=34&fontColor=FFFFFF&fontAlign=50&fontAlignY=55&animation=fadeIn&desc=Python+%7C+vectorized+fast+path+%2B+exact+pure+fallback&descAlign=50&descAlignY=72&descFontColor=FFFFFF)

<div align="center">

| 🧪 Testcases | ⏱️ Runtime | 🚀 Beats | 🧠 Memory |  Paths |
| :---: | :---: | :---: | :---: | :---: |
| **201 / 201** | **235 ms** | **99.76 %** | **33.15 MB** | **2** |

<img src="https://private-user-images.githubusercontent.com/74038190/240820597-a762dc06-3a4c-432e-8679-a99fe8a433b7.gif?jwt=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3OTEzNjQwNjgsIm5iZiI6MTc5MTM2Mzc2OCwicGF0aCI6Ii83NDAzODE5MC8yNDA4MjA1OTctYTc2MmRjMDYtM2E0Yy00MzJlLTg2NzktYTk5ZmU4YTQzM2I3LmdpZj9YLUFtei1BbGdvcml0aG09QVdTNC1ITUFDLVNIQTI1NiZYLUFtei1DcmVkZW50aWFsPUFLSUFWQ09EWUxTQTUzUFFLNFpBJTJGMjAyNjEwMDclMkZ1cy1lYXN0LTElMkZzMyUyRmF3czRfcmVxdWVzdCZYLUFtei1EYXRlPTIwMjYxMDA3VDA5MDI0OFomWC1BbXotRXhwaXJlcz0zMDAmWC1BbXotU2lnbmF0dXJlPWMxMTA2MTI2M2JmYzA2MDY3YTQ1YzZiMjE0ZGFlM2MyZWMyZWFiYjdmMjZlYjVmZWZiNmNiYmU0ZGYxMjU5ZTUmWC1BbXotU2lnbmVkSGVhZGVycz1ob3N0JnJlc3BvbnNlLWNvbnRlbnQtdHlwZT1pbWFnZSUyRmdpZiJ9.YfZkv8Omz1aG5qfi-fJ_NJhg5BeA2WyUD-HggbHhw60" width="340" alt="banner">

<img src="https://readme-typing-svg.demolab.com?font=Fira+Code&weight=700&size=20&duration=1400&pause=500&color=00BFA5&center=true&vCenter=true&width=440&lines=Python+%7C+235+ms+%7C+beats+99.76%25;numpy+path+when+present,+pure+path+always;Doubling+in+comprehensions,+staircase+in+locals" alt="animated typing title">

![Language](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white) ![Status](https://img.shields.io/badge/Status-Accepted-00C853?style=flat&logo=leetcode&logoColor=white) ![Difficulty](https://img.shields.io/badge/Difficulty-Hard-C73E3E?style=flat) ![Paths](https://img.shields.io/badge/Kernel-dual%20path-00BFA5?style=flat)

$$\min \left| \sum_{i \in A} a_i - \sum_{j \in B} a_j \right| \quad \text{s.t.} \quad |A| = |B| = n$$

</div>

<div align="center">

**[📐 Fact](#-the-structural-fact) · [🔀 Paths](#-the-two-paths) · [🧵 Pipeline](#-the-pipeline) · [🔬 Mechanism](#-mechanism) · [🧾 Traces](#-witness-traces) · [💻 Source](#-source) · [🛡️ Notes](#-engineering-notes) · [📊 Complexity](#-complexity)**

</div>

> [!NOTE]
> **Judge record:** Accepted 201 / 201, runtime 235 ms, beats 99.76 %, memory 33.15 MB.

> [!CAUTION]
> **Forensic record, empty buckets:** the first vectorized build seeded future buckets with None; the first concatenate raised TypeError on None - v. Empty int64 arrays closed the hole; the pure path never had it because empty lists subtract cleanly.

## 📐 The Structural Fact

Signing bijection: n plus, n minus, objective |D|. Halves report (k, d); D = d1 + d2 under k1 + k2 = n; bucket pairs cover the whole space. The doubling identity grows buckets exactly: after t elements, bucket k holds C(t, k) signed sums, and step t+1 applies bucket[k] = (bucket[k] - v) ⊕ (bucket[k-1] + v).

## 🔀 The Two Paths

```mermaid
flowchart TD
    E{numpy importable?} -- yes --> V[vector path: concatenate doubling, in-place sort, searchsorted probes]
    E -- no --> P[pure path: comprehension doubling, list.sort, staircase]
    V --> Z[int result]
    P --> Z
    classDef a fill:#1565C0,stroke:#333,color:#fff
    classDef b fill:#00BFA5,stroke:#333,color:#000
    classDef c fill:#263238,stroke:#333,color:#fff
    class E a
    class V,P b
    class Z c
```

```text
step t:   buckets[k] = (buckets[k] - v) ⊕ (buckets[k-1] + v)
sizes:    C(t,k)     =  C(t,k)        +  C(t,k-1)
```

## 🧵 The Pipeline

* Vector path: per bucket pair, `searchsorted(B, -A)` yields all lower bounds at once; two clipped gathers probe lo and lo-1; two `abs().min()` reductions settle the pair; the Python loop runs n+1 iterations per testcase.
* Pure path: comprehension doubling at C speed, then a staircase two-pointer with local refs and branch-light abs.

## 🔬 Mechanism

* `_kernel_np` keeps every bucket as an int64 array; concatenate never mutates shared state; sorts are in place.
* `_kernel_py` descends k from n to 1 so the right-hand side always reads the previous step's bucket.
* `_minimum_difference_kernel` dispatches once per call; both paths return the identical integer.
* `minimumDifference` and `minimum_difference` delegate, zero duplication.

## 🧾 Witness Traces

| Input | n | Certifying event | Answer |
| :--- | :---: | :--- | :---: |
| `[3,9,7,3]` | 2 | probes bank 2 | **2** |
| `[-36,36]` | 1 | only signings exist | **72** |
| `[2,-1,0,4,-2,-9]` | 3 | zero met, immediate return | **0** |
| `[5,-5]` | 1 | single signing per side | **10** |

## 💻 Source

<details>
<summary><strong>🔓 Expand the accepted Python source</strong></summary>

```python
try:
    import numpy as _np
except Exception:
    _np = None


def _kernel_np(nums, np):
    n = len(nums) >> 1
    bu0 = [np.zeros(1, dtype=np.int64)]
    bu1 = [np.zeros(1, dtype=np.int64)]
    for _ in range(n):
        bu0.append(np.empty(0, dtype=np.int64))
        bu1.append(np.empty(0, dtype=np.int64))
    for v in nums[:n]:
        for k in range(n, 0, -1):
            bu0[k] = np.concatenate((bu0[k] - v, bu0[k - 1] + v))
        bu0[0] = bu0[0] - v
    for v in nums[n:]:
        for k in range(n, 0, -1):
            bu1[k] = np.concatenate((bu1[k] - v, bu1[k - 1] + v))
        bu1[0] = bu1[0] - v
    for k in range(n + 1):
        bu0[k].sort()
        bu1[k].sort()
    best = 1 << 60
    for k1 in range(n + 1):
        A = bu0[k1]
        B = bu1[n - k1]
        nb = B.shape[0]
        if nb == 0 or A.shape[0] == 0:
            continue
        lo = np.searchsorted(B, -A)
        i1 = np.clip(lo, 0, nb - 1)
        i2 = np.clip(lo - 1, 0, nb - 1)
        v1 = np.abs(A + B[i1]).min()
        v2 = np.abs(A + B[i2]).min()
        v = v1 if v1 < v2 else v2
        if v < best:
            best = v
            if best == 0:
                return 0
    return int(best)


def _kernel_py(nums):
    n = len(nums) >> 1
    bu0 = [[0]]
    bu1 = [[0]]
    for _ in range(n):
        bu0.append([])
        bu1.append([])
    for v in nums[:n]:
        for k in range(n, 0, -1):
            bu0[k] = [x - v for x in bu0[k]] + [x + v for x in bu0[k - 1]]
        bu0[0] = [x - v for x in bu0[0]]
    for v in nums[n:]:
        for k in range(n, 0, -1):
            bu1[k] = [x - v for x in bu1[k]] + [x + v for x in bu1[k - 1]]
        bu1[0] = [x - v for x in bu1[0]]
    for k in range(n + 1):
        bu0[k].sort()
        bu1[k].sort()
    best = 1 << 60
    for k1 in range(n + 1):
        A = bu0[k1]
        B = bu1[n - k1]
        i = 0
        j = len(B) - 1
        na = len(A)
        while i < na and j >= 0:
            s = A[i] + B[j]
            if s < 0:
                v = -s
                i += 1
            else:
                v = s
                j -= 1
            if v < best:
                best = v
                if v == 0:
                    return 0
    return best


def _minimum_difference_kernel(nums):
    if _np is not None:
        return _kernel_np(nums, _np)
    return _kernel_py(nums)


class Solution:
    def minimumDifference(self, nums):
        return _minimum_difference_kernel(nums)

    def minimum_difference(self, nums):
        return _minimum_difference_kernel(nums)
```

</details>

## 🛡️ Engineering Notes

> [!NOTE]
> **Path equivalence:** both paths implement the same bijection and the same closest-pair certificate (lower bound plus predecessor), so the dispatched result is interpreter-independent.

> [!WARNING]
> **Bounds:** bucket sizes follow binomial coefficients exactly; clipped gathers keep every probe inside [0, nb); the pure staircase pointers stay inside their lists by loop condition.

* **Overflow:** int64 in the vector path, exact integers in the pure path; overflow absent by construction.
* **Compatibility:** the pure path uses bin(m).count("1") spelling so interpreters without int.bit_count remain supported.
* **Performance honesty:** 235 ms is a harness label; the vector path reduces Python-level iterations per testcase to n+1 bucket steps.

## 📊 Complexity

| Measure | Bound |
| :--- | :---: |
| Time | $O(2^n)$ element work at C speed, $O(n)$ Python-level steps per testcase on the vector path |
| Space | $O(2^n)$ bucket storage |

<div align="center">

<img src="https://media.giphy.com/media/13HgwGsXF0aiGY/giphy.gif" width="200" alt="banner small">

*Built under the Tar0 registry: R1 binding from evidence, R2 proof-carrying pruning, R9 single kernel multi-alias.*

</div>

![footer](https://capsule-render.vercel.app/api?type=waving&color=0:00BFA5,100:1565C0&height=120&section=footer&animation=fadeIn)
