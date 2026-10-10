var strongPasswordCheckerKernel = function(s) {
    var n = s.length;
    var low = 0;
    var up = 0;
    var dig = 0;
    var rep = 0;
    var c0 = 0;
    var c1 = 0;
    var i = 0;
    while (i < n) {
        var c = s[i];
        if (c >= 'a' && c <= 'z') low = 1;
        else if (c >= 'A' && c <= 'Z') up = 1;
        else if (c >= '0' && c <= '9') dig = 1;
        var j = i;
        while (j < n && s[j] === c) j++;
        var L = j - i;
        if (L >= 3) {
            rep += Math.floor(L / 3);
            var m = L % 3;
            if (m === 0) c0++;
            else if (m === 1) c1++;
        }
        i = j;
    }
    var missing = 3 - low - up - dig;
    if (n < 6) return Math.max(missing, 6 - n);
    if (n <= 20) return Math.max(missing, rep);
    var del = n - 20;
    var s1 = Math.min(c0, del);
    del -= s1;
    rep -= s1;
    var s2 = Math.min(c1, Math.floor(del / 2));
    del -= 2 * s2;
    rep -= s2;
    var s3 = Math.min(Math.floor(del / 3), rep);
    rep -= s3;
    return (n - 20) + Math.max(missing, rep);
};

var strongPasswordChecker = function(password) {
    return strongPasswordCheckerKernel(password);
};

var strong_password_checker = function(password) {
    return strongPasswordCheckerKernel(password);
};
