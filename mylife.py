ALIVE = '* '
EMPTY = '- '

class Grid(object):
    def __init__(self, w, h):
        self.w = w
        self.h = h
        self.rows = []
        for _ in range(self.h):
            self.rows.append([EMPTY] * self.w)

    def __str__(self):
        str = ''
        for i in self.rows:
            str += '\n'
            str += ''.join(i)
        return str

    def neighbor_count(self, x, y):
        n_ = grid.query(x, y+1)
        ne = grid.query(x+1, y+1)
        e_ = grid.query(x+1, y)
        se = grid.query(x+1, y-1)
        s_ = grid.query(x, y-1)
        sw = grid.query(x-1, y-1)
        w_ = grid.query(x-1, y)
        nw = grid.query(x-1, y+1)
        neighbors = [n_, ne, e_, se, s_, sw, w_, nw]
        
        count = 0
        for n in neighbors:
            if n == ALIVE:
                count += 1
        return count

    def compute_state(self, ncount, currstate):
        if currstate == ALIVE:
            if ncount < 2:
                return EMPTY
            elif ncount > 3:
                return EMPTY
        else:
            if ncount == 3:
                return ALIVE
        return currstate

    def query(self, x, y):
        return self.rows[y % self.h][x % self.w]

    def assign(self, x, y, state):
        self.rows[y % self.h][x % self.w] = state

    def step(self):
        assign_list = []
        for y in range(grid.h):
            for x in range(grid.w):
                ncount = self.neighbor_count(x,y)
                new_state = self.compute_state(ncount, self.query(x,y))
                if new_state != self.query(x,y):
                    assign_list.append((x,y,new_state))
        for t in assign_list:
            self.assign(t[0], t[1], t[2])


def print_ncount(grid):
    for y in range(grid.h):
        for x in range(grid.w):
            ncount = grid.neighbor_count(x, y)
            print(ncount, grid.query(x, y), end="", sep="")
        print()


if __name__ == "__main__":
    grid = Grid(10, 10)

    grid.assign(3, 1, ALIVE)
    grid.assign(4, 2, ALIVE)
    grid.assign(2, 3, ALIVE)
    grid.assign(3, 3, ALIVE)
    grid.assign(4, 3, ALIVE)

    print(grid)

    for i in range(10):
        grid.step()
        print(grid)
