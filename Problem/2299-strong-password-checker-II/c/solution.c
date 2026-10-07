#include <stdbool.h>

static const char SP2[] = "!@#$%^&*()-+";

static bool spc2_special(char c) {
    for (int i = 0; SP2[i] != '\0'; i++) {
        if (SP2[i] == c) return true;
    }
    return false;
}

static bool spc2_kernel(char *s) {
    int n = 0;
    while (s[n] != '\0') n++;
    if (n < 8) return false;
    int low = 0;
    int up = 0;
    int dig = 0;
    int spc = 0;
    for (int i = 0; i < n; i++) {
        char c = s[i];
        if (i > 0 && c == s[i - 1]) return false;
        if (c >= 'a' && c <= 'z') low = 1;
        else if (c >= 'A' && c <= 'Z') up = 1;
        else if (c >= '0' && c <= '9') dig = 1;
        else if (spc2_special(c)) spc = 1;
    }
    return (low && up && dig && spc) != 0;
}

bool strongPasswordCheckerII(char* password) {
    return spc2_kernel(password);
}

bool strong_password_checker_ii(char* password) {
    return spc2_kernel(password);
}
