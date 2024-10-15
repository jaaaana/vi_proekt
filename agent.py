from searching_framework import Problem, breadth_first_graph_search
from grids import grids
from solutions import solutions
import random

brojach = 0


def read_grid(string):
    grid = []
    for i in range(5):
        grid.append(tuple(string[i * 5:i * 5 + 5]))
    return tuple(grid)


class WaffleAgent(Problem):
    def __init__(self, initial, starting, goal_grid):
        super().__init__((initial, starting))
        self.starting = starting
        self.goal = ((0, 0, 0, 0, 0), (0, 0, 0, 0, 0), (0, 0, 0, 0, 0), (0, 0, 0, 0, 0), (0, 0, 0, 0, 0))
        self.goal_grid = goal_grid

    def actions(self, state):
        return self.successor(state).keys()

    def result(self, state, action):
        return self.successor(state)[action]

    def successor(self, state):
        global brojach
        print(brojach)
        brojach += 1
        neighbors = {}

        moves = []
        actions = []
        for i in range(5):
            for j in range(5):
                for k in range(5):
                    for l in range(5):
                        if (i, j) == (1, 1) or (k, l) == (1, 1) or (i, j) == (1, 3) or (k, l) == (1, 3) or (i, j) == (
                                3, 1) or (k, l) == (3, 1) or (i, j) == (3, 3) or (k, l) == (3, 3):
                            continue
                        if (i, j) == (k, l):
                            continue
                        if ((k, l), (i, j)) in moves:
                            continue
                        if state[0][i][j] == 0 or state[0][k][l] == 0:
                            continue
                        action = 'swap_' + str(i) + str(j) + '_' + str(k) + str(l)
                        move = ((i, j), (k, l))
                        actions.append(action)
                        moves.append(move)

        for action, move in zip(actions, moves):
            res = self.generate_state(state, move)
            if res is not None:
                neighbors[action] = res
        return neighbors

    def generate_state(self, state, move):
        x1, y1 = move[0]
        x2, y2 = move[1]

        zbir1 = 0
        for row in state[0]:
            for r in row:
                zbir1 += row[r]

        state = list(state)
        new_colors = []
        new_grid = []
        colors = state[0]
        grid = state[1]
        for row1, row2 in zip(colors, grid):
            new_colors.append(list(row1))
            new_grid.append(list(row2))

        new_grid[x1][y1], new_grid[x2][y2] = new_grid[x2][y2], new_grid[x1][y1]
        first, second = new_grid[x1][y1], new_grid[x2][y2]
        if first == self.goal_grid[x1][y1]:
            new_colors[x1][y1] = 0
        elif first in [self.goal_grid[x1][i] for i in range(5)] or first in [self.goal_grid[i][y1] for i in range(5)]:
            new_colors[x1][y1] = 1
        else:
            new_colors[x1][y1] = 2
        if second == self.goal_grid[x2][y2]:
            new_colors[x2][y2] = 0
        elif second in [self.goal_grid[x2][i] for i in range(5)] or second in [self.goal_grid[i][y2] for i in range(5)]:
            new_colors[x2][y2] = 1
        else:
            new_colors[x2][y2] = 2

        zbir2 = 0
        for row in new_colors:
            for r in row:
                zbir2 += row[r]

        if zbir2 > zbir1:
            return None

        new_col = []
        new_gr = []

        for row1, row2 in zip(new_colors, new_grid):
            r1 = tuple(row1)
            new_col.append(r1)
            r2 = tuple(row2)
            new_gr.append(r2)
        br_nuli = 0
        for row in new_col:
            br_nuli += row.count(0)
        print(br_nuli)
        new_state = (tuple(new_col), tuple(new_gr))

        return new_state

    def goal_test(self, state):
        return self.goal == state[0]


if __name__ == '__main__':
    random_choice = random.randint(0, 100)
    original_grid = read_grid(grids[random_choice])
    solution_grid = read_grid(solutions[random_choice])

    print(original_grid)
    print(solution_grid)

    initial = [[0 for _ in range(5)] for _ in range(5)]

    for i in range(5):
        for j in range(5):
            if solution_grid[i][j] == original_grid[i][j]:
                continue
            elif initial[i][j] in [solution_grid[i][k] for k in range(5)] or initial[i][j] in [solution_grid[k][j] for k
                                                                                               in range(5)]:
                initial[i][j] = 1
            else:
                initial[i][j] = 2

    in_state = []
    for i in range(5):
        red = tuple(initial[i])
        in_state.append(red)

    in_state = tuple(in_state)
    waffle = WaffleAgent(in_state, original_grid, solution_grid)
    node = breadth_first_graph_search(waffle)
    if node is not None:
        print(node.solution())
        print(node.solve())
    else:
        print("retardiran si")
