def copy_list(original_list):
    """take a 2D list with the same height and width and make a copy"""
    list_copy = []
    for i in range(len(original_list)):
        list_copy.append([])
        for j in range(len(original_list)):
            list_copy[i].append(original_list[i][j])
    return list_copy

def test_bool(bool_list):
    """take a list of lists containing bools and return True when True is in any
    of the list"""
    new_list = []
    for lst in bool_list:
        for item in lst:
            new_list.append(item)
    if True in new_list:
        return True
    else:
        return False

def next_t(cell_list, current_burning, b_grid, current_fuel, f_grid, h_grid, 
           i_threshold, w_direction, burnt_cells):
    """Takes a list of cells and their states in the current time and predict
    its state in the next t"""
    for cell in cell_list: 
        
        # for a cell that's not yet burning
        if b_grid[cell[0]][cell[1]] is False:
            burn = check_ignition(current_burning, current_fuel, h_grid, 
                                  i_threshold, w_direction, cell[0], cell[1])
            if burn:
                burnt_cells.append(cell)
                b_grid[cell[0]][cell[1]] = True
        
        # for a cell that's already burning
        else: 
            if f_grid[cell[0]][cell[1]] > 1:
                f_grid[cell[0]][cell[1]] -= 1
            else:
                f_grid[cell[0]][cell[1]] -= 1
                b_grid[cell[0]][cell[1]] = False

def run_model(f_grid, h_grid, i_threshold, w_direction, burn_seeds):
    
    """take list of lists of fuel load and height of cells, an ignition 
    threshold, a wind direction and cells initially burning and return the 
    final fuel load of all the cells once fire has stopped and the number of 
    cells burnt"""
    
    burnt_cells = burn_seeds
    
    # a list of all the cells to iterate over
    cell_list = []
    for i in range(len(f_grid)):
        for j in range(len(f_grid)):
            cell = (i, j)
            cell_list.append(cell)
            
    # create a mutable burning grid to be refered to in check_ignition function
    b_grid = []
    for i in range(len(f_grid)):
        b_grid.append([])
        for j in range(len(f_grid)):
            b_grid[i].append(False)
    for cell in cell_list:
        if cell in burn_seeds:
            b_grid[cell[0]][cell[1]] = True
    
    
    while test_bool(b_grid) is True:
        
        # lists for how the cells are currently behaving so that next_t and 
        # check ignition can iterate through the same values for every cell in 
        # each time frame
        current_fuel = copy_list(f_grid)
        current_burning = copy_list(b_grid)
        
        # generate scenario in the next time frame
        next_t(cell_list, current_burning, b_grid, current_fuel, f_grid, 
               h_grid, i_threshold, w_direction, burnt_cells)
        
    return f_grid, len(burnt_cells)
