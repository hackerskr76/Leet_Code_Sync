class BookMyShow:

    def __init__(self, n: int, m: int):
        self.n = n
        self.m = m
        self.used = [0] * n
        self.ptr = 0

        size = 4 * n
        self.sum = [0] * size
        self.mx = [0] * size

        self.build(1, 0, n - 1)

    def build(self, node, l, r):
        if l == r:
            self.sum[node] = self.m
            self.mx[node] = self.m
            return

        mid = (l + r) >> 1
        self.build(node << 1, l, mid)
        self.build(node << 1 | 1, mid + 1, r)

        self.sum[node] = self.sum[node << 1] + self.sum[node << 1 | 1]
        self.mx[node] = max(self.mx[node << 1], self.mx[node << 1 | 1])

    def update(self, node, l, r, idx, val):
        if l == r:
            self.sum[node] = val
            self.mx[node] = val
            return

        mid = (l + r) >> 1

        if idx <= mid:
            self.update(node << 1, l, mid, idx, val)
        else:
            self.update(node << 1 | 1, mid + 1, r, idx, val)

        self.sum[node] = self.sum[node << 1] + self.sum[node << 1 | 1]
        self.mx[node] = max(self.mx[node << 1], self.mx[node << 1 | 1])

    def query_first(self, node, l, r, maxRow, k):
        if l > maxRow or self.mx[node] < k:
            return -1

        if l == r:
            return l

        mid = (l + r) >> 1

        if self.mx[node << 1] >= k:
            res = self.query_first(node << 1, l, mid, maxRow, k)
            if res != -1:
                return res

        return self.query_first(node << 1 | 1, mid + 1, r, maxRow, k)

    def query_sum(self, node, l, r, ql, qr):
        if ql <= l and r <= qr:
            return self.sum[node]

        if r < ql or l > qr:
            return 0

        mid = (l + r) >> 1

        if qr <= mid:
            return self.query_sum(node << 1, l, mid, ql, qr)

        if ql > mid:
            return self.query_sum(node << 1 | 1, mid + 1, r, ql, qr)

        return (self.query_sum(node << 1, l, mid, ql, qr) +
                self.query_sum(node << 1 | 1, mid + 1, r, ql, qr))

    def gather(self, k: int, maxRow: int):
        row = self.query_first(1, 0, self.n - 1, maxRow, k)

        if row == -1:
            return []

        seat = self.used[row]
        self.used[row] += k

        self.update(1, 0, self.n - 1, row, self.m - self.used[row])

        return [row, seat]

    def scatter(self, k: int, maxRow: int):
        if self.query_sum(1, 0, self.n - 1, 0, maxRow) < k:
            return False

        while k:
            remain = self.m - self.used[self.ptr]

            if remain <= k:
                k -= remain
                self.used[self.ptr] = self.m
                self.update(1, 0, self.n - 1, self.ptr, 0)
                self.ptr += 1
            else:
                self.used[self.ptr] += k
                self.update(
                    1,
                    0,
                    self.n - 1,
                    self.ptr,
                    self.m - self.used[self.ptr],
                )
                return True

        return True