<p align="center">
  <img src="https://readme-typing-svg.demolab.com/?font=JetBrains+Mono&size=21&duration=3200&pause=800&color=F7DF1E&center=true&vCenter=true&width=880&lines=10+%C2%B7+Regular+Expression+Matching;JavaScript+lane+%C2%B7+DP+rows+as+single+Smi+integers;4+ms+%C2%B7+54.07+MB+%C2%B7+354%2F354" alt="typing line"/>
</p>

<h1 align="center">Regular Expression Matching</h1>

<p align="center">
  <sub>LeetCode 10 · Hard · prefix DP whose entire table lives in two 31-bit integers · zero allocation per call · two receipts filed below</sub>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/LeetCode-10%20%C2%B7%20Hard-f7df1e?style=flat-square&logo=leetcode&logoColor=000000" alt="problem"/>
  <img src="https://img.shields.io/badge/JavaScript-ES2020-f7df1e?style=flat-square&logo=javascript&logoColor=000000" alt="language"/>
  <img src="https://img.shields.io/badge/Accepted-354%2F354-1a7f37?style=flat-square" alt="verdict"/>
  <img src="https://img.shields.io/badge/Runtime-4%20ms%20%C2%B7%2084.32%25-444444?style=flat-square" alt="runtime"/>
  <img src="https://img.shields.io/badge/Memory-54.07%20MB%20%C2%B7%2090.73%25-2b2b2b?style=flat-square" alt="memory"/>
  <img src="https://img.shields.io/badge/Proof-Oct%2011%2C%202026%2012%3A51-444444?style=flat-square" alt="proof"/>
</p>

<p align="center">
  <a href="https://i.ibb.co.com/DDdpzpwJ/image.png">
    <img src="https://i.ibb.co.com/DDdpzpwJ/image.png" width="72%" alt="judge panel, Oct 11 2026 12:51"/>
  </a>
  <br/>
  <sub>the judge panel for the live build, verbatim · click for full resolution</sub>
</p>

---

## Contents

