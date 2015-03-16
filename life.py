from collections import namedtuple
import pdb

Query = namedtuple('Query', ('y', 'x'))
Transition = namedtuple('Transition', ('y', 'x', 'state'))

ALIVE = '*'
EMPTY = '-'
TICK = object()

grid = Grid(5,9)

class GenReturn(Exception):
    def __init__(self, value):
        self.value = value
        

class Grid(object):
    def __init__(self, h, w):
        self.h = h
        self.w = w
        self.rows = []
        for _ in range(self.h):
            self.rows.append([EMPTY] * self.w)

    def __str__(self):
        str = ''
        for i in self.rows:
            #print(i)
            str += ''.join(i)
            str += '\n'
        return str

    def query(self, y, x):
        return self.rows[y % self.h][x % self.w]

    def assign(self, y, x, state):
        self.rows[y % self.h][x % self.w] = state


def game_logic(state, neighbors):
    print "state:", state
    if state == ALIVE:
        if neighbors < 2:
            return EMPTY
        elif neighbors > 3:
            return EMPTY
    else:
        if neighbors == 3:
            return ALIVE
    return state


def live_a_generation(grid, sim):
    progeny = Grid(grid.h, grid.w)
    item = next(sim)
    while item is not TICK:
        if isinstance(item, Query):
            state = grid.query(item.y, item.x)
            item = sim.send(state)
        else:
            progeny.assign(item.y, item.x, item.state)
            item = next(sim)
    return progeny
            

def count_neighbors(y,x):
    n_ = yield Query(y+1, x+0)
    ne = yield Query(y+1, x+1)
    e_ = yield Query(y+0, x+1)
    se = yield Query(y-1, x+1)
    s_ = yield Query(y-1, x+0)
    sw = yield Query(y-1, x-1)
    w_ = yield Query(y+0, x-1)
    nw = yield Query(y+1, x-1)
    
    neighbor_states = [n_, ne, e_, se, s_, sw, w_, nw]
    count = 0
    for state in neighbor_states:
        if state == ALIVE:
            count += 1

    raise GenReturn(count)


def step_cell(y,x):
    q = Query(y,x)
    state = yield grid.query(q.y, q.x)
    neighbors = 0
    fake_neighbors = 0
    try:
        for n in count_neighbors(y,x):
            yield n
            if grid.query(n.y, n.x) == ALIVE:
                neighbors += 1
    except GenReturn as e:
        fake_neighbors = e.value

    # print "(", y, x, ") neighbors:", neighbors, " fake_neighbors:", fake_neighbors

    next_state = game_logic(state, neighbors)
    # print "nex_state:", next_state
    yield Transition(y, x, next_state)


def simulate(h,w):
    while True:
        for x in range(h):
            for y in range(w):
                for i in step_cell(y,x):
                    yield i
        yield TICK


if __name__ == "__main__":
    # Assign initial ALIVE cells
    grid.assign(0, 3, ALIVE)
    grid.assign(1, 4, ALIVE)
    grid.assign(2, 2, ALIVE)
    grid.assign(2, 3, ALIVE)
    grid.assign(2, 4, ALIVE)

    sim = simulate(grid.w, grid.h)
    print
    for i in range(10):
        print(grid)
        grid = live_a_generation(grid, sim)
