var mergeStones = function(s, k) {
    var n = s.length, step = k - 1;
    if ((n - 1) % step !== 0) return -1;
    
    var d = new Int32Array(n * n), i, j, l, m, in_, min, v, add, stepN = step * n, left, right;
    for (i = 1; i < n; ++i) s[i] += s[i - 1];
    
    for (l = k; l <= n; ++l) {
        add = (l - 1) % step === 0;
        
        min = 999999999; 
        j = l - 1;
        for (m = 0, left = 0, right = n + j; m < j; m += step, left += step, right += stepN) {
            v = d[left] + d[right];
            if (v < min) min = v;
        }
        d[j] = min + (add ? s[j] : 0);
        
        for (i = 1; (j = i + l - 1) < n; ++i) {
            min = 999999999; 
            in_ = i * n;
            for (m = i, left = in_ + i, right = in_ + n + j; m < j; m += step, left += step, right += stepN) {
                v = d[left] + d[right];
                if (v < min) min = v;
            }
            d[in_ + j] = min + (add ? s[j] - s[i - 1] : 0);
        }
    }
    return d[n - 1];
};
