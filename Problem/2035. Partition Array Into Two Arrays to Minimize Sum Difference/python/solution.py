try:
    import numpy as _np
except Exception:
    _np = None


def _kernel_np(nums, np):
    n = len(nums) >> 1
    bu0 = [np.zeros(1, dtype=np.int64)]
    bu1 = [np.zeros(1, dtype=np.int64)]
    for _ in range(n):
        bu0.append(np.empty(0, dtype=np.int64))
        bu1.append(np.empty(0, dtype=np.int64))
    for v in nums[:n]:
        for k in range(n, 0, -1):
            bu0[k] = np.concatenate((bu0[k] - v, bu0[k - 1] + v))
        bu0[0] = bu0[0] - v
    for v in nums[n:]:
        for k in range(n, 0, -1):
            bu1[k] = np.concatenate((bu1[k] - v, bu1[k - 1] + v))
        bu1[0] = bu1[0] - v
    for k in range(n + 1):
        bu0[k].sort()
        bu1[k].sort()
    best = 1 << 60
    for k1 in range(n + 1):
        A = bu0[k1]
        B = bu1[n - k1]
        nb = B.shape[0]
        if nb == 0 or A.shape[0] == 0:
            continue
        lo = np.searchsorted(B, -A)
        i1 = np.clip(lo, 0, nb - 1)
        i2 = np.clip(lo - 1, 0, nb - 1)
        v1 = np.abs(A + B[i1]).min()
        v2 = np.abs(A + B[i2]).min()
        v = v1 if v1 < v2 else v2
        if v < best:
            best = v
            if best == 0:
                return 0
    return int(best)


def _kernel_py(nums):
    n = len(nums) >> 1
    bu0 = [[0]]
    bu1 = [[0]]
    for _ in range(n):
        bu0.append([])
        bu1.append([])
    for v in nums[:n]:
        for k in range(n, 0, -1):
            bu0[k] = [x - v for x in bu0[k]] + [x + v for x in bu0[k - 1]]
        bu0[0] = [x - v for x in bu0[0]]
    for v in nums[n:]:
        for k in range(n, 0, -1):
            bu1[k] = [x - v for x in bu1[k]] + [x + v for x in bu1[k - 1]]
        bu1[0] = [x - v for x in bu1[0]]
    for k in range(n + 1):
        bu0[k].sort()
        bu1[k].sort()
    best = 1 << 60
    for k1 in range(n + 1):
        A = bu0[k1]
        B = bu1[n - k1]
        i = 0
        j = len(B) - 1
        na = len(A)
        while i < na and j >= 0:
            s = A[i] + B[j]
            if s < 0:
                v = -s
                i += 1
            else:
                v = s
                j -= 1
            if v < best:
                best = v
                if v == 0:
                    return 0
    return best


def _minimum_difference_kernel(nums):
    if _np is not None:
        return _kernel_np(nums, _np)
    return _kernel_py(nums)


class Solution:
    def minimumDifference(self, nums):
        return _minimum_difference_kernel(nums)

    def minimum_difference(self, nums):
        return _minimum_difference_kernel(nums)
