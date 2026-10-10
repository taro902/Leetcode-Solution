static inline int spc_max(int a, int b) {
    return a >= b ? a : b;
}

static inline void spc_fold_run(int L, int *rep, int *c0, int *c1) {
    if (L >= 3) {
        *rep += L / 3;
        int m = L % 3;
        if (m == 0) {
            (*c0)++;
        } else if (m == 1) {
            (*c1)++;
        }
    }
}

static int spc_kernel(char *s) {
    int n = 0;
    while (s[n] != '\0') n++;
    int low = 0;
    int up = 0;
    int dig = 0;
    int rep = 0;
    int c0 = 0;
    int c1 = 0;
    for (int i = 0; i < n; ) {
        char c = s[i];
        int j = i;
        while (j < n && s[j] == c) {
            if (s[j] >= 'a' && s[j] <= 'z') low = 1;
            else if (s[j] >= 'A' && s[j] <= 'Z') up = 1;
            else if (s[j] >= '0' && s[j] <= '9') dig = 1;
            j++;
        }
        spc_fold_run(j - i, &rep, &c0, &c1);
        i = j;
    }
    int missing = 3 - low - up - dig;
    if (n < 6) return spc_max(missing, 6 - n);
    if (n <= 20) return spc_max(missing, rep);
    int del = n - 20;
    int s1 = c0 < del ? c0 : del;
    del -= s1;
    rep -= s1;
    int half = del / 2;
    int s2 = c1 < half ? c1 : half;
    del -= s2 + s2;
    rep -= s2;
    int third = del / 3;
    int s3 = third < rep ? third : rep;
    rep -= s3;
    return (n - 20) + spc_max(missing, rep);
}

int strongPasswordChecker(char* password) {
    return spc_kernel(password);
}

int strong_password_checker(char* password) {
    return spc_kernel(password);
}
