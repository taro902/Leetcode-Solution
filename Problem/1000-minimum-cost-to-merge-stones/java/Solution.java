class Solution {
    public int mergeStones(int[] s, int k) {
        int n = s.length, step = k - 1;
        if ((n - 1) % step != 0) return -1;
        
        int[] d = new int[n * n];
        for (int i = 1; i < n; ++i) s[i] += s[i - 1];
        
        for (int l = k; l <= n; ++l) {
            boolean add = (l - 1) % step == 0;
            
            int min = 999999999, j = l - 1;
            for (int m = 0; m < j; m += step) {
                int v = d[m] + d[(m + 1) * n + j];
                if (v < min) min = v;
            }
            d[j] = min + (add ? s[j] : 0);
            
            for (int i = 1; (j = i + l - 1) < n; ++i) {
                min = 999999999;
                int in = i * n;
                for (int m = i; m < j; m += step) {
                    int v = d[in + m] + d[(m + 1) * n + j];
                    if (v < min) min = v;
                }
                d[in + j] = min + (add ? s[j] - s[i - 1] : 0);
            }
        }
        return d[n - 1];
    }
}
