WIND_DIR = ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW', 'None']

def convert_to_list(iteration_range):
    """Takes a list of rows in strings and returns them in the format of a list 
    of lists if the rows and columns are of the supposed length or None if 
    not."""
    
    converted_list = []
    for row in iteration_range:
        row_list = []
        for item in row.split(','):
            row_list.append(int(item))
        converted_list.append(row_list)
    return converted_list

def parse_scenario(filename):
    # TODO implement this function
    
    """Takes a file with specific structure and returns dictionary with all 
    values in the file or None if any of the values are invalid."""
    
    # make a list of all the lines in the file
    scenario = open(filename)
    scenario_list = []
    for line in scenario.readlines():
        scenario_list.append(line[:-1])
    scenario.close()
    
    # check if dimentions is positive integer
    if not scenario_list[0].isdigit() or int(scenario_list[0]) < 0:
        return None
    dimentions = int(scenario_list[0])
    
    # create a dictionary for each part of the file to be returned
    scenario_dict = {}
    
    # add the fuel load & height to dict
    scenario_dict['f_grid'] = convert_to_list(scenario_list[1: 1 + dimentions])
    scenario_dict['h_grid'] = convert_to_list(scenario_list
                                          [1 + dimentions: 1 + 2 * dimentions])
    
    
    # check if ignition threshold is valid, if so, add to dict
    if not scenario_list[1 + 2 * dimentions].isdigit() or \
            not 0 < int(scenario_list[1 + 2 * dimentions]) < 8:
        return None
    scenario_dict['i_threshold'] = int(scenario_list[1 + 2 * dimentions])
    
    # check if wind direction is valid and if so, add to dict
    if scenario_list[2 + 2 * dimentions] not in WIND_DIR:
        return None
    scenario_dict['w_direction'] = scenario_list[2 + 2 * dimentions]
    
    # add cell burning at the start to dict
    burning_cells = []
    for indecies in scenario_list[3 + 2 * dimentions:]:
        cell_list = []
        for item in indecies.split(','):
            
            # check if burning cells are located in the landscape, thus valid
            if not 0 <= int(item) <= dimentions - 1:
                return None
            cell_list.append(int(item))
            
        # check if ignition threshold is a non zero, if so add to dict
        if scenario_dict['f_grid'][cell_list[0]][cell_list[1]] == 0:
            return None
        burning_cells.append(tuple(cell_list))
    scenario_dict['burn_seeds'] = burning_cells
    
    
    return scenario_dict