- [Two receipts, one quantization](#two-receipts-one-quantization)
- [The problem](#the-problem)
- [The recurrence](#the-recurrence)
- [Anatomy of the kernel](#anatomy-of-the-kernel)
- [What V8 actually does with this](#what-v8-actually-does-with-this)
- [Trace, rows as bit patterns](#trace-rows-as-bit-patterns)
- [Cost](#cost)
- [Guards and limits](#guards-and-limits)
- [Source](#source)
- [Repo conventions](#repo-conventions)

---

## Two receipts, one quantization

| Build | Table representation | Runtime | Beat | Memory | Beat | Submitted |
| :-- | :-- | :-- | :-- | :-- | :-- | :-- |
| v1 | flat `Uint8Array(441)` byte table | 4 ms | 84.32% | 54.41 MB | 84.65% | Oct 11 2026, 12:36 |
| v2 (live, this folder) | two Smi integers, one per row | 4 ms | 84.32% | 54.07 MB | 90.73% | Oct 11 2026, 12:51 · [panel](https://i.ibb.co.com/DDdpzpwJ/image.png) |

Read the pair carefully, because it teaches something about the instrument rather than the program. The two kernels differ by an order of magnitude in actual work: v1 writes and reads 441 table bytes and indexes strings inside the hot loop, allocating a one-character string per index; v2 never touches a string in the hot loop and keeps the whole table in two registers. Their runtime labels are identical to the hundredth of a percent. A label that cannot distinguish tenfold less work is not measuring the work. It is measuring the harness floor: 354 testcases each carry a fixed judge-side cost of string handoff and timer bookkeeping, and 354 times that cost lands near four milliseconds no matter what the kernel does. The same lane recorded a 0 ms label on problem 420, where the case count is 54 and the floor sits below one millisecond; the difference between the two labels is the case count, not the language and not the algorithm.

The memory label behaves oppositely, and that is the half of the instrument that still listens. Removing per-cell string allocation moved residency from 54.41 to 54.07 MB and the percentile from 84.65 to 90.73. Residency integrates garbage over the whole run, so it responds to allocation the way runtime here cannot. What remains in the 54.07 MB is V8 process baseline: heap, code space, and runtime structures that exist before user code loads. This kernel adds two 84-byte typed arrays to that process and nothing per call, so the residue below 90.73% is lighter VM starts on shared silicon, not leaner programs.

---

## The problem

Given a string `s` and a pattern `p`, decide whether `p` matches all of `s`, not a prefix of it. Two wildcards exist: `.` stands for any single character, and `*` stands for zero or more repetitions of the element immediately before it. The star binds backward, may vanish, and may consume an unbounded run, so greedy left-to-right scanning cannot decide anything: consuming now and saving the star for later are both legal, and only the suffix knows which was right. Prefix dynamic programming removes the prophecy.

---

## The recurrence

Let `dp[i][j]` mean that the first `i` characters of `s` match the first `j` characters of `p`. The answer is `dp[n][m]`. A cell inspects the last pattern character, `p[j-1]`:

- **Literal or dot.** It must consume exactly one character of `s`: `dp[i][j] = i >= 1 && dp[i-1][j-1] && (p[j-1] == '.' || p[j-1] == s[i-1])`.
- **Star.** Two disjoint lives, OR-ed. Zero uses: the pair `x*` collapses and the cell inherits `dp[i][j-2]`, needing `j >= 2`. One or more uses: the star eats one character of `s` against `p[j-2]` and stays alive: `(p[j-2] == '.' || p[j-2] == s[i-1]) && dp[i-1][j]`, needing `i >= 1`.
- **Base.** `dp[0][0] = true`; the rest of column zero is false.

The OR is exhaustive, not heuristic: a match either never exercises the star, which is the `j-2` case, or exercises it at least once, and peeling the last consumed character leaves a match of `s[0..i-1)` against the same `j`, which is the `i-1` case. No third shape exists. Every right-hand side references only `(i, j-2)`, `(i-1, j)`, or `(i-1, j-1)`, all earlier in row-major order, so one ascending sweep per row settles every cell.

---

## Anatomy of the kernel

**Character codes, hoisted out of the hot loop.** In v1 the expression `p[j-1]` inside the cell loop allocated a one-character string on every evaluation, thousands of times per testcase, 354 testcases deep. v2 calls `charCodeAt` exactly `n + m <= 40` times per call, before any loop, and stores the numeric codes in two module-scope `Int32Array(21)` buffers, `PC` and `SC`. The hot loop then compares plain numbers: 42 for `*`, 46 for `.`, and character equality as integer equality. A sentinel of `-1` stands in for the absent character on row zero, where no `s` character may be read at all.

**The table is two integers.** Constraints cap `m` at 20, so one row of the table is 21 booleans, which fit in 21 bits of a single V8 Smi. The kernel keeps `cur`, the row under construction, and `prev`, the row above it. Reading `dp[i][j-2]` is `(cur >>> (j-2)) & 1`, a shift of the register being built; reading `dp[i-1][j]` or `dp[i-1][j-1]` is a shift of `prev`. Writing a cell is `cur |= (1 << j)`. The 441-byte table of the C and Java lanes collapses to two 31-bit values that never leave registers, and with the table gone, the question of clearing it between testcases disappears entirely: there is no storage left to go stale.

**Branch order follows cost.** The star's zero-use life is a shift and an AND on `cur`, tested first. The consume-one life sits behind `i >= 1 && j >= 2`, so row zero and the impossible front-star case never reach a character comparison. The literal life tests the length guard and the `prev` bit before loading any character code, so a dead prefix costs one shift.

**Two names, one body.** `isMatch` and `is_match` are one-expression thunks over the private `kernel_10`, covering whichever spelling a driver emits. The logic exists once.

```mermaid
flowchart TD
    A["charCodeAt hoisted: PC and SC filled, 40 calls total"] --> B["row loop i in 0..n"]
    B --> C["cur seeded: bit 0 set iff i == 0; sc hoisted per row"]
    C --> D["column loop j in 1..m over PC codes"]
    D --> E{"PC[j-1] == 42"}
    E -- yes --> F["zero-use: bit j-2 of cur"]
    F -- false --> G["consume-one: PC[j-2] vs sc, bit j of prev"]
    E -- no --> H["literal: bit j-1 of prev, PC[j-1] vs sc"]
    F --> I["set bit j of cur if v"]
    G --> I
    H --> I
    I --> D
    D --> J["prev = cur, next row"]
    J --> K["return bit m of prev"]
```

---

## What V8 actually does with this

Every value in the hot loop is a Smi: row masks, shift counts, character codes loaded from `Int32Array`. Smis are unboxed 31-bit values tagged in the pointer itself, so `>>>`, `&`, `|`, and `<<` here compile to single machine instructions with no heap object involved at any step. The two typed arrays are fixed-length external-style buffers whose loads C2 emits as raw memory reads with the bounds check hoisted, because the loop bounds are provable against the constant length 21. `charCodeAt` on the judge's one-byte strings is a byte load plus a coder check, executed forty times per call outside every loop. Steady state allocates nothing, so the kernel never appears in a GC pause, and the row loop is small enough to inline wholly into both thunks. What remains at runtime is roughly four hundred forty-one iterations of six integer operations, repeated 354 times, which is the arithmetic behind the quantization argument above: the kernel's share of the four-millisecond label is the small part.

One caveat belongs in the open. `PC` and `SC` are module-scope mutable buffers, so concurrent calls inside one VM would race on them. The judge drives one testcase at a time per worker, which is the contract this file is written against; a parallel harness would make the buffers per-call locals, a one-line change.

---

## Trace, rows as bit patterns

Input `s = "aab"`, `p = "c*a*b"`, so `n = 3`, `m = 5`. Each row printed as the mask the kernel actually holds, bit `j` on the left-to-right scale of the pattern:

```text
row i=0  ""     cur = 0b010101 = 21    bits 0,2,4   both stars vanish against empty
row i=1  "a"    cur = 0b011000 = 24    bits 3,4     'a' consumed literally, then by the star
row i=2  "aa"   cur = 0b010000 = 16    bit  4       the star eats the second 'a'
row i=3  "aab"  cur = 0b100000 = 32    bit  5       'b' consumed literally, corner bit
return bit 5 of prev = 1 -> true
```

The refusals are visible as absent bits. Row 1 never sets bit 2, because the `c*` star cannot eat `a` and its zero-use reads bit 0 of a row whose bit 0 is unset once `i >= 1`. Row 3 never sets bit 4, because the `a*` star cannot eat `b` and its zero-use reads bit 2 of row 2, which row 2 never set. The corner bit survives only through the chain `bit4(row2) -> bit5(row3)`, which is exactly the chain a hand trace of the pattern writes down.

---

## Cost

| Quantity | Bound | At n = m = 20 |
| :-- | :-- | :-- |
| `charCodeAt` calls per testcase | n + m | at most 40 |
| Row iterations | (n+1)·m | at most 441 |
| Operations per iteration | about six integer ops | no loads beyond two typed arrays |
| Allocation per call | none | 0 bytes |
| Static footprint | two `Int32Array(21)` | 168 bytes plus headers |
| Recursion | none | constant stack |

---

## Guards and limits

- **Shift range.** `j <= m <= 20`, so `1 << j` and every `>>>` count stay inside the 31-bit Smi window; no operand ever heap-boxes.
- **Star arithmetic.** Both star lives test `j >= 2` before forming `j - 2`; `i >= 1` gates every read of `SC[i-1]` and every meaningful `prev` bit; row zero seeds bit 0 without touching either code buffer.
- **Buffer bounds.** `PC` and `SC` are indexed at most at 20 inside length-21 arrays, filled by loops bounded by `m` and `n`.
- **Front star.** Forbidden by the problem contract and neutralized by the `j >= 2` guards regardless.
- **Depth and heap.** No recursion and no allocation, so no input can deepen a stack or pressure the collector; the two classic failure shapes of naive matchers have no representation here.
- **Label honesty.** The 4 ms runtime label is harness-quantized at 354 testcases and is filed as such; the memory label is the responsive instrument and is filed with its percentile, not rounded up to a claim.

---

## Source

<details>
<summary><strong>The live kernel as submitted</strong></summary>

```javascript
var PC = new Int32Array(21);
var SC = new Int32Array(21);

var kernel_10 = function(s, p) {
    var n = s.length;
    var m = p.length;
    var k;
    for (k = 0; k < m; k++) PC[k] = p.charCodeAt(k);
    for (k = 0; k < n; k++) SC[k] = s.charCodeAt(k);
    var prev = 0;
    var cur = 0;
    var i;
    var j;
    for (i = 0; i <= n; i++) {
        cur = (i === 0) ? 1 : 0;
        var sc = (i >= 1) ? SC[i - 1] : -1;
        for (j = 1; j <= m; j++) {
            var pcj = PC[j - 1];
            var v = 0;
            if (pcj === 42) {
                if (j >= 2 && ((cur >>> (j - 2)) & 1)) {
                    v = 1;
                } else if (i >= 1 && j >= 2) {
                    var pc2 = PC[j - 2];
                    if (pc2 === 46 || pc2 === sc) {
                        v = (prev >>> j) & 1;
                    }
                }
            } else if (i >= 1 && ((prev >>> (j - 1)) & 1)) {
                if (pcj === 46 || pcj === sc) v = 1;
            }
            if (v) cur |= (1 << j);
        }
        prev = cur;
    }
    return ((prev >>> m) & 1) === 1;
};

var isMatch = function(s, p) {
    return kernel_10(s, p);
};

var is_match = function(s, p) {
    return kernel_10(s, p);
};
```

</details>

---

## Repo conventions

- Judge screenshots are the only evidence; both builds of this lane stay filed so the quantization argument remains checkable.
- One kernel per problem, public names as thunks, logic written once.
- Documents live beside the code they describe and speak only for that code and that runtime.
- When a label cannot distinguish tenfold less work, the document says so plainly instead of claiming the label.

---

<p align="center">
  <img src="https://media.giphy.com/media/3o7aCTfyhYawdOXcFW/giphy.gif" width="320" alt="sticker"/>
</p>

<p align="center">
  <img src="https://ghchart.rshah.org/f7df1e/taro902" width="90%" alt="commit pulse"/>
</p>

<p align="center">
  <img src="https://api.star-history.com/svg?repos=taro902/Leetcode-Solution&type=Date" width="62%" alt="star history"/>
</p>

<p align="center">
  <img src="https://media.giphy.com/media/13HgwGsXF0aiGY/giphy.gif" width="280" alt="sticker"/>
  <br/>
  <img src="https://komarev.com/ghpvc/?username=taro902&label=reads+on+this+dossier&color=f7df1e&style=flat-square" alt="view counter"/>
</p>
