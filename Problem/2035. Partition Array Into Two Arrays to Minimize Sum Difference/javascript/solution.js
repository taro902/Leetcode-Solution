var minimumDifferenceKernel = function(nums) {
    var n = nums.length >> 1;
    var masks = 1 << n;
    var d0 = new Int32Array(masks);
    var d1 = new Int32Array(masks);
    var sum0 = 0;
    var sum1 = 0;
    var i;
    for (i = 0; i < n; i++) sum0 += nums[i];
    for (i = n; i < nums.length; i++) sum1 += nums[i];
    d0[0] = -sum0;
    d1[0] = -sum1;
    for (var m = 1; m < masks; m++) {
        var low = m & -m;
        i = 31 - Math.clz32(low);
        var pm = m ^ low;
        d0[m] = d0[pm] + 2 * nums[i];
        d1[m] = d1[pm] + 2 * nums[n + i];
    }
    var pc = new Uint8Array(masks);
    for (m = 1; m < masks; m++) pc[m] = pc[m >> 1] + (m & 1);
    var comb = new Array(n + 1);
    comb[0] = 1;
    for (var k = 1; k <= n; k++) comb[k] = comb[k - 1] * (n - k + 1) / k;
    var bu0 = new Array(n + 1);
    var bu1 = new Array(n + 1);
    for (k = 0; k <= n; k++) {
        bu0[k] = new Int32Array(comb[k]);
        bu1[k] = new Int32Array(comb[k]);
    }
    var fill = new Array(n + 1).fill(0);
    for (m = 0; m < masks; m++) bu0[pc[m]][fill[pc[m]]++] = d0[m];
    fill = new Array(n + 1).fill(0);
    for (m = 0; m < masks; m++) bu1[pc[m]][fill[pc[m]]++] = d1[m];
    for (k = 0; k <= n; k++) {
        bu0[k].sort();
        bu1[k].sort();
    }
    var best = Infinity;
    for (k = 0; k <= n; k++) {
        var A = bu0[k];
        var B = bu1[n - k];
        var ia = 0;
        var jb = B.length - 1;
        while (ia < A.length && jb >= 0) {
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
