import java.util.Arrays;

public class Solution {
    private int kernel(int[] nums) {
        int n = nums.length >> 1;
        int masks = 1 << n;
        int[] d0 = new int[masks];
        int[] d1 = new int[masks];
        long sum0 = 0;
        long sum1 = 0;
        for (int i = 0; i < n; i++) sum0 += nums[i];
        for (int i = n; i < nums.length; i++) sum1 += nums[i];
        d0[0] = (int) -sum0;
        d1[0] = (int) -sum1;
        for (int m = 1; m < masks; m++) {
            int low = m & -m;
            int i = Integer.numberOfTrailingZeros(low);
            int pm = m ^ low;
            d0[m] = d0[pm] + 2 * nums[i];
            d1[m] = d1[pm] + 2 * nums[n + i];
        }
        int[] comb = new int[n + 1];
        comb[0] = 1;
        for (int k = 1; k <= n; k++) comb[k] = comb[k - 1] * (n - k + 1) / k;
        int[][] bu0 = new int[n + 1][];
        int[][] bu1 = new int[n + 1][];
        int[] fill = new int[n + 1];
        for (int k = 0; k <= n; k++) {
            bu0[k] = new int[comb[k]];
            bu1[k] = new int[comb[k]];
        }
        for (int m = 0; m < masks; m++) {
            int k = Integer.bitCount(m);
            bu0[k][fill[k]++] = d0[m];
        }
        fill = new int[n + 1];
        for (int m = 0; m < masks; m++) {
            int k = Integer.bitCount(m);
            bu1[k][fill[k]++] = d1[m];
        }
        for (int k = 0; k <= n; k++) {
            Arrays.sort(bu0[k]);
            Arrays.sort(bu1[k]);
        }
        long best = Long.MAX_VALUE;
        for (int k1 = 0; k1 <= n; k1++) {
            int[] A = bu0[k1];
            int[] B = bu1[n - k1];
            int nb = B.length;
            for (int x : A) {
                long target = -(long) x;
                int lo = 0;
                int hi = nb;
                while (lo < hi) {
                    int mid = (lo + hi) >>> 1;
                    if (B[mid] < target) lo = mid + 1;
                    else hi = mid;
                }
                if (lo < nb) {
                    long v = Math.abs((long) x + B[lo]);
                    if (v < best) best = v;
                }
                if (lo > 0) {
                    long v = Math.abs((long) x + B[lo - 1]);
                    if (v < best) best = v;
                }
                if (best == 0) return 0;
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
