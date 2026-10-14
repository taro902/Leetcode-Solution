class Solution {
    private static final int MAX_STATES = 60005;
    private static final char[] nxt = new char[MAX_STATES << 5];
    private static final char[] linkSt = new char[MAX_STATES];
    private static final char[] lenSt = new char[MAX_STATES];
    private static final char[] ZERO_ROW = new char[26];

    public String longestDupSubstring(String s) {
        final int n = s.length();
        int sz = 1, last = 1;
        lenSt[1] = 0;
        linkSt[1] = 0;
        System.arraycopy(ZERO_ROW, 0, nxt, 32, 26);

        int maxLen = 0, bestEnd = 0;

        for (int i = 0; i < n; ++i) {
            final int c = s.charAt(i) - 'a';
            final int cur = ++sz;
            lenSt[cur] = (char) (i + 1);
            System.arraycopy(ZERO_ROW, 0, nxt, cur << 5, 26);

            int p = last;
            while (p != 0 && nxt[(p << 5) | c] == 0) {
                nxt[(p << 5) | c] = (char) cur;
                p = linkSt[p];
            }

            if (p == 0) {
                linkSt[cur] = 1;
            } else {
                final int pIdx = (p << 5) | c;
                final int q = nxt[pIdx];
                final int lp = lenSt[p] + 1;
                if (lp == lenSt[q]) {
                    linkSt[cur] = (char) q;
                } else {
                    final int clone = ++sz;
                    lenSt[clone] = (char) lp;
                    System.arraycopy(nxt, q << 5, nxt, clone << 5, 26);
                    linkSt[clone] = linkSt[q];
                    while (p != 0 && nxt[(p << 5) | c] == q) {
                        nxt[(p << 5) | c] = (char) clone;
                        p = linkSt[p];
                    }
                    linkSt[q] = linkSt[cur] = (char) clone;
                }
                if (lp > maxLen) {
                    maxLen = lp;
                    bestEnd = i;
                }
            }
            last = cur;
        }

        return maxLen == 0 ? "" : s.substring(bestEnd - maxLen + 1, bestEnd + 1);
    }
}
