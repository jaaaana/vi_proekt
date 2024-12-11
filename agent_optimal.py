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


def generate_optimal_moves(state, solution):
    swaps = []
    colors, grid = state
    for i in range(5):
        for j in range(5):
            if colors[i][j] == 0:
                continue
            for k in range(5):
                for l in range(5):
                    if (i, j) == (k, l) or colors[k][l] == 0:
                        continue
                    if (
                            grid[i][j] == solution[k][l]
                            and grid[k][l] == solution[i][j]
                    ):
                        swaps.append((i, j, k, l))
    return swaps


def generate_optimal_move(state, solution):
    colors, grid = state
    for i in range(5):
        for j in range(5):
            if colors[i][j] == 0:
                continue
            for k in range(5):
                for l in range(5):
                    if (i, j) == (k, l) or colors[k][l] == 0:
                        continue
                    if (
                            grid[i][j] == solution[k][l]
                            and grid[k][l] == solution[i][j]
                    ):
                        return i, j, k, l
    return None


class WaffleAgent(Problem):
    def __init__(self, initial, starting, goal_grid, total, correct, path):
        super().__init__((initial, starting, correct, path))
        self.goal = ((0, 0, 0, 0, 0), (0, 0, 0, 0, 0), (0, 0, 0, 0, 0), (0, 0, 0, 0, 0), (0, 0, 0, 0, 0))
        self.goal_grid = goal_grid
        self.total = total

    # def h(self, node):
    #     sum = 0
    #     for row in node.state[0]:
    #         for r in row:
    #             sum += r
    #     # if node.depth < 7:
    #     sum -= (10 - node.depth)
    #     return sum - 1 * secondary_tiebreaker(node.state)

    def h(self, node):
        misplaced = 0
        for i in range(5):
            for j in range(5):
                if node.state[1][i][j] != self.goal_grid[i][j]:
                    misplaced += 1
        # penalty = max(0, 10 - node.depth)
        return misplaced - 0.1 * secondary_tiebreaker(node.state)

    # def h(self, node):
    #     misplaced = 0
    #     green_bonus = 0
    #     grid, colors = node.state[1], node.state[0]
    #     for i in range(5):
    #         for j in range(5):
    #             if grid[i][j] != self.goal_grid[i][j]:
    #                 misplaced += 1
    #             if colors[i][j] == 0:
    #                 green_bonus += 2
    #     return (misplaced - green_bonus) - 0.1 * secondary_tiebreaker(node.state)

    def actions(self, state):
        return self.successor(state).keys()

    def result(self, state, action):
        return self.successor(state)[action]

    def successor(self, state):
        neighbors = {}

        optimal_swap = generate_optimal_move((state[0], state[1]), self.goal_grid)
        if optimal_swap is not None:
            action = 'swap_' + str(optimal_swap[0]) + str(optimal_swap[1]) + '_' + str(optimal_swap[2]) + str(optimal_swap[3])
            move = (optimal_swap[:2], optimal_swap[2:])
            res = self.generate_state(state, move)
            if res is not None:
                neighbors[action] = res
                return neighbors

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

        colors, grid, correct, path = state
        correct_dict = tuple_to_dict(correct)
        new_grid = [list(row) for row in grid]
        new_path = list(path)

        # swaps = generate_optimal_moves((new_colors, new_grid), self.goal_grid)
        # for swap in swaps:
        #     i, j, k, l = swap
        #     if not is_valid(i, j, k, l, [], new_colors):
        #         continue
        #     new_grid[i][j], new_grid[k][l] = new_grid[k][l], new_grid[i][j]
        #     new_colors, correct_dict = refresh_colors(new_grid, self.goal_grid, self.total, correct_dict, new_colors)
        #     new_path.append('swap_' + str(i) + str(j) + '_' + str(k) + str(l))
        #
        # if is_valid(x1, y1, x2, y2, [], new_colors):
        #     new_grid[x1][y1], new_grid[x2][y2] = new_grid[x2][y2], new_grid[x1][y1]
        #     new_colors, correct_dict = refresh_colors(new_grid, self.goal_grid, self.total, correct_dict, colors)
        #     new_color_sum = sum(sum(row) for row in new_colors)
        #     if new_color_sum >= initial_color_sum:
        #         return None
        #     new_path.append('swap_' + str(x1) + str(y1) + '_' + str(x2) + str(y2))
        #     optimal_swaps = generate_optimal_moves((new_colors, new_grid), self.goal_grid)
        #     for a, swap in enumerate(optimal_swaps):
        #         i, j, k, l = swap
        #         if not is_valid(i, j, k, l, [], new_colors):
        #             continue
        #         new_grid[i][j], new_grid[k][l] = new_grid[k][l], new_grid[i][j]
        #         new_colors, correct_dict = refresh_colors(new_grid, self.goal_grid, self.total, correct_dict,
        #                                                   new_colors)
        #         new_path.append('swap_' + str(i) + str(j) + '_' + str(k) + str(l))

        new_grid[x1][y1], new_grid[x2][y2] = new_grid[x2][y2], new_grid[x1][y1]
        new_colors, correct_dict = refresh_colors(new_grid, self.goal_grid, self.total, correct_dict, colors)
        new_color_sum = sum(sum(row) for row in new_colors)
        if new_color_sum >= initial_color_sum:
            return None

        new_state = (
            tuple(tuple(row) for row in new_colors),
            tuple(tuple(row) for row in new_grid),
            dict_to_tuple(correct_dict),
            tuple(new_path)
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
                         dict_to_tuple(green_dict), ())
    node = astar_search(waffle)
    suma = 0
    if node is not None:
        # print(node.state[3])
        print(node.solution())
        # print(len(node.state[3]))
        print(len(node.solution()))
        return len(node.solution())
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
    # lista = [9, 12, 15, 25, 32, 35, 36, 54, 56, 65, 73, 78, 81, 90, 93, 98]
    # file = open('edinaeski.txt', 'w')
    suma = 0
    for number in range(100):
        # number = 34
        print(number)
        x = main(number)
        suma += x


    print(suma)
