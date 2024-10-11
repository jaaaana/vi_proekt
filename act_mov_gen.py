# if __name__ == '__main__':
#     moves = []
#     actions = []
#     for i in range(5):
#         for j in range(5):
#             for k in range(5):
#                 for l in range(5):
#                     if (i, j) == (1, 1) or (k, l) == (1, 1) or (i, j) == (1, 3) or (k, l) == (1, 3) or (i, j) == (3, 1) or (k, l) == (3, 1) or (i, j) == (3, 3) or (k, l) == (3, 3):
#                         continue
#                     if (i, j) == (k, l):
#                         continue
#                     if moves.__contains__(((k, l), (i, j))):
#                         continue
#                     action = 'swap_' + str(i) + str(j) + '_' + str(k) + str(l)
#                     move = ((i, j), (k, l))
#                     actions.append(action)
#                     moves.append(move)
#     print(actions)
#     print(moves)
#     print(len(moves))

colors, grid = ((0, 0, 0, 0, 0), (0, 0, 0, 0, 0), (0, 0, 0, 0, 0), (0, 0, 0, 0, 0), (0, 0, 0, 0, 0)), (
    (0, 0, 0, 0, 0), (0, 0, 0, 0, 0), (0, 0, 0, 0, 0), (0, 0, 0, 0, 0), (0, 0, 0, 0, 0))

new_colors = []
new_grid = []

for row1, row2 in zip(colors, grid):
    new_colors.append(list(row1))
    new_grid.append(list(row2))

print(new_colors)
print(new_grid)

new_colors[2][3] = 3

for row1, row2 in zip(new_colors, new_grid):
    row1 = tuple(row1)
    row2 = tuple(row2)

print(new_colors)
print(new_grid)
