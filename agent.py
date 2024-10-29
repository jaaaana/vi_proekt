from searching_framework import Problem, astar_search
from grids import grids
from solutions import solutions
import random

gray = 10
yellow = 5


def dict_to_tuple(d):
    result = []
    for key, value in d.items():
        if isinstance(value, dict):
            result.append((key, dict_to_tuple(value)))
        else:
            result.append((key, value))
    return tuple(result)


def tuple_to_dict(t):
    result = {}
    for key, value in t:
        if isinstance(value, tuple):
            result[key] = tuple_to_dict(value)
        else:
            result[key] = value
    return result


def check_yellow(i, j, original, solution, total, correct):
    letter = original[i][j]
    in_row = letter in [solution[i][k] for k in range(5) if i in (0, 2, 4)]
    if in_row:
        if total[i // 2][letter] > correct[i // 2][letter]:
            return True
    in_col = letter in [solution[k][j] for k in range(5) if j in (0, 2, 4)]
    if in_col:
        if total[j // 2 + 3][letter] > correct[j // 2 + 3][letter]:
            return True
    in_row_1_3 = letter in [solution[i][k] for k in range(5) if j in (1, 3)]
    if in_row_1_3:
        if total[i // 2][letter] > correct[i // 2][letter]:
            return True
    in_col_1_3 = letter in [solution[k][j] for k in range(5) if i in (1, 3)]
    if in_col_1_3:
        if total[j // 2 + 3][letter] > correct[j // 2 + 3][letter]:
            return True

    return False


def create_dictionaries(grid):
    total = {}
    correct = {}
    for i in (0, 2, 4):
        for j in range(5):
            if i // 2 not in total:
                total[i // 2] = {}
                correct[i // 2] = {}
            if grid[i][j] not in total[i // 2]:
                total[i // 2][grid[i][j]] = 0
                correct[i // 2][grid[i][j]] = 0
            total[i // 2][grid[i][j]] += 1

    for j in (0, 2, 4):
        for i in range(5):
            if j // 2 + 3 not in total:
                total[j // 2 + 3] = {}
                correct[j // 2 + 3] = {}
            if grid[i][j] not in total[j // 2 + 3]:
                total[j // 2 + 3][grid[i][j]] = 0
                correct[j // 2 + 3][grid[i][j]] = 0
            total[j // 2 + 3][grid[i][j]] += 1

    return total, correct


def read_grid(string):
    grid = []
    for i in range(5):
        grid.append(tuple(string[i * 5:i * 5 + 5]))
    return tuple(grid)


def is_valid(i, j, k, l, moves, state):
    if (i, j) == (1, 1) or (k, l) == (1, 1) or (i, j) == (1, 3) or (k, l) == (1, 3) or (i, j) == (
            3, 1) or (k, l) == (3, 1) or (i, j) == (3, 3) or (k, l) == (3, 3):
        return False
    if (i, j) == (k, l):
        return False
    if ((k, l), (i, j)) in moves:
        return False
    if state[i][j] == 0 or state[k][l] == 0:
        return False
    return True


class WaffleAgent(Problem):
    def __init__(self, initial, starting, goal_grid, total, correct):
        super().__init__((initial, starting, correct))
        self.goal = ((0, 0, 0, 0, 0), (0, 0, 0, 0, 0), (0, 0, 0, 0, 0), (0, 0, 0, 0, 0), (0, 0, 0, 0, 0))
        self.goal_grid = goal_grid
        self.total = total

    def h(self, node):
        sum = 0
        for row in node.state[0]:
            for r in row:
                sum += r
        return sum

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
                        if is_valid(i, j, k, l, moves, state[0]):
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

        initial_color_sum = sum(sum(row) for row in state[0])

        colors, grid, correct = state
        correct_dict = tuple_to_dict(correct)
        new_colors = [list(row) for row in colors]
        new_grid = [list(row) for row in grid]

        new_grid[x1][y1], new_grid[x2][y2] = new_grid[x2][y2], new_grid[x1][y1]
        first, second = new_grid[x1][y1], new_grid[x2][y2]

        if first == self.goal_grid[x1][y1]:
            if x1 in (0, 2, 4):
                correct_dict[x1 // 2][first] += 1
            if y1 in (0, 2, 4):
                correct_dict[y1 // 2 + 3][first] += 1
            new_colors[x1][y1] = 0
        elif check_yellow(x1, y1, grid, self.goal_grid, self.total, correct_dict):
            new_colors[x1][y1] = yellow
        else:
            new_colors[x1][y1] = gray

        if second == self.goal_grid[x2][y2]:
            if x2 in (0, 2, 4):
                correct_dict[x2 // 2][second] += 1
            if y2 in (0, 2, 4):
                correct_dict[y2 // 2 + 3][second] += 1
            new_colors[x2][y2] = 0
        elif check_yellow(x2, y2, grid, self.goal_grid, self.total, correct_dict):
            new_colors[x2][y2] = yellow
        else:
            new_colors[x2][y2] = gray

        new_color_sum = sum(sum(row) for row in new_colors)
        if new_color_sum > initial_color_sum:
            return None

        new_state = (
            tuple(tuple(row) for row in new_colors),
            tuple(tuple(row) for row in new_grid),
            dict_to_tuple(correct_dict)
        )

        return new_state

    def goal_test(self, state):
        return self.goal == state[0]


if __name__ == '__main__':
    for random_choice in range(100):
        random_choice = 36
        original_grid = read_grid(grids[random_choice])
        solution_grid = read_grid(solutions[random_choice])

        total, correct = create_dictionaries(solution_grid)

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

        initial_state = tuple(tuple(row) for row in initial)

        waffle = WaffleAgent(initial_state, original_grid, solution_grid, total, dict_to_tuple(correct))
        node = astar_search(waffle)
        if node is not None:
            print(node.solution())
            print(len(node.solution()))
            states = node.solve()
            for state in states:
                suma = sum(sum(row) for row in state[0])
                print(suma)
        else:
            print("No solution")
        break
