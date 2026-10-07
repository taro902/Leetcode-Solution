<h1 align="center">Leetcode-Solution</h1>

<p align="center"><sub>a field manual of proven algebras — every claim witnessed, every inventory self-counting</sub></p>

<p align="center"><sub>MIT license · five production languages · six accepted harness records · zero fabricated benchmarks</sub></p>

---

> "A solution without a witness is a rumor with indentation."
> — house rule, Tar0 registry

**Contents**

1. [What this repo is](#1-what-this-repo-is)
2. [How to read a dossier](#2-how-to-read-a-dossier)
3. [The map](#3-the-map)
4. [The live vault](#4-the-live-vault)
5. [The flagship lesson](#5-the-flagship-lesson)
6. [Witness discipline](#6-witness-discipline)
7. [Failure-mode catalogue](#7-failure-mode-catalogue)
8. [Receipts](#8-receipts)
9. [Study protocol](#9-study-protocol)

---

## 1. What this repo is

A study room, not an answer dump. Each problem lives in one folder; each language lives in one subfolder; each subfolder holds a dossier and a kernel. The same algebra travels across Racket, C, Java, Python, and JavaScript with zero drift: when a bound changes in one port it changes in all, because the ports are translations of one proof, not five guesses.

What you carry out of here is technique that outlives the problem: run-fold scanning, priced greedy with exchange arguments, regime analysis, online refutation, meet-in-the-middle over bucketed counts, and the habit of naming entry points from evidence instead of from titles.

## 2. How to read a dossier

1. **Structural fact.** Why the algorithm is the only possible one; the invariant and the closure property that make it composable.
2. **Pipeline.** The scan and its accumulators, drawn with the exact variable names you will meet in the source.
3. **Price market.** When a budget exists, its prices tabulated cheapest-first with the exchange argument in one sentence.
4. **Witness traces.** Full arithmetic tables; recompute any cell by hand and catch any lie.
5. **Source.** The kernel: comment-free, single-responsibility, public names delegating to one private kernel.
6. **Failure notes.** Bounds, overflow, sentinel, binding, allocation — each closed with a reason, not a hope.

Read in that order. The order is the pedagogy; jumping straight to the source is reading the verdict before the trial.

## 3. The map

The tree below mirrors the repository at the last commit. Folders first, files after, indentation as the only ornament. It is an instrument reading, not prose; it is never edited by hand.

<!-- AUTO-TREE:START -->
```text
📦 Leetcode-Solution/
├── 📁 .github/
│   └── 📁 workflows/
│       └── ⚙️ auto-atlas.yml
├── 📁 Problem/
│   ├── 📁 2035. Partition Array Into Two Arrays to Minimize Sum Difference/
│   │   ├── 📁 c/
│   │   │   ├── 📖 README.md
│   │   │   └── ⚪ solution.c
│   │   ├── 📁 java/
│   │   │   ├── 📖 README.md
│   │   │   └── 🟠 solution.java
│   │   ├── 📁 javascript/
│   │   │   ├── 📖 README.md
│   │   │   └── 🟡 solution.js
│   │   └── 📁 python/
│   │       ├── 📖 README.md
│   │       └── 🔵 solution.py
│   ├── 📁 2299-strong-password-checker-II/
│   │   └── 📁 c/
│   │       ├── 📖 README.md
│   │       └── ⚪ solution.c
│   └── 📁 420-strong-password-checker /
│       ├── 📁 c/
│       │   ├── 📖 README.md
│       │   └── ⚪ solution.c
│       ├── 📁 Java/
│       │   ├── 📖 README.md
│       │   └── 🟠 solution.java
│       ├── 📁 JavaScript/
│       │   ├── 📖 README.md
│       │   └── 🟡 solution.js
│       ├── 📁 python3/
│       │   ├── 📖 README.md
│       │   └── 🔵 solution.py
│       └── 📁 racket/
│           ├── 📖 README.md
│           └── 🟪 solution.rkt
├── ⚖️ LICENSE
└── 📖 README.md
```

📊 23 files · 16 folders
<!-- AUTO-TREE:END -->

## 4. The live vault

One line per problem. The checkbox ticks the moment a dossier folder exists; the five-square meter fills, language by language, the moment a source file lands anywhere inside that folder. Add a folder or drop a file anywhere and the vault recounts itself in the next commit.

Meter legend: 🟪 Racket · ⚪ C · 🟠 Java · 🟡 JavaScript ·  Python · ⬜ not yet

<!-- AUTO-LEDGER:START -->
- [x] **420 · Strong Password Checker** · 🟪⚪🟠🟡🔵 · 10 files · [dossier](Problem/420-strong-password-checker%20)
- [x] **2035 · Partition Array Into Two Arrays To Minimize Sum Difference** · ⬜⚪🟠🟡🔵 · 8 files · [dossier](Problem/2035.%20Partition%20Array%20Into%20Two%20Arrays%20to%20Minimize%20Sum%20Difference)
- [x] **2299 · Strong Password Checker II** · ⬜⚪⬜⬜⬜ · 2 files · [dossier](Problem/2299-strong-password-checker-II)

📊 3 problems · 20 files inside dossiers
<!-- AUTO-LEDGER:END -->

The repo-wide census, as GitHub's own language bar reports it:

`🟪🟪🟪 ⚪⚪ 🟠🟠 🟡🟡 🔵`

| Language | Share | What studying this port teaches |
| :--- | :---: | :--- |
| 🟪 Racket | 25.1 % | tail recursion as the only loop; values as unboxed multi-return; how a driver's naming convention overrides every convention you brought |
| ⚪ C | 20.8 % | NUL-terminator reasoning; header-free translation units; static inline folds and radix passes that lower to straight-line code |
| 🟠 Java | 19.5 % | primitive-only hot paths; static flat buffers reused across testcases; fused recurrence and bucketing in one pass |
| 🟡 JavaScript | 17.8 % | IEEE-754 exactness below 2^53; typed arrays with native numeric sort; tabulated popcount |
| 🔵 Python | 16.8 % | exact integers by language guarantee; keyword collision discipline; a vectorized fast path with an exact pure fallback |

## 5. The flagship lesson

LeetCode 420 is the teaching vehicle: three defects (length outside $[6,20]$, missing character classes, runs of three), three repairs (insert, delete, replace), and a cost algebra that changes regime at the thresholds.

$$
\text{cost}(n) =
\begin{cases}
\max(m,\; 6-n) & n < 6 \\
\max(m,\; \sum \lfloor L/3 \rfloor) & 6 \le n \le 20 \\
(n-20) + \max(m,\; \text{rep}) & n > 20
\end{cases}
$$

```text
0        6                   20                  n
├────────┼───────────────────┼───────────────────▶
 insert   replace-only        delete + replace
```

In the overlong regime a deletion is worth exactly the replacement it cancels, priced by $L \bmod 3$: one deletion at mod 0, two at mod 1, three at mod 2. Buy cheapest first; once the cheap runs are gone every survivor is congruent to $2 \bmod 3$ and the remainder collapses to the closed form $\min(\lfloor \text{budget}/3 \rfloor, \text{rep})$.

> **Exchange argument, one sentence:** if a solution buys a cancellation at a higher price while a cheaper one remains unbought, swapping the purchase to the cheaper run never increases total cost; therefore cheapest-first is optimal.

## 6. Witness discipline

A formula table is a claim; a witness family is a test. Families here are small, hand-computable, and lethal to wrong variants.

| Witness | What it discriminates | Outcome |
| :--- | :--- | :---: |
| 21 identical chars | price-1 existence: without mod-0 buys the answer would be 8, not 7 | **7** |
| 25 identical chars | price-2 existence: skipping mod-1 buys yields 12, not 11 | **11** |
| 27 identical chars | price-3 closed form: concentration must hold for naive and closed forms to agree | **13** |
| `"aaa111"` | regime boundary at $n = 6$: replacement-only algebra | **2** |
| `"a"` | regime below 6: insertion algebra dominates | **5** |
| `"Me+You--IsMyDream"` | online refutation: one adjacent pair kills the conjunction at 2299 | **false** |

```diff
- weak:   Baaabb0     a run of three identical characters
+ strong: Baaba0      every run bounded by two
```

> **Build your own family:** take the cheapest structure that exercises one price at a time — length a multiple of 3, then plus 1, then plus 2. If two candidate formulas disagree, one member exposes it by hand arithmetic.

## 7. Failure-mode catalogue

| Failure class | Recorded event | Closure now in force |
| :--- | :--- | :--- |
| Unbound driver symbol | a Racket driver called a kebab-case name the solution did not define | driver reports rank as binding evidence; rename exactly one symbol, keep the kernel |
| Broken visual asset | one progress-bar renderer returned broken images under the GitHub proxy | asset purged; only renderers verified live on GitHub remain |
| Shared bucket cursor | a fused Java loop let one cursor array serve two buffers; [-36,36] answered 0 | two cursor arrays F0 and F1; the witness stays in the trace table forever |
| Empty bucket placeholder | a vectorized Python path seeded future buckets with None; first concatenate raised TypeError | empty int64 arrays; the pure path never had the hole |
| Index bounds | run walks can overrun if the inner test is misplaced | inner loop tests the bound before every read; outer index jumps monotonically |
| Stale documentation | hand-written trees rot the moment a file moves | sections 3 and 4 are regenerated artifacts; humans write prose, machines write inventories |

> **Binding lesson, verbatim in spirit:** a compile error that names a symbol is a driver line speaking to you. Evidence outranks convention, and the fix is one rename, not a rewrite.

## 8. Receipts

* **420 · Racket** — 54 / 54 testcases, 0 ms, beats 100.00 %
* **2299 · C** — 201 / 201 testcases, 0 ms, beats 100.00 %, 8.37 MB
* **2035 · C** — 201 / 201 testcases, 171 ms, beats 100.00 %, 9.34 MB
* **2035 · Java** — 201 / 201 testcases, 197 ms, beats 99.40 %, memory beats 100.00 %
* **2035 · JavaScript** — 201 / 201 testcases, 201 ms, beats 100.00 %
* **2035 · Python** — 201 / 201 testcases, 235 ms, beats 99.76 %

<div align="center">

[![Star History Chart](https://api.star-history.com/svg?repos=taro902/Leetcode-Solution&type=Date)](https://star-history.com/#taro902/Leetcode-Solution&Date)

![Contribution chart](https://ghchart.rshah.org/00897B/taro902)

</div>

## 9. Study protocol

1. Pick the language you want to sharpen; open its dossier from the vault line.
2. Read the structural fact and close the tab; predict the pipeline from memory.
3. Reopen at the witness table; recompute one row by hand before looking at the answer column.
4. Read the source last, and only to confirm what you already derived.
5. Port the kernel to a sixth language yourself; the catalogue tells you which traps to seal first, and the vault meter gains a sixth square the day you commit it.

---

<p align="center"><sub>Tar0 registry · R1 binding from evidence · R2 proof-carrying pruning · R9 single kernel multi-alias</sub><br><sub>the map and the vault are regenerated artifacts; the prose around them is human and stays human</sub></p>
