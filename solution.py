assignments = []

from pprint import  pprint
import  sys
import itertools

digits = '123456789'
alphas = 'ABCDEFGHI'

cols = {}
rows = {}
boxes = {}
diagonals = {}
cell_constraints = {}


def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """
    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values

def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """

    # Find all instances of naked twins
    # Eliminate the naked twins as possibilities for their peers

def cross(A, B):
    "Cross product of elements in A and elements in B."
    return [ "{}{}".format(x,y) for x,y in itertools.product(A,B) ]
    pass

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
    return values

def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    print()
    spacer = '\t'
    print(spacer.join([d for d in digits]))
    for r in alphas:
        print("")
        row_str = []
        row_str.append(r)
        for d in digits:
            row_str.append("{}".format(values["{}{}".format(r,d)]) )
        print( spacer.join(row_str))
    #print( values )
    pass

def eliminate(values):
    for key,val in values.items():
        if len(val) == 1:
            for ccell in  cell_constraints[key]:
                values[ccell] = values[ccell].replace(val, '')
    return values

def only_choice(values):
    pass

def reduce_puzzle(values):
    pass

def search(values):
    pass

def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """

    values = grid_values(grid)

    display(values)

    _boxes = [ list(map(''.join , itertools.product(A,B))) \
               for A,B in list(itertools.product(['ABC','DEF','GHI'],['123','456','789'])) ]
    boxes = { x:y for item in [{cell:box} for box in _boxes for cell in box ] for x, y in item.items() }

    _diagonals = ["{}{}".format(x,y) for x, y in (zip(alphas, digits))]
    diagonals = [ {cell:_diagonals} for cell in _diagonals ]
    _diagonals = ["{}{}".format(x,y) for x, y in zip(reversed([a for a in alphas]), [d for d in digits]) ]
    diagonals +=  [ {cell:_diagonals} for cell in _diagonals ]

    diagonals = { x:y for item in diagonals for x, y in item.items() }

    for cell in values:
        cols[cell] = [ "{}{}".format(cell[0], i) for i in digits]
        rows[cell] = [ "{}{}".format(a, cell[1]) for a in alphas]

        if cell not in cell_constraints: cell_constraints[cell] = cols[cell].copy()

        cell_constraints[cell] = cols[cell] + rows[cell] + boxes[cell]
        if cell in diagonals:
            cell_constraints[cell] += diagonals[cell]

        cell_constraints[cell] = list(set(cell_constraints[cell]))
        cell_constraints[cell].remove(cell)

    print()
    # print("---- boxes")
    # print( boxes )
    # print("---- cols")
    # print( cols )
    #
    # print("-- rows")
    # print( rows )
    #
    # print('----- diagonals')
    # print( diagonals )
    #
    print('----cell constraints')
    print( cell_constraints['A1'])

    values = eliminate( values )

    display ( values )

    return
    return values

if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(solve(diag_sudoku_grid))

    sys.exit(0)

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
