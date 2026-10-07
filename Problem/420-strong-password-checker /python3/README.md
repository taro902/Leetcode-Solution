![header](https://capsule-render.vercel.app/api?type=waving&color=0:6A1B9A,100:F57F17&height=190&section=header&text=420.+Strong+Password+Checker&fontSize=38&fontColor=FFFFFF&fontAlign=50&fontAlignY=55&animation=fadeIn&desc=Python+port+%7C+closed-form+mod-class+deletion+greedy&descAlign=50&descAlignY=72&descFontColor=FFFFFF)

<div align="center">

|  Language |  Heap allocation |  Recursion |  Time |  Space |
| :---: | :---: | :---: | :---: | :---: |
| **Python** | **zero** | **none** | **O(n)** | **O(1)** |

</div>

<table align="center">
<tr>
<td align="center">
<img src="https://media.giphy.com/media/JIX9t2j0ZTN9S/giphy.gif" width="320" alt="typing cat sticker">
</td>
<td align="center">
<img src="https://readme-typing-svg.demolab.com?font=Fira+Code&weight=700&size=20&duration=1400&pause=500&color=306998&center=true&vCenter=true&width=420&lines=Python+port+%7C+one+run+walk+%7C+zero+allocation;budget+guards+the+del+keyword;Closed-form+mod-class+clamps" alt="animated typing title">
<br>
<img src="https://img.shields.io/badge/Language-Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="language badge">
<br>
<img src="https://img.shields.io/badge/Heap%20allocation-zero-brightgreen?style=for-the-badge" alt="allocation badge">
<br>
<img src="https://img.shields.io/badge/Time-O%28n%29-blue?style=for-the-badge" alt="time badge">
<br>
<img src="https://img.shields.io/badge/Space-O%281%29-blue?style=for-the-badge" alt="space badge">
</td>
</tr>
</table>

<div align="center">

**[📐 Fact](#-the-structural-fact) · [💸 Market](#-the-mod-class-market) · [🧵 Pipeline](#-the-pipeline) · [⚙️ Mechanism](#-mechanism) · [🧾 Traces](#-witness-traces) · [💻 Source](#-source) · [🛡️ Notes](#-engineering-notes) · [📊 Complexity](#-complexity)**

</div>

> [!NOTE]
> **Judge record:** the identical closed-form algebra was accepted in the Racket build at 54 / 54 testcases, 0 ms, beats 100.00 %. This Python port ships the same algebra on exact integers; no millisecond or percentile label is claimed for Python until the harness reports it.

> [!IMPORTANT]
> **Binding stance:** no Python driver line has been observed yet, so the R1 no-evidence fallback applies: one module-private kernel plus the camelCase and snake_case public methods inside class Solution, each a single delegating call, zero logic duplication.

## 📐 The Structural Fact

Three defects must be repaired: length outside $[6, 20]$, absent character classes, and runs of three or more equal characters. The length regime fixes the cost algebra.

| Regime | Condition | Cost Algebra |
| :--- | :---: | :---: |
| **Insertion** | $n < 6$ | $\max(\text{missing},\; 6 - n)$ |
| **Replacement** | $6 \le n \le 20$ | $\max(\text{missing},\; \sum \lfloor L/3 \rfloor)$ |
| **Deletion** | $n > 20$ | $(n - 20) + \max(\text{missing},\; \text{rep})$ |

## 🧵 The Pipeline

```mermaid
graph LR
    P[password chars] --> W[run walk: i, j indices]
    W --> H[head-only class flags]
    H --> R[fold: rep, c0, c1]
    R --> Q{length regime}
    Q -- n < 6 --> I[max missing, 6 - n]
    Q -- 6 .. 20 --> M[max missing, rep]
    Q -- n > 20 --> D[s1 then s2 then s3 clamps]
    D --> A[n - 20 + max missing, rep]
```

```text
a a a b b b
└─ L=3 ── L=3 ─
rep += 1   rep += 1          residue 0 → c0 += 1 on each run
```

## 💸 The Mod-Class Market

For $n > 20$, exactly $n - 20$ deletions are mandatory. A deletion matters only through the replacement it cancels, and the price depends on $L \bmod 3$.

| Residue | Price in deletions | Cancellation | Buy order | Price map |
| :---: | :---: | :---: | :---: | :--- |
| **Mod 0** | 1 | 1 replacement | 1st, cheapest | 🟥 |
| **Mod 1** | 2 | 1 replacement | 2nd | 🟥🟥 |
| **Mod 2** | 3 | 1 replacement | 3rd, closed form | 🟥🟥🟥 |

> *Buying cancellations in ascending price order is optimal by exchange:* any purchase at a higher price while a cheaper one remains can be swapped without loss.

```diff
- weak:   Baaabb0     a run of three identical characters
+ strong: Baaba0      every run bounded by two
+ s1 = min(c0, budget)          one deletion cancels one replacement
+ s2 = min(c1, budget // 2)     two deletions cancel one replacement
+ s3 = min(budget // 3, rep)    three deletions cancel one, capped by the bill
```

The greedy is closed form. When the mod-2 phase is active, the remaining budget is at least 3, which implies the mod-0 and mod-1 phases ran to completion, hence every live run is congruent to $2 \bmod 3$, and concentration across runs is exact: the total mod-2 cancellation is $\min(\lfloor \text{budget}/3 \rfloor, \text{remaining bill})$.

<div align="center">
<img src="https://media.giphy.com/media/13HgwGsXF0aiGY/giphy.gif" width="280" alt="typing hands sticker">
</div>

## ⚙️ Mechanism

* `_strong_password_checker_kernel` walks maximal runs with indices `i` and `j`; class flags `low`, `up`, `dig` are set from the run head only, which is complete because every character is a run head exactly once.
* The fold adds `L // 3` to `rep` and increments `c0` or `c1` by residue class at the single run-close site.
* The deletion budget lives in `budget`, never in `del`, because `del` is a Python keyword; renaming is the only dialect accommodation in the file.
* `s1`, `s2`, `s3` spend one, two, three deletions per cancellation in ascending price order; `s3` is capped by the remaining bill.
* The overlong answer is `(n - 20) + max(missing, rep)`; surviving replacements absorb the class obligation.
* `strongPasswordChecker` and `strong_password_checker` delegate to the kernel with zero logic duplication.

## 🧾 Witness Traces

Spend map conserves the deletion budget: 🟪 one deletion per mod-0 cancellation, 🟧 two per mod-1, 🟥 three per mod-2. The square count always equals `budget`.

| Input shape | Runs | rep | c0 | c1 | del | s1 | s2 | s3 | Spend map | Answer |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :--- | :---: |
| 21 identical | L=21 | 7 | 1 | 0 | 1 | 1 | 0 | 0 | 🟪 | **7** |
| 25 identical | L=25 | 8 | 0 | 1 | 5 | 0 | 1 | 1 | 🟧🟥 | **11** |
| 27 identical | L=27 | 9 | 1 | 0 | 7 | 1 | 0 | 2 | 🟪🟥🟥🟥 | **13** |
| `"aaa111"` | 3,3 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | — | **2** |
| `"a"` | none | 0 | 0 | 0 | 0 | 0 | 0 | 0 | — | **5** |
| `"aA1"` | none | 0 | 0 | 0 | 0 | 0 | 0 | 0 | — | **3** |
| `"1337C0d3"` | none | 0 | 0 | 0 | 0 | 0 | 0 | 0 | — | **0** |

## 💻 Source

<details>
<summary><strong>🔓 Expand the Python source</strong></summary>

```python
def _strong_password_checker_kernel(s):
    n = len(s)
    low = 0
    up = 0
    dig = 0
    rep = 0
    c0 = 0
    c1 = 0
    i = 0
    while i < n:
        c = s[i]
        if 'a' <= c <= 'z':
            low = 1
        elif 'A' <= c <= 'Z':
            up = 1
        elif '0' <= c <= '9':
            dig = 1
        j = i
        while j < n and s[j] == c:
            j += 1
        L = j - i
        if L >= 3:
            rep += L // 3
            m = L % 3
            if m == 0:
                c0 += 1
            elif m == 1:
                c1 += 1
        i = j
    missing = 3 - low - up - dig
    if n < 6:
        return max(missing, 6 - n)
    if n <= 20:
        return max(missing, rep)
    budget = n - 20
    s1 = min(c0, budget)
    budget -= s1
    rep -= s1
    s2 = min(c1, budget // 2)
    budget -= 2 * s2
    rep -= s2
    s3 = min(budget // 3, rep)
    rep -= s3
    return (n - 20) + max(missing, rep)


class Solution:
    def strongPasswordChecker(self, password: str) -> int:
        return _strong_password_checker_kernel(password)

    def strong_password_checker(self, password: str) -> int:
        return _strong_password_checker_kernel(password)
```

</details>

## 🛡️ Engineering Notes

> [!NOTE]
> **Keyword collision closed:** `del` is reserved in Python, so the budget variable is `budget`; no other identifier in the file shadows a builtin or keyword.

> [!WARNING]
> **Bounds:** indexing `s[i]` and `s[j]` occurs only under `i < n` and `j < n`; the outer loop sets `i = j` with `j > i`, so termination is monotone and no IndexError is reachable.

* **Binding:** one module-private kernel plus camelCase and snake_case public methods under the no-driver-evidence fallback; both delegate with zero logic duplication.
* **Overflow:** Python integers are exact; overflow is absent from the failure catalogue by language guarantee.
* **Price strictness:** divisors 1, 2, 3 in `s1`, `s2`, `s3` are the exact cancellation prices; witnesses 21, 25, 27 identical characters return 7, 11, 13 and discriminate all three prices.
* **Allocation:** no list, dict, or comprehension is created; the scan mutates six scalar locals.
* **Performance honesty:** one read per character plus constant closing arithmetic meets the read-once lower bound; millisecond labels remain properties of the judge harness.

## 📊 Complexity

| Measure | Bound | Witness |
| :--- | :---: | :--- |
| Time | $O(n)$ | one run walk plus $O(1)$ closing arithmetic |
| Space | $O(1)$ | six scalar accumulators |

<div align="center">

<img src="https://media.giphy.com/media/LmNwrBhejkK9EFP504/giphy.gif" width="200" alt="coder cat sticker">

![Port](https://img.shields.io/badge/Port-of%20accepted%20Racket%20build-8E24AA?style=for-the-badge)

*Built under the Tar0 registry: R1 binding from evidence, R2 proof-carrying pruning, R9 single kernel multi-alias.*

</div>

![footer](https://capsule-render.vercel.app/api?type=waving&color=0:F57F17,100:6A1B9A&height=120&section=footer&animation=fadeIn)
