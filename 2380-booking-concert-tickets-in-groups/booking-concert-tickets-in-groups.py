class BookMyShow:
    
    def __init__(self, n: int, m: int):
        self.n = n
        self.m = m
        self.used = [0] * n
        self.sum = [0] * (4 * n)
        self.mx = [0] * (4 * n)
        self.ptr = 0
        self.build(1, 0, n - 1)

    def build(self, node, l, r):
        if l == r:
            self.sum[node] = self.m
            self.mx[node] = self.m
            return
        mid = (l + r) // 2
        self.build(node * 2, l, mid)
        self.build(node * 2 + 1, mid + 1, r)
        self.pull(node)

    def pull(self, node):
        self.sum[node] = self.sum[node * 2] + self.sum[node * 2 + 1]
        self.mx[node] = max(self.mx[node * 2], self.mx[node * 2 + 1])

    def update(self, node, l, r, idx, val):
        if l == r:
            self.sum[node] = val
            self.mx[node] = val
            return

        mid = (l + r) // 2
        if idx <= mid:
            self.update(node * 2, l, mid, idx, val)
        else:
            self.update(node * 2 + 1, mid + 1, r, idx, val)

        self.pull(node)

    def query_first(self, node, l, r, maxRow, k):
        if l > maxRow or self.mx[node] < k:
            return -1

        if l == r:
            return l

        mid = (l + r) // 2

        left = self.query_first(node * 2, l, mid, maxRow, k)
        if left != -1:
            return left

        return self.query_first(node * 2 + 1, mid + 1, r, maxRow, k)

    def query_sum(self, node, l, r, ql, qr):
        if ql > r or qr < l:
            return 0

        if ql <= l and r <= qr:
            return self.sum[node]

        mid = (l + r) // 2

        return (self.query_sum(node * 2, l, mid, ql, qr) +
                self.query_sum(node * 2 + 1, mid + 1, r, ql, qr))

    def gather(self, k: int, maxRow: int):
        row = self.query_first(1, 0, self.n - 1, maxRow, k)

        if row == -1:
            return []

        seat = self.used[row]
        self.used[row] += k

        self.update(1, 0, self.n - 1, row, self.m - self.used[row])

        return [row, seat]

    def scatter(self, k: int, maxRow: int) -> bool:
        if self.query_sum(1, 0, self.n - 1, 0, maxRow) < k:
            return False

        while k > 0:
            if self.ptr > maxRow:
                break

            remain = self.m - self.used[self.ptr]

            if remain == 0:
                self.ptr += 1
                continue

            take = min(remain, k)
            self.used[self.ptr] += take
            k -= take

            self.update(1, 0, self.n - 1, self.ptr,
                        self.m - self.used[self.ptr])

            if self.used[self.ptr] == self.m:
                self.ptr += 1

        return True