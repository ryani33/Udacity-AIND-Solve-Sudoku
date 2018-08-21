
from utils import *


row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
diagonal_units = [
    ['A1', 'B2', 'C3', 'D4', 'E5', 'F6', 'G7', 'H8', 'I9'],
    ['A9', 'B8', 'C7', 'D6', 'E5', 'F4', 'G3', 'H2', 'I1']
]
unitlist = row_units + column_units + square_units + diagonal_units

# Must be called after all units (including diagonals) are added to the unitlist
units = extract_units(unitlist, boxes)
peers = extract_peers(units, boxes)

def naked_twins(map_values):
    for box in map_values:
        if len(map_values[box]) == 2:
            for unit in units[box]:
                twins = [box_in_unit for box_in_unit in unit if map_values[box_in_unit] == map_values[box]]
                if len(twins) == 2:
                    for other_box in unit:
                        if other_box in twins:
                            continue
                        map_values[other_box] = map_values[other_box].replace(map_values[box][0], "").replace(map_values[box][1], "")
    return map_values


def eliminate(map_values):
    solved_values = [box for box in map_values if len(map_values[box]) == 1]
    for single in solved_values:
        for box in peers[single]:
            map_values[box] = map_values[box].replace(map_values[single], "")
    return map_values


def only_choice(map_values):
    for unit in unitlist:
        digits = "123456789"
        for digit in digits:
            dplace = [box for box in unit if digit in map_values[box]]
            if len(dplace) == 1:
                map_values[dplace[0]] = digit
    return map_values


def reduce_puzzle(map_values):
    stalled = False
    while not stalled:
        solved_before = [box for box in map_values if len(map_values[box]) == 1]
        map_values = eliminate(map_values)
        map_values = naked_twins(map_values)
        map_values = only_choice(map_values)
        solved_after = [box for box in map_values if len(map_values[box]) == 1]
        stalled = len(solved_before) == len(solved_after)
        if len([box for box in map_values if len(map_values[box]) == 0]):
            return False
    return map_values


def search(map_values):
    map_values = reduce_puzzle(map_values)
    if map_values is False:
        return False
    if all(len(map_values[box]) == 1 for box in map_values):
        return map_values
    n, s = min((len(map_values[box]), box) for box in map_values if len(map_values[box]) > 1)
    for temp in map_values[s]:
        new_map = map_values.copy()
        new_map[s] = temp
        attempt = search(new_map)
        if attempt:
            return attempt
    

def solve(grid):
    values = grid2values(grid)
    values = search(values)
    return values


if __name__ == "__main__":
    #diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    diag_sudoku_grid = '9.1....8.8.5.7..4.2.4....6...7......5..............83.3..6......9................'
    display(grid2values(diag_sudoku_grid))
    result = solve(diag_sudoku_grid)
    display(result)

    try:
        import PySudoku
        PySudoku.play(grid2values(diag_sudoku_grid), result, history)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
