var PC = new Int32Array(21);
var SC = new Int32Array(21);

var kernel_10 = function(s, p) {
    var n = s.length;
    var m = p.length;
    var k;
    for (k = 0; k < m; k++) PC[k] = p.charCodeAt(k);
    for (k = 0; k < n; k++) SC[k] = s.charCodeAt(k);
    var prev = 0;
    var cur = 0;
    var i;
    var j;
    for (i = 0; i <= n; i++) {
        cur = (i === 0) ? 1 : 0;
        var sc = (i >= 1) ? SC[i - 1] : -1;
        for (j = 1; j <= m; j++) {
            var pcj = PC[j - 1];
            var v = 0;
            if (pcj === 42) {
                if (j >= 2 && ((cur >>> (j - 2)) & 1)) {
                    v = 1;
                } else if (i >= 1 && j >= 2) {
                    var pc2 = PC[j - 2];
                    if (pc2 === 46 || pc2 === sc) {
                        v = (prev >>> j) & 1;
                    }
                }
            } else if (i >= 1 && ((prev >>> (j - 1)) & 1)) {
                if (pcj === 46 || pcj === sc) v = 1;
            }
            if (v) cur |= (1 << j);
        }
        prev = cur;
    }
    return ((prev >>> m) & 1) === 1;
};

var isMatch = function(s, p) {
    return kernel_10(s, p);
};

var is_match = function(s, p) {
    return kernel_10(s, p);
};
