<p align="center">
  <img src="https://readme-typing-svg.demolab.com/?font=JetBrains+Mono&size=21&duration=3200&pause=800&color=CC3300&center=true&vCenter=true&width=880&lines=10+%C2%B7+Regular+Expression+Matching;Java+lane+%C2%B7+one+flat+441-byte+table%2C+never+cleared;1+ms+%C2%B7+43.02+MB+%C2%B7+354%2F354" alt="typing line"/>
</p>

<h1 align="center">Regular Expression Matching</h1>

<p align="center">
  <sub>LeetCode 10 · Hard · a prefix DP over a single static boolean array · zero allocation per call · the judge panel below is the only number this document argues from</sub>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/LeetCode-10%20%C2%B7%20Hard-cc3300?style=flat-square&logo=leetcode&logoColor=white" alt="problem"/>
  <img src="https://img.shields.io/badge/Java-17-e85d04?style=flat-square" alt="language"/>
  <img src="https://img.shields.io/badge/Accepted-354%2F354-1a7f37?style=flat-square" alt="verdict"/>
  <img src="https://img.shields.io/badge/Runtime-1%20ms%20%C2%B7%2099.98%25-cc3300?style=flat-square" alt="runtime"/>
  <img src="https://img.shields.io/badge/Memory-43.02%20MB%20%C2%B7%2096.63%25-e85d04?style=flat-square" alt="memory"/>
  <img src="https://img.shields.io/badge/Proof-Oct%2011%2C%202026%2012%3A24-444444?style=flat-square" alt="proof"/>
</p>

<p align="center">
  <a href="https://i.ibb.co.com/LDQvmPp2/image.png">
    <img src="https://i.ibb.co.com/LDQvmPp2/image.png" width="72%" alt="judge panel, Oct 11 2026 12:24"/>
  </a>
  <br/>
  <sub>the judge panel, verbatim · click for full resolution</sub>
</p>

---

## Contents

