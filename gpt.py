def read_grid(string):
    grid = []
    for i in range(5):
        grid.append(list(string[i * 5:i * 5 + 5]))
    return grid

def refresh_colors(grid, solution):
    """
    Updates the colors of the grid based on the current grid state and the solution grid.
    Returns the updated colors matrix and the counts of correctly placed letters.
    """
    colors = [[0 for _ in range(5)] for _ in range(5)]
    correct_positions = [[False for _ in range(5)] for _ in range(5)]
    yellow_counts = {}

    for i in range(5):
        for j in range(5):
            if grid[i][j] == solution[i][j]:
                colors[i][j] = "green"
                correct_positions[i][j] = True
            elif grid[i][j] in (row[j] for row in solution):
                colors[i][j] = "yellow"
                yellow_counts[grid[i][j]] = yellow_counts.get(grid[i][j], 0) + 1
            else:
                colors[i][j] = "gray"

    return colors, correct_positions, yellow_counts


def find_optimal_swaps(grid, solution, correct_positions):
    """
    Finds all optimal swaps, where both swapped letters end up in the correct position.
    """
    swaps = []
    for i1 in range(5):
        for j1 in range(5):
            if correct_positions[i1][j1]:
                continue
            for i2 in range(5):
                for j2 in range(5):
                    if (i1, j1) == (i2, j2) or correct_positions[i2][j2]:
                        continue
                    # Check if swapping makes both letters correct
                    if (
                            grid[i1][j1] == solution[i2][j2]
                            and grid[i2][j2] == solution[i1][j1]
                    ):
                        swaps.append((i1, j1, i2, j2))
    return swaps


def find_yellow_swap(grid, solution, colors, yellow_counts):
    """
    Finds the first swap where one letter ends up in the correct position
    and the other becomes yellow.
    """
    for i1 in range(5):
        for j1 in range(5):
            if colors[i1][j1] == "green":
                continue
            for i2 in range(5):
                for j2 in range(5):
                    if (i1, j1) == (i2, j2):
                        continue
                    # Check if the swap results in a green and yellow
                    if (
                            grid[i1][j1] == solution[i2][j2]
                            and grid[i2][j2] in (row[j2] for row in solution)
                            and yellow_counts.get(grid[i2][j2], 0) > 0
                    ):
                        return i1, j1, i2, j2
    return None


def find_any_swap(grid, solution, colors):
    """
    Finds any swap where the first letter ends up in the correct position.
    """
    for i1 in range(5):
        for j1 in range(5):
            if colors[i1][j1] == "green":
                continue
            for i2 in range(5):
                for j2 in range(5):
                    if (i1, j1) == (i2, j2):
                        continue
                    # Check if swapping makes the first letter correct
                    if grid[i1][j1] == solution[i2][j2]:
                        return i1, j1, i2, j2
    return None


def solve_waffle(grid, solution):
    colors, correct_positions, yellow_counts = refresh_colors(grid, solution)
    swaps = []

    while not all(all(row) for row in correct_positions):
        optimal_swaps = find_optimal_swaps(grid, solution, correct_positions)
        for swap in optimal_swaps:
            i1, j1, i2, j2 = swap
            grid[i1][j1], grid[i2][j2] = grid[i2][j2], grid[i1][j1]
            swaps.append(swap)
            colors, correct_positions, yellow_counts = refresh_colors(grid, solution)

        yellow_swap = find_yellow_swap(grid, solution, colors, yellow_counts)
        if yellow_swap:
            i1, j1, i2, j2 = yellow_swap
            grid[i1][j1], grid[i2][j2] = grid[i2][j2], grid[i1][j1]
            swaps.append((i1, j1, i2, j2))
            colors, correct_positions, yellow_counts = refresh_colors(grid, solution)
            continue

        any_swap = find_any_swap(grid, solution, colors)
        if any_swap:
            i1, j1, i2, j2 = any_swap
            grid[i1][j1], grid[i2][j2] = grid[i2][j2], grid[i1][j1]
            swaps.append((i1, j1, i2, j2))
            colors, correct_positions, yellow_counts = refresh_colors(grid, solution)

    return swaps


if __name__ == '__main__':
    g_s = 'FBOUEG I ULSOOMG E LOEMNA'
    s_s = 'FUGUEO L NLOOSEI B MOMEGA'
    grid = read_grid(g_s)
    solution = read_grid(s_s)
    print(solve_waffle(grid, solution))
