class Solution:
    def mergeStones(self, stones: list[int], k: int) -> int:
        n = len(stones)
        step = k - 1
        if (n - 1) % step:
            return -1
        if n == 1:
            return 0
            
        for i in range(1, n):
            stones[i] += stones[i - 1]
        stones.append(0)
        
        dp = [[0] * n for _ in range(n)]
        
        if k == 2:
            opt = [[0] * n for _ in range(n)]
            for i in range(n - 1):
                dp[i][i + 1] = stones[i + 1] - stones[i - 1]
                opt[i][i + 1] = i
                
            for l in range(3, n + 1):
                for i in range(n - l + 1):
                    j = i + l - 1
                    min_v = 999999999
                    best_m = opt[i][j - 1]
                    dp_i = dp[i]
                    for m in range(best_m, opt[i + 1][j] + 1):
                        v = dp_i[m] + dp[m + 1][j]
                        if v < min_v:
                            min_v = v
                            best_m = m
                    dp_i[j] = min_v + stones[j] - stones[i - 1]
                    opt[i][j] = best_m
            return dp[0][n - 1]
            
        for l in range(k, n + 1):
            is_merge = not ((l - 1) % step)
            for i in range(n - l + 1):
                j = i + l - 1
                dp_i = dp[i]
                min_v = 999999999
                for m in range(i, j, step):
                    v = dp_i[m] + dp[m + 1][j]
                    if v < min_v:
                        min_v = v
                dp_i[j] = min_v + (stones[j] - stones[i - 1] if is_merge else 0)
                
        return dp[0][n - 1]
