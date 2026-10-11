int mergeStones(int* s, int n, int k) {
    if ((n - 1) % (k - 1)) return -1;
    int d[n * n], i = -1, j, l, m, c, v;
    while (++i < n * n) d[i] = 0;
    for (i = 1; i < n; ++i) s[i] += s[i - 1];
    for (l = k; l <= n; ++l)
        for (i = 0; (j = i + l - 1) < n; ++i) {
            for (c = 999999999, m = i; m < j; m += k - 1)
                if ((v = d[i * n + m] + d[(m + 1) * n + j]) < c) c = v;
            d[i * n + j] = c + ((j - i) % (k - 1) ? 0 : s[j] - (i ? s[i - 1] : 0));
        }
    return d[n - 1];
}
