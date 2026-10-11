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
