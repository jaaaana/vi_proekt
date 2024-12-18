from grids import grids
from solutions import solutions
from yellow_tile_script import *


def read_grid(string):
    grid = []
    for i in range(5):
        grid.append(list(string[i * 5:i * 5 + 5]))
    return grid


# def find_optimal_swaps(grid, solution, colors):
#     optimal_swaps = []
#     for i in range(5):
#         for j in range(5):
#             for k in range(5):
#                 for l in range(5):
#                     if (k, l, i, j) in optimal_swaps:
#                         continue
#                     if grid[i][j] == solution[k][l] and grid[k][l] == solution[i][j] and \
#                             colors[i][j] != 0 and colors[k][l] != 0:
#                         optimal_swaps.append((i, j, k, l))
#     return optimal_swaps


def find_yellow_swaps(grid, solution, colors, total, green):
    yellow_swaps = []
    for i in range(5):
        for j in range(5):
            for k in range(5):
                for l in range(5):
                    if (k, l, i, j) in yellow_swaps:
                        continue
                    if grid[k][l] == solution[i][j] and colors[k][l] != 0:
                        grid[i][j], grid[k][l] = grid[k][l], grid[i][j]
                        if check_yellow(i, j, grid, solution, total, green):
                            yellow_swaps.append((i, j, k, l))
    return yellow_swaps


def find_first_yellow(grid, solution, total, green):
    new_grid = grid
    for i in range(5):
        for j in range(5):
            if new_grid[i][j] == solution[i][j]:
                continue
            for k in range(5):
                for l in range(5):
                    if new_grid[k][l] == solution[i][j] and colors[k][l] != 0 and colors[i][j] != 0:
                        new_grid[i][j], new_grid[k][l] = new_grid[k][l], new_grid[i][j]
                        if check_yellow(k, l, new_grid, solution, total, green):
                            return i, j, k, l
                        else:
                            new_grid[i][j], new_grid[k][l] = new_grid[k][l], new_grid[i][j]
    return None


# def find_any_swap(grid, solution, colors):
#     for i in range(5):
#         for j in range(5):
#             if grid[i][j] == solution[i][j]:
#                 continue
#             for k in range(5):
#                 for l in range(5):
#                     if grid[k][l] == solution[i][j] and colors[i][j] != 0 and colors[k][l] != 0:
#                         return i, j, k, l
#     return None

def check_valid(i, j, k, l, colors):
    if i == k and j == l:
        return False
    if i == 1 and j == 1:
        return False
    if i == 1 and j == 3:
        return False
    if i == 3 and j == 1:
        return False
    if i == 3 and j == 3:
        return False
    if k == 1 and l == 1:
        return False
    if k == 1 and l == 3:
        return False
    if k == 3 and l == 1:
        return False
    if k == 3 and l == 3:
        return False
    if colors[i][j] == 0 or colors[k][l] == 0:
        return False
    return True


def find_optimal_swaps(grid, solution, colors):
    swaps = []
    for i1 in range(5):
        for j1 in range(5):
            if colors[i1][j1] == 0:
                continue
            for i2 in range(5):
                for j2 in range(5):
                    if (i1, j1) == (i2, j2) or colors[i2][j2]:
                        continue
                    if (
                        grid[i1][j1] == solution[i2][j2]
                        and grid[i2][j2] == solution[i1][j1]
                    ):
                        swaps.append((i1, j1, i2, j2))
    return swaps


def find_yellow_swap(grid, solution, colors, total, green):
    """
    Finds the first swap where one letter ends up in the correct position
    and the other becomes yellow.
    """
    for i1 in range(5):
        for j1 in range(5):
            if colors[i1][j1] == 0:
                continue
            for i2 in range(5):
                for j2 in range(5):
                    if (i1, j1) == (i2, j2):
                        continue
                    # Check if the swap results in a green and yellow
                    if (
                        grid[i1][j1] == solution[i2][j2]
                        and check_yellow(i2, j2, grid, solution, total, green)
                    ):
                        return i1, j1, i2, j2
    return None


def find_any_swap(grid, solution, colors):
    for i1 in range(5):
        for j1 in range(5):
            if colors[i1][j1] == 0:
                continue
            for i2 in range(5):
                for j2 in range(5):
                    if (i1, j1) == (i2, j2):
                        continue
                    if grid[i1][j1] == solution[i2][j2]:
                        return i1, j1, i2, j2
    return None


