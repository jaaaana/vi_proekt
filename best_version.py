from searching_framework import Problem, astar_search
from grids import grids
from solutions import solutions
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
    def __init__(self, initial, starting, goal_grid, total, correct):
        super().__init__((initial, starting, correct))
        self.goal = ((0, 0, 0, 0, 0), (0, 0, 0, 0, 0), (0, 0, 0, 0, 0), (0, 0, 0, 0, 0), (0, 0, 0, 0, 0))
        self.goal_grid = goal_grid
        self.total = total

    def h(self, node):
        suma1 = 0
        for row in node.state[0]:
            for r in row:
                suma1 += r
        suma2 = suma1
        suma1 -= (10 - node.depth)
        misplaced = 0
        for row in node.state[0]:
            misplaced += 5 - row.count(0)
        return min([suma1, suma2, misplaced])

    def actions(self, state):
        return self.successor(state).keys()

    def result(self, state, action):
        return self.successor(state)[action]

    def successor(self, state):
        neighbors = {}

        optimal_swap = generate_optimal_move((state[0], state[1]), self.goal_grid)
        if optimal_swap is not None:
            action = 'swap_' + str(optimal_swap[0]) + str(optimal_swap[1]) + '_' + str(optimal_swap[2]) + str(
                optimal_swap[3])
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
    if node is not None:
        if len(node.solution()) > 10:
            print(number, ";", len(node.solution()))
    else:
        print("no sol")
    print(node.solution())
    return node.solution()


if __name__ == '__main__':
    suma = 0
    for i in range(100):
        print(i)
        suma += len(main(10))
        break

    print(suma)
    # suma = 1011
    # happy accident: suma = 1001
