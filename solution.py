#-------------------------------------------------------------------------------------------#
#  @Author       : Bhavin Patel                                                             #
#  @Date         : 2017-02-23                                                               #
#  @Term         : AI - Feb                                                                 #
#  @Project Name : AIND-Sudoku                                                              #
#-------------------------------------------------------------------------------------------#

from pprint import  pprint
import  sys
import itertools
import operator


assignments = []

digits = '123456789'
alphas = 'ABCDEFGHI'

cols             = {}
rows             = {}
boxes            = {}
diagonals        = {}
cell_constraints = {}


#-----------------------------------#
#       Initializing Constraints    #
#-----------------------------------#
def get_box_constraints():
    _boxes = [ list(map(''.join , itertools.product(A,B))) \
               for A,B in list(itertools.product(['ABC','DEF','GHI'],['123','456','789'])) ]
    for item in [{cell:box} for box in _boxes for cell in box ]:
        for k, v in item.items():
            if k not in boxes: boxes[k] = v.copy()
            else: boxes[k] += v.copy()
            if k in boxes[k]: boxes[k].remove(k)

    return boxes


#-----------------------------#
#   get_diagonal_constraints  #
#-----------------------------#
def get_diagonal_constraints():
    diagonals_l = ["{}{}".format(x,y) for x, y in (zip(alphas, digits))]
    diagonals_r = ["{}{}".format(x,y) for x, y in zip(reversed([a for a in alphas]), [d for d in digits]) ]
    _diagonals = [ {cell:diagonals_l} for cell in diagonals_l ] +  [ {cell:diagonals_r} for cell in diagonals_r ]

    for item in _diagonals:
        for k, v in item.items():
            if k not in diagonals: diagonals[k] = v.copy()
            else: diagonals[k] += v.copy()
            if k in diagonals[k] : diagonals[k].remove(k)

    # make unique values
    for item in _diagonals:
        for k, v in item.items():
            diagonals[k] = sorted( list(set(diagonals[k])) )

    return diagonals


#--------------------------------#
#   get_row_and_col_constraints  #
#--------------------------------#
def get_row_and_col_constraints():
    board  = cross(alphas,digits)
    for cell in board:
        cols[cell] = [ "{}{}".format(cell[0], i) for i in digits if cell != "{}{}".format(cell[0],i)]
        rows[cell] = [ "{}{}".format(a, cell[1]) for a in alphas if cell != "{}{}".format(a, cell[1])]


#-----------------------------#
#   combine_all_constraints   #
#-----------------------------#
def combine_all_constraints():
    for constraint_dicts in [ cols, rows, boxes, diagonals]:
        for cell in constraint_dicts:
            if cell not in cell_constraints: cell_constraints[cell] = constraint_dicts[cell].copy()
            else : cell_constraints[cell] += constraint_dicts[cell].copy()

    for cell in cross(alphas,digits):
        cell_constraints[cell] = list(set(cell_constraints[cell]))


#---------------------------#
#   initialize_constraints  #
#---------------------------#
def initialize_constraints():
    if not bool(boxes):                     get_box_constraints()
    if not bool(diagonals):                 get_diagonal_constraints()
    if not bool(rows) or not bool(cols) :   get_row_and_col_constraints()
    if not bool(cell_constraints):          combine_all_constraints()


#-------------------#
#   sort_values()   #
#-------------------#
def sort_values(values):
    return dict(sorted( values.items() , key=operator.itemgetter(0)))


#-------------------#
#   assign_value    #
#-------------------#
def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """
    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values


#--------------#
#   cross      #
#--------------#
def cross(A, B):
    "Cross product of elements in A and elements in B."
    return [ "{}{}".format(x,y) for x,y in itertools.product(A,B) ]
    pass


#--------------------#
#   grid_values      #
#--------------------#
def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Args:
        grid(string) - A grid in string form.
    Returns:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """
    board  = cross(alphas,digits)
    values = dict(zip(board, grid))
    for k,v in values.items():
        if v == '.' : values[k] = digits
        assign_value( values.copy(), k, values[k])
    return values


#-------------------#
#   display         #
#-------------------#
def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    if not values: return

    print()
    for r in ' ' + alphas:
        row_str = []
        row_str.append(r)
        for d in digits:
            if r == ' ': row_str.append("| {:^9}".format(d))
            else:
                cell = "{}{}".format(r,d)
                if cell in values:
                    row_str.append("| {:^9}".format(values[cell]) )
                else:
                    row_str.append("| {:^9}".format('*'))
        line = ' '.join(row_str)
        print( line )
        print( "".join([ '-' for i in range(0, len(line))]))

    print()


