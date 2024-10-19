from searching_framework import Problem, astar_search
from grids import grids
from solutions import solutions
import random

gray = 2
yellow = 1


def dict_to_tuple(d):
    result = []
    for key, value in d.items():
        if isinstance(value, dict):
            # Recursively convert nested dictionaries to tuples
            result.append((key, dict_to_tuple(value)))
        else:
            result.append((key, value))
    return tuple(result)


def tuple_to_dict(t):
    result = {}
    for key, value in t:
        if isinstance(value, tuple):
            # Recursively convert nested tuples back to dictionaries
            result[key] = tuple_to_dict(value)
        else:
            result[key] = value
    return result


def check_yellow(i, j, original, solution, total, correct):
    # Check if the original grid character is present in the horizontal or vertical lines
    # for rows 0, 2, 4 or columns 0, 2, 4
    letter = original[i][j]
    in_row = letter in [solution[i][k] for k in range(5) if i in (0, 2, 4)]
    if in_row:
        if total[i // 2][letter] > correct[i // 2][letter]:
            return True
    in_col = letter in [solution[k][j] for k in range(5) if j in (0, 2, 4)]
    if in_col:
        if total[j // 2 + 3][letter] > correct[j // 2 + 3][letter]:
            return True

    # Check for rows 1, 3 or columns 1, 3
    in_row_1_3 = letter in [solution[i][k] for k in range(5) if j in (1, 3)]
    if in_row_1_3:
        if total[i // 2][letter] > correct[i // 2][letter]:
            return True
    in_col_1_3 = letter in [solution[k][j] for k in range(5) if i in (1, 3)]
    if in_col_1_3:
        if total[j // 2 + 3][letter] > correct[j // 2 + 3][letter]:
            return True

    # Return True if any of the conditions are met
    return False


def foo(grid):
    rechnik1 = {}
    rechnik2 = {}
    for i in (0, 2, 4):
        for j in range(5):
            if i // 2 not in rechnik1:
                rechnik1[i // 2] = {}
                rechnik2[i // 2] = {}
            if grid[i][j] not in rechnik1[i // 2]:
                rechnik1[i // 2][grid[i][j]] = 0
                rechnik2[i // 2][grid[i][j]] = 0
            rechnik1[i // 2][grid[i][j]] += 1

    for j in (0, 2, 4):
        for i in range(5):
            if j // 2 + 3 not in rechnik1:
                rechnik1[j // 2 + 3] = {}
                rechnik2[j // 2 + 3] = {}
            if grid[i][j] not in rechnik1[j // 2 + 3]:
                rechnik1[j // 2 + 3][grid[i][j]] = 0
                rechnik2[j // 2 + 3][grid[i][j]] = 0
            rechnik1[j // 2 + 3][grid[i][j]] += 1

    return rechnik1, rechnik2


def read_grid(string):
    grid = []
    for i in range(5):
        grid.append(tuple(string[i * 5:i * 5 + 5]))
    return tuple(grid)


class WaffleAgent(Problem):
    def __init__(self, initial, starting, goal_grid, total, correct):
        super().__init__((initial, starting, correct))
        self.goal = ((0, 0, 0, 0, 0), (0, 0, 0, 0, 0), (0, 0, 0, 0, 0), (0, 0, 0, 0, 0), (0, 0, 0, 0, 0))
        self.goal_grid = goal_grid
        self.total = total

    def h(self, node):
        zbir2 = 0
        for row in node.state[0]:
            for r in row:
                zbir2 += r
        return zbir2
        # mis = 0
        # for row in node.state[0]:
        #     for r in row:
        #         if r != 0:
        #             mis += 1
        # return mis / 2

    def actions(self, state):
        return self.successor(state).keys()

    def result(self, state, action):
        return self.successor(state)[action]

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

        zbir1 = 0
        for row in state[0]:
            for r in row:
                zbir1 += r

        state = list(state)
        new_colors = []
        new_grid = []
        colors = state[0]
        grid = state[1]
        correct = tuple_to_dict(state[2])
        for row1, row2 in zip(colors, grid):
            new_colors.append(list(row1))
            new_grid.append(list(row2))

        new_grid[x1][y1], new_grid[x2][y2] = new_grid[x2][y2], new_grid[x1][y1]
        first, second = new_grid[x1][y1], new_grid[x2][y2]
        if first == self.goal_grid[x1][y1]:
            if x1 in (0, 2, 4):
                correct[x1 // 2][first] += 1
            if y1 in (0, 2, 4):
                correct[y1 // 2 + 3][first] += 1
            new_colors[x1][y1] = 0
        elif check_yellow(x1, y1, state[1], self.goal_grid, self.total, correct):
            new_colors[x1][y1] = yellow
        else:
            new_colors[x1][y1] = gray

        if second == self.goal_grid[x2][y2]:
            if x2 in (0, 2, 4):
                correct[x2 // 2][second] += 1
            if y2 in (0, 2, 4):
                correct[y2 // 2 + 3][second] += 1
            new_colors[x2][y2] = 0
        elif check_yellow(x2, y2, state[1], self.goal_grid, self.total, correct):
            new_colors[x2][y2] = yellow
        else:
            new_colors[x2][y2] = gray

        zbir2 = 0
        for row in new_colors:
            for r in row:
                zbir2 += r

        if zbir2 > zbir1:
            return None

        new_col = []
        new_gr = []

        for row1, row2 in zip(new_colors, new_grid):
            r1 = tuple(row1)
            new_col.append(r1)
            r2 = tuple(row2)
            new_gr.append(r2)
        new_state = (tuple(new_col), tuple(new_gr), dict_to_tuple(correct))

        return new_state

    def goal_test(self, state):
        return self.goal == state[0]


if __name__ == '__main__':
    # random_choice = random.randint(0, 100)
    # file = open('./results.txt', 'w')
    for random_choice in range(100):
        random_choice = 80
        original_grid = read_grid(grids[random_choice])
        solution_grid = read_grid(solutions[random_choice])

        # print(random_choice)
        # print(original_grid)
        # print(solution_grid)

        total, correct = foo(solution_grid)

        initial = [[0 for _ in range(5)] for _ in range(5)]

        for i in range(5):
            for j in range(5):
                if solution_grid[i][j] == original_grid[i][j]:
                    if i in (0, 2, 4):
                        correct[i // 2][original_grid[i][j]] += 1
                    if j in (0, 2, 4):
                        correct[j // 2 + 3][original_grid[i][j]] += 1

        for i in range(5):
            for j in range(5):
                if solution_grid[i][j] == original_grid[i][j]:
                    continue
                elif check_yellow(i, j, original_grid, solution_grid, total, correct):
                    initial[i][j] = yellow
                else:
                    initial[i][j] = gray

        # print(correct)

        in_state = []
        for i in range(5):
            red = tuple(initial[i])
            in_state.append(red)

        in_state = tuple(in_state)
        waffle = WaffleAgent(in_state, original_grid, solution_grid, total, dict_to_tuple(correct))
        node = astar_search(waffle)
        if node is not None:
            print(node.solution())
            print(len(node.solution()))
            print(random_choice)
            # file.write(f'{random_choice}: {len(node.solution())}\n')
            states = node.solve()
            for state in states:
                sum = 0
                colors = state[0]
                for row in colors:
                    for r in row:
                        sum += r
                print(sum)
        else:
            print("retardiran si")
        break
