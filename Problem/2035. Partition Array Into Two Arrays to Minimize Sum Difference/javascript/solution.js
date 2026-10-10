var K_MASKS = 1 << 15;
var K_D0 = new Int32Array(K_MASKS);
var K_D1 = new Int32Array(K_MASKS);
var K_F0 = new Int32Array(K_MASKS);
var K_F1 = new Int32Array(K_MASKS);
var K_PC = new Uint8Array(K_MASKS);
var K_OFF = new Int32Array(17);
var K_COMB = new Int32Array(17);
var K_CUR = new Int32Array(17);
var K_PC_READY = 0;

var minimumDifferenceKernel = function(nums) {
    var n = nums.length >> 1;
    var masks = 1 << n;
    var d0 = K_D0;
    var d1 = K_D1;
    var f0 = K_F0;
    var f1 = K_F1;
    var pc = K_PC;
    var off = K_OFF;
    var comb = K_COMB;
    var cur = K_CUR;
    var clz = Math.clz32;
    var sum0 = 0;
    var sum1 = 0;
    var i;
    var m;
    var k;
    for (i = 0; i < n; i++) sum0 += nums[i];
    for (i = n; i < nums.length; i++) sum1 += nums[i];
    if (K_PC_READY === 0) {
        for (m = 1; m < K_MASKS; m++) pc[m] = pc[m >> 1] + (m & 1);
        K_PC_READY = 1;
    }
    d0[0] = -sum0;
    d1[0] = -sum1;
    for (m = 1; m < masks; m++) {
        var low = m & -m;
        i = 31 - clz(low);
        var pm = m ^ low;
        d0[m] = d0[pm] + 2 * nums[i];
        d1[m] = d1[pm] + 2 * nums[n + i];
    }
    comb[0] = 1;
    for (k = 1; k <= n; k++) comb[k] = (comb[k - 1] * (n - k + 1) / k) | 0;
    off[0] = 0;
    for (k = 0; k <= n; k++) off[k + 1] = off[k] + comb[k];
    for (k = 0; k <= n; k++) cur[k] = off[k];
    for (m = 0; m < masks; m++) {
        k = pc[m];
        f0[cur[k]++] = d0[m];
    }
    for (k = 0; k <= n; k++) cur[k] = off[k];
    for (m = 0; m < masks; m++) {
        k = pc[m];
        f1[cur[k]++] = d1[m];
    }
    var best = Infinity;
    for (k = 0; k <= n; k++) {
        var A = f0.subarray(off[k], off[k + 1]);
        var B = f1.subarray(off[n - k], off[n - k + 1]);
        A.sort();
        B.sort();
        var na = A.length;
        var ia = 0;
        var jb = B.length - 1;
        while (ia < na && jb >= 0) {
            var s = A[ia] + B[jb];
            var v = s < 0 ? -s : s;
            if (v < best) best = v;
            if (best === 0) return 0;
            if (s < 0) ia++;
            else jb--;
        }
    }
    return best;
};

var minimumDifference = function(nums) {
    return minimumDifferenceKernel(nums);
};

var minimum_difference = function(nums) {
    return minimumDifferenceKernel(nums);
};
