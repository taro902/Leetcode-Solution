class Solution:
    def isMatch(self, s: str, p: str) -> bool:
        v, m, l, lp, i = 1, 0, len(s), len(p), 0
        for j, c in enumerate(s, 1): m |= 1 << (j + 22 * ord(c))
        d = (1 << (l + 1)) - 2
        
        while i < lp:
            o, s_ = ord(p[i]), i + 1 < lp and p[i + 1] == '*'
            if s_:
                if o == 46: 
                    v |= (1 << (l + 1)) - (v & -v)
                elif (k := (m >> (22 * o)) & 4194303):
                    while (x := v | ((v << 1) & k)) != v: v = x
            else:
                if not (v := (v << 1) & (d if o == 46 else ((m >> (22 * o)) & 4194303))): return False
            i += 2 if s_ else 1
            
        return bool((v >> l) & 1)
