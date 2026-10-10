def _strong_password_checker_kernel(s):
    n = len(s)
    low = 0
    up = 0
    dig = 0
    rep = 0
    c0 = 0
    c1 = 0
    i = 0
    while i < n:
        c = s[i]
        if 'a' <= c <= 'z':
            low = 1
        elif 'A' <= c <= 'Z':
            up = 1
        elif '0' <= c <= '9':
            dig = 1
        j = i
        while j < n and s[j] == c:
            j += 1
        L = j - i
        if L >= 3:
            rep += L // 3
            m = L % 3
            if m == 0:
                c0 += 1
            elif m == 1:
                c1 += 1
        i = j
    missing = 3 - low - up - dig
    if n < 6:
        return max(missing, 6 - n)
    if n <= 20:
        return max(missing, rep)
    budget = n - 20
    s1 = min(c0, budget)
    budget -= s1
    rep -= s1
    s2 = min(c1, budget // 2)
    budget -= 2 * s2
    rep -= s2
    s3 = min(budget // 3, rep)
    rep -= s3
    return (n - 20) + max(missing, rep)


class Solution:
    def strongPasswordChecker(self, password: str) -> int:
        return _strong_password_checker_kernel(password)

    def strong_password_checker(self, password: str) -> int:
        return _strong_password_checker_kernel(password)
