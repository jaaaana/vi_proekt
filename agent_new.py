from searching_framework import Problem, astar_search
from grids import grids
from solutions import solutions
import random
from yellow_tile_script import *

gray = 2
yellow = 1


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


def secondary_tiebreaker(state):
    colors = state[0]
    green_count = sum(row.count(0) for row in colors)
    return green_count


class WaffleAgent(Problem):
    def __init__(self, initial, starting, goal_grid, total, correct):
        super().__init__((initial, starting, correct))
        self.goal = ((0, 0, 0, 0, 0), (0, 0, 0, 0, 0), (0, 0, 0, 0, 0), (0, 0, 0, 0, 0), (0, 0, 0, 0, 0))
        self.goal_grid = goal_grid
        self.total = total

    # def h(self, node):
    #     sum = 0
    #     for row in node.state[0]:
    #         for r in row:
    #             sum += r
    #     # if node.depth < 7:
    #     # sum -= (10 - node.depth)
    #     return sum - 1 * secondary_tiebreaker(node.state)

    # def h(self, node):
    #     misplaced = 0
    #     for i in range(5):
    #         for j in range(5):
    #             if node.state[1][i][j] != self.goal_grid[i][j]:
    #                 misplaced += 1
    #     # penalty = max(0, 10 - node.depth)
    #     return misplaced - node.depth

    def h(self, node):
        misplaced = 0
        green_bonus = 0
        grid, colors = node.state[1], node.state[0]
        for i in range(5):
            for j in range(5):
                if grid[i][j] != self.goal_grid[i][j]:
                    misplaced += 1
                if colors[i][j] == 0:
                    green_bonus += 2
        return (misplaced - green_bonus) - 0.1 * secondary_tiebreaker(node.state)

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
        new_grid = [list(row) for row in grid]

        new_grid[x1][y1], new_grid[x2][y2] = new_grid[x2][y2], new_grid[x1][y1]

        new_colors, correct_dict = refresh_colors(new_grid, self.goal_grid, self.total, correct_dict, colors)

        new_color_sum = sum(sum(row) for row in new_colors)
        if new_color_sum >= initial_color_sum:
            return None

        new_state = (
            tuple(tuple(row) for row in new_colors),
            tuple(tuple(row) for row in new_grid),
            dict_to_tuple(correct_dict)
        )

        return new_state

    def goal_test(self, state):
        return self.goal == state[0]


def main(number):
    original_grid = read_grid(grids[number])
    solution_grid = read_grid(solutions[number])

    total_dict, green_dict = create_dictionaries(solution_grid)

    initial, green_dict = initial_colors(original_grid, solution_grid, total_dict, green_dict)

    initial_state = tuple(tuple(row) for row in initial)

    waffle = WaffleAgent(initial_state, original_grid, solution_grid, total_dict,
                         dict_to_tuple(green_dict))
    node = astar_search(waffle)
    suma = 0
    if node is not None:
        print(node.solution())
        print(len(node.solution()))
        states = node.solve()
        return node.solution()
        # for state in states:
        #     print('colors', state[0])
        #     print('grid', state[1])
        #     print('correct', state[2])
        #     suma = sum(sum(row) for row in state[0])
        #     print(suma)
        # if len(node.solution()) > 10:
        #     print(random_choice, ";", len(node.solution()))
    else:
        print("no sol")
        return None


if __name__ == '__main__':
    main(1)