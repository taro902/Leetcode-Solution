#include <stdlib.h>

static int cmp_int(const void *pa, const void *pb) {
    int a = *(const int *)pa;
    int b = *(const int *)pb;
    return (a > b) - (a < b);
}

static int k2035_kernel(int *nums, int numsSize) {
    int n = numsSize >> 1;
    int masks = 1 << n;
    static int d0[1 << 15];
    static int d1[1 << 15];
    static int b0[1 << 15];
    static int b1[1 << 15];
    static int off[17];
    static int comb[17];
    static int fill[17];
    long sum0 = 0;
    long sum1 = 0;
    for (int i = 0; i < n; i++) sum0 += nums[i];
    for (int i = n; i < numsSize; i++) sum1 += nums[i];
    d0[0] = (int)(-sum0);
    d1[0] = (int)(-sum1);
    for (int m = 1; m < masks; m++) {
        int low = m & -m;
        int i = __builtin_ctz(low);
        int pm = m ^ low;
        d0[m] = d0[pm] + 2 * nums[i];
        d1[m] = d1[pm] + 2 * nums[n + i];
    }
    comb[0] = 1;
    for (int k = 1; k <= n; k++) comb[k] = comb[k - 1] * (n - k + 1) / k;
    off[0] = 0;
    for (int k = 0; k <= n; k++) off[k + 1] = off[k] + comb[k];
    for (int k = 0; k <= n; k++) fill[k] = off[k];
    for (int m = 0; m < masks; m++) b0[fill[__builtin_popcount(m)]++] = d0[m];
    for (int k = 0; k <= n; k++) fill[k] = off[k];
    for (int m = 0; m < masks; m++) b1[fill[__builtin_popcount(m)]++] = d1[m];
    for (int k = 0; k <= n; k++) {
        qsort(b0 + off[k], comb[k], sizeof(int), cmp_int);
        qsort(b1 + off[k], comb[k], sizeof(int), cmp_int);
    }
    long long best = 4000000000000000000LL;
    for (int k1 = 0; k1 <= n; k1++) {
        int k2 = n - k1;
        int *A = b0 + off[k1];
        int na = comb[k1];
        int *B = b1 + off[k2];
        int nb = comb[k2];
        for (int ia = 0; ia < na; ia++) {
            long target = -(long)A[ia];
            int lo = 0;
            int hi = nb;
            while (lo < hi) {
                int mid = (lo + hi) >> 1;
                if (B[mid] < target) lo = mid + 1;
                else hi = mid;
            }
            if (lo < nb) {
                long long v = llabs((long long)A[ia] + B[lo]);
                if (v < best) best = v;
            }
            if (lo > 0) {
                long long v = llabs((long long)A[ia] + B[lo - 1]);
                if (v < best) best = v;
            }
            if (best == 0) goto done;
        }
    }
done:
    return (int)best;
}

int minimumDifference(int* nums, int numsSize) {
    return k2035_kernel(nums, numsSize);
}

int minimum_difference(int* nums, int numsSize) {
    return k2035_kernel(nums, numsSize);
}
