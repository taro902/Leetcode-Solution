import java.util.Arrays;

public class Solution {
    private static final int K_MASKS = 1 << 15;
    private static final int[] K_D0 = new int[K_MASKS];
    private static final int[] K_D1 = new int[K_MASKS];
    private static final int[] K_F0 = new int[K_MASKS];
    private static final int[] K_F1 = new int[K_MASKS];
    private static final int[] K_OFF = new int[17];
    private static final int[] K_COMB = new int[17];
    private static final int[] K_CUR = new int[17];

    private int kernel(int[] nums) {
        final int n = nums.length >> 1;
        final int masks = 1 << n;
        final int[] d0 = K_D0;
        final int[] d1 = K_D1;
        final int[] f0 = K_F0;
        final int[] f1 = K_F1;
        final int[] off = K_OFF;
        final int[] comb = K_COMB;
        final int[] cur = K_CUR;
        long sum0 = 0;
        long sum1 = 0;
        int i;
        int m;
        int k;
        for (i = 0; i < n; i++) sum0 += nums[i];
        for (i = n; i < nums.length; i++) sum1 += nums[i];
        d0[0] = (int) -sum0;
        d1[0] = (int) -sum1;
        for (m = 1; m < masks; m++) {
            final int low = m & -m;
            i = Integer.numberOfTrailingZeros(low);
            final int pm = m ^ low;
            d0[m] = d0[pm] + 2 * nums[i];
            d1[m] = d1[pm] + 2 * nums[n + i];
        }
        comb[0] = 1;
        for (k = 1; k <= n; k++) comb[k] = comb[k - 1] * (n - k + 1) / k;
        off[0] = 0;
        for (k = 0; k <= n; k++) off[k + 1] = off[k] + comb[k];
        for (k = 0; k <= n; k++) cur[k] = off[k];
        for (m = 0; m < masks; m++) {
            k = Integer.bitCount(m);
            f0[cur[k]++] = d0[m];
        }
        for (k = 0; k <= n; k++) cur[k] = off[k];
        for (m = 0; m < masks; m++) {
            k = Integer.bitCount(m);
            f1[cur[k]++] = d1[m];
        }
        long best = Long.MAX_VALUE;
        for (k = 0; k <= n; k++) {
            final int aFrom = off[k];
            final int aTo = off[k + 1];
            final int bFrom = off[n - k];
            final int bTo = off[n - k + 1];
            Arrays.sort(f0, aFrom, aTo);
            Arrays.sort(f1, bFrom, bTo);
            int ia = aFrom;
            int jb = bTo - 1;
            while (ia < aTo && jb >= bFrom) {
                final long s = (long) f0[ia] + f1[jb];
                final long v = s < 0 ? -s : s;
                if (v < best) best = v;
                if (best == 0) return 0;
                if (s < 0) ia++;
                else jb--;
            }
        }
        return (int) best;
    }

    public int minimumDifference(int[] nums) {
        return kernel(nums);
    }

    public int minimum_difference(int[] nums) {
        return kernel(nums);
    }
}
