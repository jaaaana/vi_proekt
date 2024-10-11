from searching_framework import Problem


class WaffleAgent(Problem):
    def __init__(self, initial, starting, goal_grid):
        super().__init__((initial, starting))
        self.starting = starting
        self.goal = ((0, 0, 0, 0, 0), (0, 0, 0, 0, 0), (0, 0, 0, 0, 0), (0, 0, 0, 0, 0), (0, 0, 0, 0, 0))
        self.goal_grid = goal_grid

    def actions(self, state):
        return

    def successor(self, state):
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


        new_col = []
        new_gr = []

        for row1, row2 in zip (new_colors, new_grid):
            r1 = tuple(row1)
            new_col.append(r1)
            r2 = tuple(row2)
            new_gr.append(r2)

        new_state = (tuple(new_col), tuple(new_gr))

        return new_state






if __name__ == '__main__':