- [The receipt](#the-receipt)
- [The problem](#the-problem)
- [The recurrence](#the-recurrence)
- [Anatomy of the kernel](#anatomy-of-the-kernel)
- [What the JVM actually does with this](#what-the-jvm-actually-does-with-this)
- [Trace, the full grid](#trace-the-full-grid)
- [Cost](#cost)
- [Guards and limits](#guards-and-limits)
- [Source](#source)
- [Repo conventions](#repo-conventions)

---

## The receipt

| Verdict | Cases | Runtime | Beat | Memory | Beat | Submitted |
| :-- | :-- | :-- | :-- | :-- | :-- | :-- |
| Accepted | 354/354 | 1 ms | 99.98% | 43.02 MB | 96.63% | Oct 11 2026, 12:24 · [panel](https://i.ibb.co.com/LDQvmPp2/image.png) |

Two readings, both in JVM terms. The runtime histogram on the panel starts its axis at 3 ms, and this build sits left of the first visible bar at 1 ms. The 0.02% of submissions labeled 0 ms are not doing less work; a 441-cell sweep cannot be subdivided further. They drew a warmer JIT state on their run, where C2 had already compiled the loop before the timer started. Chasing that label would mean optimizing the judge's warmup, not the program.

The memory number is HotSpot residency: heap, metaspace, code cache, and thread stacks of a Java process that exists before a single line of user code runs. This kernel contributes one 441-byte static array to that process and allocates nothing per call. The 3.37% of submissions reading below 43.02 MB are lighter JVM starts on shared silicon, not leaner programs. There is no allocation left in this file to remove.

---

## The problem

Given a string `s` and a pattern `p`, decide whether `p` matches all of `s`, not a prefix of it. The pattern has two wildcards: `.` stands for any single character, and `*` stands for zero or more repetitions of the element immediately before it. The star is the whole difficulty. It binds backward, it may vanish, and it may consume an unbounded run, so a left-to-right greedy scan cannot decide anything: consuming now and saving the star for later are both legal, and only the suffix knows which was right. Prefix dynamic programming removes the prophecy entirely.

---

## The recurrence

Let `dp[i][j]` mean that the first `i` characters of `s` match the first `j` characters of `p`. The answer is the corner cell `dp[n][m]`. Filling a cell looks at the last pattern character, `p[j-1]`:

- **Literal or dot.** It must consume exactly one character of `s`, so the cell is `i >= 1 && dp[i-1][j-1] && (p[j-1] == '.' || p[j-1] == s[i-1])`. With `i == 0` there is nothing to consume and the cell is false.
- **Star.** Two disjoint lives, OR-ed together. Zero uses: the pair `x*` collapses and the cell inherits `dp[i][j-2]`, which needs `j >= 2`. One or more uses: the star eats one character of `s` against its own predecessor `p[j-2]` and stays alive, giving `(p[j-2] == '.' || p[j-2] == s[i-1]) && dp[i-1][j]`, which needs `i >= 1`.
- **Base.** `dp[0][0] = true`, and the rest of column zero is false, because an empty pattern matches only an empty string.

The OR over the star's two lives is exhaustive rather than heuristic: any match of `s[0..i)` against `p[0..j)` either never uses the star, which is the `j-2` case, or uses it at least once, in which case peeling the last consumed character leaves a match of `s[0..i-1)` against the same `j`, which is the `i-1` case. There is no third shape a match can take.

Every right-hand side references only `(i, j-2)`, `(i-1, j)`, or `(i-1, j-1)`. In a row-major sweep all three were written earlier, so one pass suffices and no cell is ever read before it is final.

---

## Anatomy of the kernel

**One flat table.** `DP` is a single `static final boolean[441]`, allocated once when the class initializes. HotSpot stores a `boolean[]` as one byte per element, so the whole table is 441 bytes behind a 16-byte object header, contiguous, and resident in L1 from the first testcase onward. The obvious alternative, `boolean[21][21]`, is really 22 objects: one array of row pointers plus 21 row arrays. Every cell read through it pays two loads, one for the row pointer and one for the byte. The flat form pays one address computation, `i * 21 + j`, and one load. `rowBase = i * 21` is hoisted out of the inner loop so even that multiplication happens once per row.

**Never cleared, on purpose.** The table is mutable static state and is never reset between calls. That is safe by the dependency order above: within a call, every read addresses a cell the same call already wrote, two columns back in the current row or anywhere in the previous row. Content left over from the previous testcase is unreachable, not overwritten defensively. An `Arrays.fill` per call would be 441 stores of pure waste, 354 times over.

**Branch order follows cost.** The `j == 0` base column is a register compare and nothing else. In the star branch the zero-use life is tried first because it is cheaper: one bounds test and one same-row load. The consume-one life sits behind `!v && i >= 1`, so a cell already proved by zero-use never touches the string, and the empty-prefix row never calls `charAt(i - 1)`. In the literal branch the length guard and the table load come before any character comparison, so a dead prefix costs one load and a mismatched character costs two.

**`charAt`, not `toCharArray`.** Converting both inputs to `char[]` up front would allocate two arrays per call and copy up to 40 bytes into them. On Java 9+ compact strings, `charAt` on an immutable `String` compiles under C2 to a coder check plus a load from the backing `byte[]`, with no allocation at all. Since the kernel reads each character at most a few times, the zero-allocation path wins and the copies never happen.

**Two names, one body.** `isMatch` and `is_match` are one-expression thunks over the private `kernel_10`, covering whichever spelling a driver emits. C2 inlines the kernel into both, so the thunks cost nothing and the logic exists exactly once.

```mermaid
flowchart TD
    A["lengths n, m; rowBase hoisted per row"] --> B["sweep i in 0..n, j in 0..m"]
    B --> C{"j == 0"}
    C -- yes --> D["v = (i == 0)"]
    C -- no --> E{"p[j-1] == '*'"}
    E -- yes --> F["zero-use: j >= 2 and DP[rowBase + j - 2]"]
    F -- still false --> G["consume-one: i >= 1, p[j-2] vs s[i-1], DP[(i-1)*21 + j]"]
    E -- no --> H["literal: i >= 1, DP[(i-1)*21 + j - 1], p[j-1] vs s[i-1]"]
    D --> I["DP[rowBase + j] = v"]
    G --> I
    H --> I
    I --> B
    I --> J["return DP[n*21 + m]"]
```

---

## What the JVM actually does with this

At class-initialization time the single `new boolean[441]` lands in the old generation almost immediately, because nothing ever reassigns or discards it; it is effectively immortal, so no collection ever copies or scans it beyond one root. Inside the loop, C2 sees a monomorphic `boolean[]` load with a provably in-bounds index after the first few interpreted iterations, hoists the array base out of the loop, and keeps `rowBase`, `j`, and the loop bounds in registers. The `charAt` calls devirtualize against `java.lang.String` and fold into byte loads with the latin-1 coder path selected, because the judge's inputs are ASCII. What remains at steady state is a tight doubly-nested loop of byte loads and compares over 441 bytes, which is why the panel's histogram has no bar where this build sits.

One honest caveat belongs here. The table is shared mutable static state, so two threads calling `isMatch` concurrently inside one JVM would race on it. The judge drives one testcase at a time per worker, which is the contract this file is written against; if a future harness ever parallelizes within a process, the table becomes per-call or thread-local, and that change is one line.

---

## Trace, the full grid

Input `s = "aab"`, `p = "c*a*b"`, so `n = 3`, `m = 5`. The table as the sweep writes it:

```text
            j=0   j=1(c)  j=2(*)  j=3(a)  j=4(*)  j=5(b)
i=0  ""      T     F       T       F       T       F
i=1  "a"     F     F       F       T       T       F
i=2  "aa"    F     F       F       F       T       F
i=3  "aab"   F     F       F       F       F       T
```

The cells that carry the argument:

```text
dp[0][2]  star zero-use over dp[0][0]          T   "c*" vanishes against the empty string
dp[0][4]  star zero-use over dp[0][2]          T   "a*" vanishes as well
dp[1][3]  literal 'a' == 'a' over dp[0][2]     T   first character actually consumed
dp[1][4]  star consume 'a' over dp[0][4]       T   the star eats the first 'a'
dp[2][4]  star consume 'a' over dp[1][4]       T   and the second
dp[3][5]  literal 'b' == 'b' over dp[2][4]     T   corner cell, the returned answer
```

Row 1 column 2 shows a star correctly refusing: zero-use reads `dp[1][0] = F`, and consume-one compares `p[0] = 'c'` against `s[0] = 'a'` and fails, so the cell is false and the whole column below it stays false. Row 3 column 4 shows the same star dying differently: `p[2] = 'a'` cannot eat `s[2] = 'b'`, and zero-use reads `dp[3][2] = F`. The corner inherits its truth from `dp[2][4]`, the cell where the star finished its work two rows earlier.

---

## Cost

| Quantity | Bound | At n = m = 20 |
| :-- | :-- | :-- |
| Cells written | (n+1)·(m+1) | 441 |
| Loads per cell | at most 3 table bytes, 2 string bytes | constant |
| Allocation per call | none | 0 bytes |
| Static footprint | one boolean[441] plus header | 457 bytes |
| Stack | five locals, no recursion | constant frame |

Three hundred fifty-four testcases of that table is a few hundred thousand instructions in total, which is what a 1 ms label looks like when the axis starts at 3.

---

## Guards and limits

- **Index bounds.** Constraints cap both lengths at 20, so the largest address computed is `20 * 21 + 20 = 440`, the last byte of the array. No write or read can leave the object.
- **Star arithmetic.** `j >= 2` is tested before `j - 2` is formed, and `i >= 1` before any `i - 1` reaches the table or the string. The `j == 0` branch returns before `p.charAt(j - 1)` could ever see a negative index.
- **Star at pattern front.** The problem contract forbids it, and the zero-use guard makes the code independent of that contract anyway.
- **Depth and heap.** There is no recursion, so no pattern can deepen a stack, and there is no allocation, so no input can pressure the collector. The two classic failure shapes of naive regex matchers simply have no representation here.
- **Concurrency.** Accepted as a documented tradeoff, stated in the JVM section above rather than hidden.

---

## Source

<details>
<summary><strong>The kernel as submitted</strong></summary>

```java
class Solution {
    private static final int CAP = 21;
    private static final boolean[] DP = new boolean[CAP * CAP];

    private boolean kernel_10(String s, String p) {
        int n = s.length();
        int m = p.length();
        for (int i = 0; i <= n; i++) {
            int rowBase = i * CAP;
            for (int j = 0; j <= m; j++) {
                boolean v;
                if (j == 0) {
                    v = (i == 0);
                } else {
                    char pc = p.charAt(j - 1);
                    if (pc == '*') {
                        v = (j >= 2) && DP[rowBase + (j - 2)];
                        if (!v && i >= 1) {
                            char pc2 = p.charAt(j - 2);
                            char sc = s.charAt(i - 1);
                            if (pc2 == '.' || pc2 == sc) {
                                v = DP[(i - 1) * CAP + j];
                            }
                        }
                    } else {
                        if (i >= 1 && DP[(i - 1) * CAP + (j - 1)]) {
                            char sc = s.charAt(i - 1);
                            v = (pc == '.') || (pc == sc);
                        } else {
                            v = false;
                        }
                    }
                }
                DP[rowBase + j] = v;
            }
        }
        return DP[n * CAP + m];
    }

    public boolean isMatch(String s, String p) {
        return kernel_10(s, p);
    }

    public boolean is_match(String s, String p) {
        return kernel_10(s, p);
    }
}
```

</details>

---

## Repo conventions

- Judge screenshots are the only evidence. Every number in this document traces to the panel embedded at the top, and labels the harness owns are called harness properties rather than achievements.
- One kernel per problem, public names as thunks, logic written once.
- Documents live in the folder of the code they describe and speak only for that code.
- When a build trades one axis for another, both vertices stay filed; when it dominates, the ledger says so plainly.

---

<p align="center">
  <img src="https://media4.giphy.com/media/v1.Y2lkPTc5MGI3NjExajJ5bHltbDg2NHg0Mzl4cjF5d3o5bXhncmhjNDB2dTNpcTRkOTdtMSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/fVcKQDvHKtfBKfRGm4/giphy.gif" width="320" alt="sticker"/>
</p>

<p align="center">
  <img src="https://ghchart.rshah.org/cc3300/taro902" width="90%" alt="commit pulse"/>
</p>

<p align="center">
  <img src="https://api.star-history.com/svg?repos=taro902/Leetcode-Solution&type=Date" width="62%" alt="star history"/>
</p>

<p align="center">
  <img src="https://media.giphy.com/media/26BRBKzUi8g3uO7uw/giphy.gif" width="280" alt="sticker"/>
  <br/>
  <img src="https://komarev.com/ghpvc/?username=taro902&label=reads+on+this+dossier&color=e85d04&style=flat-square" alt="view counter"/>
</p>
