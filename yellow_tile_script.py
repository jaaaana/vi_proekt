yellow = 1
gray = 2


def check_yellow(i, j, current_grid, solution, total, green):
    return check_row(i, j, current_grid, solution, total, green) or check_column(i, j, current_grid, solution, total,
                                                                                 green)


def check_row(i, j, current_grid, solution, total, green):
    letter = current_grid[i][j]
    row_sol = [solution[i][k] for k in range(5) if i in (0, 2, 4)]
    # row_sol = green[i // 2].keys()
    # row_sol = green[i // 2].keys() if i in (0, 2, 4) else []
    in_row = letter in row_sol
    if in_row:
        if total[i // 2][letter] <= green[i // 2][letter]:
            return False
        row_grid = [current_grid[i][k] for k in range(5) if i in (0, 2, 4)]
        grid_count = row_grid.count(letter)
        if total[i // 2][letter] > green[i // 2][letter] and grid_count <= total[i // 2][letter]:
            return True
        else:
            if row_grid.index(letter) == j:
                return True

    return False


def check_column(i, j, current_grid, solution, total, green):
    letter = current_grid[i][j]
    col_list = [solution[k][j] for k in range(5) if j in (0, 2, 4)]
    # # col_list = green[j // 2 + 3].keys()
    # col_list = green[j // 2 + 3].keys() if j in (0, 2, 4) else []
    in_col = letter in col_list
    if in_col:
        if total[j // 2 + 3][letter] <= green[j // 2 + 3][letter]:
            return False
        col_grid = [current_grid[k][j] for k in range(5) if j in (0, 2, 4)]
        if total[j // 2 + 3][letter] > green[j // 2 + 3][letter] and col_grid.count(letter) <= total[j // 2 + 3][
                letter]:
            return True
        else:
            if col_grid.index(letter) == i:
                return True

    return False


def create_dictionaries(grid):
    total = {}
    green = {}
    for i in (0, 2, 4):
        for j in range(5):
            if i // 2 not in total:
                total[i // 2] = {}
                green[i // 2] = {}
            if grid[i][j] not in total[i // 2]:
                total[i // 2][grid[i][j]] = 0
                green[i // 2][grid[i][j]] = 0
            total[i // 2][grid[i][j]] += 1

    for j in (0, 2, 4):
        for i in range(5):
            if j // 2 + 3 not in total:
                total[j // 2 + 3] = {}
                green[j // 2 + 3] = {}
            if grid[i][j] not in total[j // 2 + 3]:
                total[j // 2 + 3][grid[i][j]] = 0
                green[j // 2 + 3][grid[i][j]] = 0
            total[j // 2 + 3][grid[i][j]] += 1

    return total, green


def refresh_colors(new_grid, solution_grid, total, correct, current_colors):
    new_colors = [[0 for _ in range(5)] for _ in range(5)]
    new_correct = correct
    for i in range(5):
        for j in range(5):
            if solution_grid[i][j] == new_grid[i][j] and current_colors[i][j] != 0:
                if i in (0, 2, 4):
                    new_correct[i // 2][new_grid[i][j]] += 1
                if j in (0, 2, 4):
                    new_correct[j // 2 + 3][new_grid[i][j]] += 1

    for i in range(5):
        for j in range(5):
            if solution_grid[i][j] == new_grid[i][j]:
                new_colors[i][j] = 0
            elif check_yellow(i, j, new_grid, solution_grid, total, new_correct):
                new_colors[i][j] = yellow
            else:
                new_colors[i][j] = gray
    return new_colors, new_correct


def initial_colors(grid, solution, total, correct):
    colors = [[0 for _ in range(5)] for _ in range(5)]

    for i in range(5):
        for j in range(5):
            if solution[i][j] == grid[i][j]:
                if i in (0, 2, 4):
                    correct[i // 2][grid[i][j]] += 1
                if j in (0, 2, 4):
                    correct[j // 2 + 3][grid[i][j]] += 1

    for i in range(5):
        for j in range(5):
            if solution[i][j] == grid[i][j]:
                continue
            elif check_yellow(i, j, grid, solution, total, correct):
                colors[i][j] = yellow
            else:
                colors[i][j] = gray

    return colors, correct
