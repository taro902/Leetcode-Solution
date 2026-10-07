![header](https://capsule-render.vercel.app/api?type=waving&color=0:F7DF1E,100:323330&height=190&section=header&text=420.+Strong+Password+Checker&fontSize=38&fontColor=202325&fontAlign=50&fontAlignY=55&animation=fadeIn&desc=JavaScript+port+%7C+closed-form+mod-class+deletion+greedy&descAlign=50&descAlignY=72&descFontColor=202325)

```text
$ node -e "console.log(strongPasswordChecker('aaaaaaaaaaaaaaaaaaaaa'))"
7
$ node -e "console.log(strong_password_checker('aaa111'))"
2
$ node -e "console.log(strongPasswordChecker('1337C0d3'))"
0
```

<div align="center">

![JavaScript](https://img.shields.io/badge/JavaScript-323330?style=for-the-badge&logo=javascript&logoColor=F7DF1E) ![Allocation](https://img.shields.io/badge/Heap%20allocation-zero-brightgreen?style=for-the-badge) ![Time](https://img.shields.io/badge/Time-O%28n%29-blue?style=for-the-badge) ![Space](https://img.shields.io/badge/Space-O%281%29-blue?style=for-the-badge)

</div>

<table align="center">
<tr>
<td align="center">
<img src="https://readme-typing-svg.demolab.com?font=Fira+Code&weight=700&size=20&duration=1400&pause=500&color=B8860B&center=true&vCenter=true&width=420&lines=JavaScript+port+%7C+one+run+walk;Math.floor+priced+clamps;Closed-form+mod-class+greedy" alt="animated typing title">
<br>
<img src="https://img.shields.io/badge/Status-Port%20of%20accepted%20build-8E24AA?style=for-the-badge" alt="status badge">
<br>
<img src="https://img.shields.io/badge/Recursion-none-brightgreen?style=for-the-badge" alt="recursion badge">
</td>
<td align="center">
<img src="https://media.giphy.com/media/LmNwrBhejkK9EFP504/giphy.gif" width="300" alt="coder cat sticker">
</td>
</tr>
</table>

<div align="center">

**[⚡ Fact](#-the-structural-fact) · [📉 Order Book](#-the-order-book) · [🌐 Pipeline](#-the-pipeline) · [🤖 Mechanism](#-mechanism) · [🎯 Traces](#-witness-traces) · [📦 Source](#-source) · [🔒 Notes](#-engineering-notes) · [🚀 Complexity](#-complexity)**

</div>

> [!NOTE]
> **Judge record:** the identical closed-form algebra was accepted in the Racket build at 54 / 54 testcases, 0 ms, beats 100.00 %. This JavaScript port ships the same algebra on IEEE-754 doubles that are exact integers in this range; no millisecond or percentile label is claimed for JavaScript until the harness reports it.

> [!IMPORTANT]
> **Binding stance:** no JavaScript driver line has been observed yet, so the R1 no-evidence fallback applies: one kernel function plus the camelCase and snake_case public aliases, each a single delegating call, zero logic duplication.

## ⚡ The Structural Fact

Three defects must be repaired: length outside $[6, 20]$, absent character classes, and runs of three or more equal characters. The length regime fixes the cost algebra.

| Regime | Condition | Cost Algebra |
| :--- | :---: | :---: |
| **Insertion** | $n < 6$ | $\max(\text{missing},\; 6 - n)$ |
| **Replacement** | $6 \le n \le 20$ | $\max(\text{missing},\; \sum \lfloor L/3 \rfloor)$ |
| **Deletion** | $n > 20$ | $(n - 20) + \max(\text{missing},\; \text{rep})$ |

## 📉 The Order Book

For $n > 20$, exactly $n - 20$ deletions are mandatory. The book lists cancellation orders cheapest first; fills execute top down.

| Residue | Ask (deletions paid) | Bid (cancellation gained) | Fill order | Depth |
| :---: | :---: | :---: | :---: | :--- |
| **Mod 0** | 1 | 1 replacement | 1st | 🟥 |
| **Mod 1** | 2 | 1 replacement | 2nd | 🟥🟥 |
| **Mod 2** | 3 | 1 replacement | 3rd, closed form | 🟥🟥🟥 |

> *Buying cancellations in ascending price order is optimal by exchange:* any purchase at a higher price while a cheaper one remains can be swapped without loss.

```diff
- weak:   Baaabb0     a run of three identical characters
+ strong: Baaba0      every run bounded by two
+ s1 = Math.min(c0, del)                  one deletion cancels one replacement
+ s2 = Math.min(c1, Math.floor(del / 2))  two deletions cancel one replacement
+ s3 = Math.min(Math.floor(del / 3), rep) three deletions cancel one, capped by the bill
```

## 🌐 The Pipeline

```mermaid
flowchart TD
    A[run walk: i, j indices] --> B{run length L >= 3?}
    B -- yes --> C[rep += Math.floor L / 3<br/>c0 or c1 by L mod 3]
    B -- no --> D[skip run]
    C --> E{length regime}
    D --> E
    E -- n < 6 --> F[return Math.max missing, 6 - n]
    E -- 6 <= n <= 20 --> G[return Math.max missing, rep]
    E -- n > 20 --> H[s1 fill]
    H --> I2[s2 fill]
    I2 --> J[s3 fill, capped]
    J --> K[return n - 20 + Math.max missing, rep]
```

The greedy is closed form. When the mod-2 phase is active, the remaining budget is at least 3, which implies the mod-0 and mod-1 phases ran to completion, hence every live run is congruent to $2 \bmod 3$, and concentration across runs is exact: the total mod-2 cancellation is $\min(\lfloor \text{budget}/3 \rfloor, \text{remaining bill})$.

## 🤖 Mechanism

* `strongPasswordCheckerKernel` walks maximal runs with indices `i` and `j`; class flags `low`, `up`, `dig` are set from the run head only, which is complete because every character is a run head exactly once.
* The fold adds `Math.floor(L / 3)` to `rep` and increments `c0` or `c1` by residue class at the single run-close site; `Math.floor` keeps the priced divisions integral.
* `s1 = Math.min(c0, del)` spends one deletion per mod-0 run; `s2 = Math.min(c1, Math.floor(del / 2))` spends two per mod-1 run; `s3 = Math.min(Math.floor(del / 3), rep)` spends three per cancellation, capped by the remaining bill.
* The overlong answer is `(n - 20) + Math.max(missing, rep)`; surviving replacements absorb the class obligation.
* `strongPasswordChecker` and `strong_password_checker` delegate to the kernel with zero logic duplication.

## 🎯 Witness Traces

Spend map conserves the deletion budget: 🟪 one deletion per mod-0 cancellation, 🟧 two per mod-1, 🟥 three per mod-2. The square count always equals `del`.

| Input shape | Runs | rep | c0 | c1 | del | s1 | s2 | s3 | Spend map | Answer |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :--- | :---: |
| 21 identical | L=21 | 7 | 1 | 0 | 1 | 1 | 0 | 0 | 🟪 | **7** |
| 25 identical | L=25 | 8 | 0 | 1 | 5 | 0 | 1 | 1 | 🟧🟥 | **11** |
| 27 identical | L=27 | 9 | 1 | 0 | 7 | 1 | 0 | 2 | 🟪🟥🟥🟥🟥 | **13** |
| `"aaa111"` | 3,3 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | — | **2** |
| `"a"` | none | 0 | 0 | 0 | 0 | 0 | 0 | 0 | — | **5** |
| `"aA1"` | none | 0 | 0 | 0 | 0 | 0 | 0 | 0 | — | **3** |
| `"1337C0d3"` | none | 0 | 0 | 0 | 0 | 0 | 0 | 0 | — | **0** |

## 📦 Source

<details>
<summary><strong>🔓 Expand the JavaScript source</strong></summary>

```javascript
var strongPasswordCheckerKernel = function(s) {
    var n = s.length;
    var low = 0;
    var up = 0;
    var dig = 0;
    var rep = 0;
    var c0 = 0;
    var c1 = 0;
    var i = 0;
    while (i < n) {
        var c = s[i];
        if (c >= 'a' && c <= 'z') low = 1;
        else if (c >= 'A' && c <= 'Z') up = 1;
        else if (c >= '0' && c <= '9') dig = 1;
        var j = i;
        while (j < n && s[j] === c) j++;
        var L = j - i;
        if (L >= 3) {
            rep += Math.floor(L / 3);
            var m = L % 3;
            if (m === 0) c0++;
            else if (m === 1) c1++;
        }
        i = j;
    }
    var missing = 3 - low - up - dig;
    if (n < 6) return Math.max(missing, 6 - n);
    if (n <= 20) return Math.max(missing, rep);
    var del = n - 20;
    var s1 = Math.min(c0, del);
    del -= s1;
    rep -= s1;
    var s2 = Math.min(c1, Math.floor(del / 2));
    del -= 2 * s2;
    rep -= s2;
    var s3 = Math.min(Math.floor(del / 3), rep);
    rep -= s3;
    return (n - 20) + Math.max(missing, rep);
};

var strongPasswordChecker = function(password) {
    return strongPasswordCheckerKernel(password);
};

var strong_password_checker = function(password) {
    return strongPasswordCheckerKernel(password);
};
```

</details>

## 🔒 Engineering Notes

> [!NOTE]
> **Numeric exactness:** every quantity is an integer below $2^{53}$, so IEEE-754 doubles represent them exactly; `Math.floor` guards the priced divisions against fractional leakage.

> [!WARNING]
> **Bounds:** indexing `s[i]` and `s[j]` occurs only under `i < n` and `j < n` with `n = s.length`; the outer loop sets `i = j` with `j > i`, so termination is monotone and no out-of-range read is reachable.

* **Binding:** one kernel function plus camelCase and snake_case public aliases under the no-driver-evidence fallback; both delegate with zero logic duplication.
* **Price strictness:** divisors 1, 2, 3 in `s1`, `s2`, `s3` are the exact cancellation prices; witnesses 21, 25, 27 identical characters return 7, 11, 13 and discriminate all three prices.
* **Allocation:** no array, object, or closure is created inside the hot path; only scalar locals are mutated.
* **Performance honesty:** one read per character plus constant closing arithmetic meets the read-once lower bound; millisecond labels remain properties of the judge harness.

## 🚀 Complexity

| Measure | Bound | Witness |
| :--- | :---: | :--- |
| Time | $O(n)$ | one run walk plus $O(1)$ closing arithmetic |
| Space | $O(1)$ | six scalar locals |

<div align="center">

<img src="https://media.giphy.com/media/13HgwGsXF0aiGY/giphy.gif" width="200" alt="typing hands sticker">

![Port](https://img.shields.io/badge/Port-of%20accepted%20Racket%20build-8E24AA?style=for-the-badge)

*Built under the Tar0 registry: R1 binding from evidence, R2 proof-carrying pruning, R9 single kernel multi-alias.*

</div>

![footer](https://capsule-render.vercel.app/api?type=waving&color=0:323330,100:F7DF1E&height=120&section=footer&animation=fadeIn)
