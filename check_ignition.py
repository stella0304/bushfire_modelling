def check_surrounding(cell, b_grid, h_grid, i, j):
    """takes in a pair of coordinates and return the corresponding contribution
    of that coordinate to the burn_factor in check_ignition"""
    # print(cell)
    row = cell[0]
    column = cell[1]
    if b_grid[row][column] is True:
        if h_grid[row][column] == h_grid[i][j]:
            return 1
        elif h_grid[row][column] < h_grid[i][j]:
            return 2
        elif h_grid[row][column] > h_grid[i][j]:
            return 0.5

def check_ignition(b_grid, f_grid, h_grid, i_threshold, w_direction, i, j):
    """takes in a list of lists of bool, fuel load and height, an ignition
    threshold, a wind direction and a pair of coordinates and determine whether
    the coordinate will burn at t + 1"""
    
    # check if the coordinates given can burn and that it's not burning in the 
    # beginning
    if f_grid[i][j] == 0 or b_grid[i][j] is True:
        return False
    
    # a burn factor to be added to and compared to i_threshold
    burn_factor = 0
    
    surrounding = [[i - 1, j - 1], [i - 1, j], [i - 1, j + 1], [i, j - 1], 
                   [i, j + 1], [i + 1, j - 1], [i + 1, j], [i + 1, j + 1]]
    
    # add to the burn factor with consideration of height
    for cell in surrounding:
        if 0 <= cell[0] <= len(b_grid) - 1 and 0 <= cell[1] <= len(b_grid) - 1:
            contribution = check_surrounding(cell, b_grid, h_grid, i, j)
            if contribution:
                burn_factor += contribution
    
    dir_dict = {'N': [[i - 2, j - 1], [i - 2, j], [i - 2, j + 1]], 
                'NE': [[i - 2, j + 1], [i - 2, j + 2], [i - 1, j + 2]], 
                'E': [[i - 1, j + 2], [i, j + 2], [i + 1, j + 2]],
                'SE': [[i + 2, j], [i + 2, j + 2], [i + 1, j + 2]],
                'S': [[i + 2, j - 1], [i + 2, j], [i + 2, j + 1]],
                'SW': [[i + 2, j - 1], [i - 2, j + 2], [i + 1, j - 2]],
                'W': [[i - 1, j - 2], [i, j - 2], [i + 1, j - 2]],
                'NW': [[i + 2, j + 1], [i - 2, j + 2], [i + 1, j + 2]]}
    
    # add to burn_factor with consideration of wind
    if w_direction:
        for cells in dir_dict[w_direction]:
            if (0 <= cells[0] <= len(b_grid) - 1 and 
                0 <= cells[1] <= len(b_grid) - 1):
                contribution = check_surrounding(cells, b_grid, h_grid, i, j)
            if contribution:
                burn_factor += contribution
    
    if burn_factor >= i_threshold:
        return True
    else:
        return False
    
