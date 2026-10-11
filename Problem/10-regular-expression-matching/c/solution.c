#include <stdbool.h>
#include <string.h>

static bool dp[21][21];

static bool kernel_10(const char *s, const char *p) {
    int n = (int) strlen(s);
    int m = (int) strlen(p);
    for (int i = 0; i <= n; i++) {
        for (int j = 0; j <= m; j++) {
            bool v;
            if (j == 0) {
                v = (i == 0);
            } else if (p[j - 1] == '*') {
                v = (j >= 2 && dp[i][j - 2]);
                if (!v && i >= 1 && (p[j - 2] == '.' || p[j - 2] == s[i - 1])) {
                    v = dp[i - 1][j];
                }
            } else {
                v = (i >= 1 && dp[i - 1][j - 1] && (p[j - 1] == '.' || p[j - 1] == s[i - 1]));
            }
            dp[i][j] = v;
        }
    }
    return dp[n][m];
}

bool isMatch(char* s, char* p) {
    return kernel_10(s, p);
}

bool is_match(char* s, char* p) {
    return kernel_10(s, p);
}