#-------------------------------------#
#   get_number_of_solved_boxes        #
#-------------------------------------#
def get_number_of_solved_boxes(values):
    return len([box for box in values.keys() if len(values[box]) == 1])


#-------------------#
#   is_solved       #
#-------------------#
def is_solved(values):
    return all([ len(v) == 1 for k,v in values.items()])


#.......................................#
#           Naked Twins Helpers         #
#.......................................#

#-----------------------#
#   find_naked_twins    #
#-----------------------#
def find_naked_twins(values, search_value, search_array):
    """
        search for the 'seach_value' in the given constraint 'search_array'

    :param values:
    :param search_value:
    :param search_array:
    :return: ntwin_value if valued found in the constraint array or None

    """
    ntwin_value = None

    # only search for values whose length is 2 , by def. of naked twins.
    if len(search_value) != 2 : return None

    for item in search_array:
        if search_value == values[item]: ntwin_value = search_value
    return  ntwin_value


#---------------------------#
#   eliminate_naked_twins   #
#---------------------------#
def eliminate_naked_twins(values, ntwin_value, constraint_array):
    """
        eliminate all the digits from naked twins vales if present in any cell of the given constraint array

    :param values:
    :param ntwin_value:
    :param constraint_array:
    :return:values either updated values dict or original values dict
    """
    if ntwin_value is None: return values

    for item in constraint_array:
        if values[item] != ntwin_value:

            # find and eliminate all the digits present in the naked twins
            for locked_digits in ntwin_value:
                values[item] = values[item].replace(locked_digits, '')
                assign_value(values,item, values[item])
    return values


#--------------------#
#   naked_twins      #
#--------------------#
def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.

    Note:
        instead of using cell_constraint which houses all the possible constraints for a give cell,  I have used them
        individually to avoid cases possibility of matching the values across different constraints.

    """

    initialize_constraints()
    for cell, value in values.items():
        if cell in cols:
            values = eliminate_naked_twins(values, find_naked_twins(values, value, cols[cell]), cols[cell])
        if cell in rows:
            values = eliminate_naked_twins(values, find_naked_twins(values, value, rows[cell]), rows[cell])
        if cell in boxes:
            values = eliminate_naked_twins(values, find_naked_twins(values, value, boxes[cell]), boxes[cell])
        if cell in diagonals:
            values = eliminate_naked_twins(values, find_naked_twins(values, value, diagonals[cell]), diagonals[cell])

    return values


#------------------------#
#   reduce_puzzle        #
#------------------------#
def reduce_puzzle(values):
    stalled = False
    while not stalled:
        solved_before = get_number_of_solved_boxes(values)

        values = eliminate( values )
        values = only_choice(values)
        values = naked_twins(values)

        solved_after = get_number_of_solved_boxes(values)

        stalled = solved_before == solved_after

    return values



#--------------------#
#   eliminate        #
#--------------------#
def eliminate(values):
    initialize_constraints
    for key,val in values.items():
        if len(val) == 1:
            for ccell in  cell_constraints[key]:
                values[ccell] = values[ccell].replace(val, '')
                assign_value(values.copy(), ccell , values[ccell])
    return values


#----------------------#
#   only_choice        #
#----------------------#
def only_choice(values):
    initialize_constraints
    for k,v in values.items():
        if len(v) == 1 : continue
        chosen = v
        for search_val in v:
            for cell in cell_constraints[k]:
                if search_val in values[cell] and len(chosen) > 1: chosen.replace(search_val, '')
            if len(chosen) == 1:
                values[k] = chosen
    return values


#-----------------#
#   search        #
#-----------------#
def search(values):
    values = reduce_puzzle(values)

    if is_solved(values): return values

    #find min elements to solve
    _min = None
    for k , v in values.items():
        if len(v) == 1 : continue
        if _min is None : _min = { 'key': k, 'val': v, 'len':len(v) }
        if len(v) < _min['len']: _min = { 'key': k, 'val': v, 'len':len(v) }

    for chosen in values[ _min['key'] ]:
        new_values = values.copy()
        new_values[ _min['key'] ] = chosen
        return_values = search(new_values)
        if return_values:
            return return_values



#--------------#
#   solve      #
#--------------#
def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    initialize_constraints()
    return search( grid_values(grid) )



#===================#
#       MAIN        #
#===================#
if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    values = solve(diag_sudoku_grid)
    display(values)

    sys.exit(0)

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)


    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