if __name__ == '__main__':
    yellow = 1
    gray = 2
    number = 0
    grid = grids[number]
    solution = solutions[number]
    original_grid = read_grid(grid)
    solution_grid = read_grid(solution)
    print(solution_grid)
    total, green = create_dictionaries(solution_grid)
    colors, green = initial_colors(original_grid, solution_grid, total, green)

    swaps = []
    # while sum(sum(row) for row in colors) != 0:
    #     optimal_swaps = find_optimal_swaps(original_grid, solution_grid, colors)
    #     print(optimal_swaps)
    #     for s in optimal_swaps:
    #         i, j, k, l = s
    #         if not check_valid(i, j, k, l, colors):
    #             continue
    #         original_grid[i][j], original_grid[k][l] = original_grid[k][l], original_grid[i][j]
    #         swaps.append((i, j, k, l))
    #         colors, green = refresh_colors(original_grid, solution_grid, total, green, colors)
    #
    #     swap = find_first_yellow(original_grid, solution_grid, total, green)
    #     print('y', swap)
    #     if swap is not None:
    #         i, j, k, l = swap
    #     else:
    #         swap = find_any_swap(original_grid, solution_grid, colors)
    #         print('g', swap)
    #         i, j, k, l = swap
    #     print(original_grid)
    #     original_grid[i][j], original_grid[k][l] = original_grid[k][l], original_grid[i][j]
    #     swaps.append((i, j, k, l))
    #
    #     colors, green = refresh_colors(original_grid, solution_grid, total, green, colors)

    print(swaps)
    # for i in range(5):
    #     for j in range(5):
    #         if original_grid[i][j] == solution_grid[i][j]:
    #             continue
    #         letter = solution_grid[i][j]
    #         possible_swaps = []
    #         for k in range(5):
    #             for l in range(5):
    #                 if original_grid[k][l] == letter and colors[k][l] != 0:
    #                     possible_swaps.append((k, l))
    #         flag = False
    #         for k, l in possible_swaps:
    #             if original_grid[i][j] == solution_grid[k][l]:
    #                 swaps.append((i, j, k, l))
    #                 original_grid[i][j], original_grid[k][l] = original_grid[k][l], original_grid[i][j]
    #                 colors, green = refresh_colors(original_grid, solution_grid, total, green, colors)
    #                 flag = True
    #                 break
    #         if flag:
    #             continue
    #
    #         for k, l in possible_swaps:
    #             if original_grid[k][l] == solution_grid[i][j] and colors[k][l] != 0:
    #                 original_grid[i][j], original_grid[k][l] = original_grid[k][l], original_grid[i][j]
    #                 if check_yellow(k, l, original_grid, solution_grid, total, green):
    #                     colors, green = refresh_colors(original_grid, solution_grid, total, green, colors)
    #                     swaps.append((i, j, k, l))
    #                     flag = True
    #                     break
    #                 else:
    #                     original_grid[i][j], original_grid[k][l] = original_grid[k][l], original_grid[i][j]
    #         if flag:
    #             continue
    #
    #         swaps.append((i, j) + possible_swaps[0])

    swaps = []

    while not all(all(row) for row in colors):
        optimal_swaps = find_optimal_swaps(original_grid, solution_grid, colors)
        for swap in optimal_swaps:
            i1, j1, i2, j2 = swap
            original_grid[i1][j1], original_grid[i2][j2] = original_grid[i2][j2], original_grid[i1][j1]
            swaps.append(swap)
            colors, green = refresh_colors(original_grid, solution_grid, total, green, colors)

        yellow_swap = find_yellow_swap(original_grid, solution_grid, colors, total, green)
        if yellow_swap:
            i1, j1, i2, j2 = yellow_swap
            original_grid[i1][j1], original_grid[i2][j2] = original_grid[i2][j2], original_grid[i1][j1]
            swaps.append((i1, j1, i2, j2))
            colors, green = refresh_colors(original_grid, solution_grid, total, green, colors)
            continue

        any_swap = find_any_swap(original_grid, solution_grid, colors)
        if any_swap:
            i1, j1, i2, j2 = any_swap
            original_grid[i1][j1], original_grid[i2][j2] = original_grid[i2][j2], original_grid[i1][j1]
            swaps.append((i1, j1, i2, j2))
            colors, green = refresh_colors(original_grid, solution_grid, total, green, colors)

    print(swaps)
    print(len(swaps))
