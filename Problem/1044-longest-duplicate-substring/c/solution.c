#include <stdlib.h>
#include <string.h>

#define MAX_STATES 200005

static int nxt[MAX_STATES][26];
static int link_st[MAX_STATES];
static int len_st[MAX_STATES];

char* longestDupSubstring(char* s) {
    int n = (int)strlen(s);
    int sz = 1, last = 1;
    len_st[1] = 0;
    link_st[1] = 0;
    memset(nxt[1], 0, sizeof(nxt[1]));

    int max_len = 0, best_end = 0;

    for (int i = 0; i < n; ++i) {
        int c = s[i] - 'a';
        int cur = ++sz;
        len_st[cur] = len_st[last] + 1;
        memset(nxt[cur], 0, sizeof(nxt[cur]));

        int p = last;
        while (p && !nxt[p][c]) {
            nxt[p][c] = cur;
            p = link_st[p];
        }

        if (!p) {
            link_st[cur] = 1;
        } else {
            int q = nxt[p][c];
            if (len_st[p] + 1 == len_st[q]) {
                link_st[cur] = q;
            } else {
                int clone = ++sz;
                len_st[clone] = len_st[p] + 1;
                memcpy(nxt[clone], nxt[q], sizeof(nxt[q]));
                link_st[clone] = link_st[q];
                while (p && nxt[p][c] == q) {
                    nxt[p][c] = clone;
                    p = link_st[p];
                }
                link_st[q] = link_st[cur] = clone;
            }
        }
        last = cur;

        int l = len_st[link_st[cur]];
        if (l > max_len) {
            max_len = l;
            best_end = i;
        }
    }

    char* res = (char*)malloc(max_len + 1);
    if (max_len > 0) {
        memcpy(res, s + best_end - max_len + 1, max_len);
    }
    res[max_len] = '\0';
    return res;
}
