WIND_DIR = ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW', 'None']

def copy_list(original_list):
    """take a 2D list with the same height and width and make a copy"""
    list_copy = []
    for i in range(len(original_list)):
        list_copy.append([])
        for j in range(len(original_list)):
            list_copy[i].append(original_list[i][j])
    return list_copy

def plan_burn(f_grid, h_grid, i_threshold, town_cell):
    
    # create a list of cells with non-zero fuel values to be iterated over
    nonzero_fuel = []
    for i in range(len(f_grid)):
        for j in range(len(f_grid)):
            if f_grid[i][j] > 0:
                if (i, j) != town_cell:
                    nonzero_fuel.append((i, j))
    
    # create a dictionary of the number of times the cell causes town to burn 
    # from fire after prescribed burning to compare each cell
    burn_freq = {}
    for cell in nonzero_fuel:
        burn_freq[cell] = 0
        
        # check if it is a valid cell for prescribed burn
        for direction in WIND_DIR:
            f_copy = copy_list(f_grid)
            final_state = run_model(f_copy, h_grid, i_threshold * 2, direction, 
                                    [cell])[0]
            
            if final_state[town_cell[0]][town_cell[1]] == 0:
                burn_freq.pop(cell)
                break
            else:    
                # find how fires started in other cells will behave if 
                # prescribed burn occur on this cell
                for othercell in nonzero_fuel:
                    fuel_state = copy_list(final_state)   
                    after_fire = run_model(fuel_state, h_grid, i_threshold, 
                                            direction, [othercell])[0]
                    if after_fire[town_cell[0]][town_cell[1]] == 0:
                        burn_freq[cell] += 1
    
    # swap the key and value in the items so it is easier to sort and find the 
    # min burns caused by the prescribed burning of each cell
    swap_burn_freq = []
    for item in burn_freq.items():
        swapped = (item[1], item[0])
        swap_burn_freq.append(swapped)
    min_burn_freq = sorted(swap_burn_freq)[0][0]
    
    # find all the cells with the min_burn_freq and return them
    optimal_cells = []
    for item in swap_burn_freq:
        if item[0] == min_burn_freq:
            optimal_cells.append(item[1])
            
    return optimal_cells
    
