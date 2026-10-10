public class Solution {
    private int kernel(String s) {
        int n = s.length();
        int low = 0;
        int up = 0;
        int dig = 0;
        int rep = 0;
        int c0 = 0;
        int c1 = 0;
        for (int i = 0; i < n; ) {
            char c = s.charAt(i);
            if (c >= 'a' && c <= 'z') low = 1;
            else if (c >= 'A' && c <= 'Z') up = 1;
            else if (c >= '0' && c <= '9') dig = 1;
            int j = i;
            while (j < n && s.charAt(j) == c) j++;
            int L = j - i;
            if (L >= 3) {
                rep += L / 3;
                int m = L % 3;
                if (m == 0) c0++;
                else if (m == 1) c1++;
            }
            i = j;
        }
        int missing = 3 - low - up - dig;
        if (n < 6) return Math.max(missing, 6 - n);
        if (n <= 20) return Math.max(missing, rep);
        int del = n - 20;
        int s1 = Math.min(c0, del);
        del -= s1;
        rep -= s1;
        int s2 = Math.min(c1, del / 2);
        del -= 2 * s2;
        rep -= s2;
        int s3 = Math.min(del / 3, rep);
        rep -= s3;
        return (n - 20) + Math.max(missing, rep);
    }

    public int strongPasswordChecker(String password) {
        return kernel(password);
    }

    public int strong_password_checker(String password) {
        return kernel(password);
    }
}
