#
# Some convenient definitions brought over from utils.py
#

rows = 'ABCDEFGHI'
cols = '123456789'

def cross(a, b):
    "Cross product of elements in A and elements in B."
    return [s+t for s in a for t in b]

boxes = cross(rows, cols)

# Added diagonal units for project requirements and added to unitlist
leftdiag=[['A1','B2','C3','D4','E5','F6','G7','H8','I9']]
rightdiag=[['A9','B8','C7','D6','E5','F4','G3','H2','I1']]

row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
unitlist = row_units + column_units + square_units + leftdiag + rightdiag
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)

#
# End of definitions from utils.py
#

assignments = []

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

    # Algorithm
    # 1. Select a unit
    # 2. Step through the boxes until a box with 2 values is found.
    # 2a. Mark this box.
    # 3. Step through the remainder of the boxes and mark those boxes
    # where a duplicate of the first pair is found.  If there is more
    # than one box, then exit
    # 4. Eliminate the naked pairs from the peers of the first box and
    # second box, one digit at a time.
    # 5. Continue stepping through the boxes, ignoring any box that
    # was part of a nakedtwins.
    # 6. Move to next unit and repeat steps 1-5.
    #
    
###    print("====")
###    print("naked twins before processing")
###    display(values)
    new_values = values.copy()
    # 1. Select a unit
    for iUnit in unitlist:
###    for iUnit in row_units:
        seenPair = dict()
###        print("iUnit= ", iUnit)
    # 2. Step through the boxes in a unit until a box with 2 values is found.
    # 2a. Mark this box.
        for iBox in range(len(iUnit)):
###            print("iBox = ", iBox)
            iBoxID = iUnit[iBox]
###            print("iBoxID = ", iBoxID)
            if len(values[iBoxID])==2:  #candidate naked twin
                try: 
                    if seenPair[values[iBoxID]]==1:  # pair seen before, skip
 ###                       print("Lead seen before-skipping")
                        continue
                except:
###                    print("Candidate Naked Twin Lead:")
                    seenPair[values[iBoxID]]=1  # mark for next time
                    pairVal1=values[iBoxID]
                    pairBox1=iBox
                    if iBox==len(iUnit)-1:  #can't search beyond end.
###                        print("Skipping pair search.")
                        break
    # 3. Step through the remainder of the boxes and mark those boxes
    # where a duplicate of the first pair is found.  If there is more
    # than one box, then exit
                    pairFlag=False  #to prevent more than one duplicate.
                    multiFlag=False
                    for jBox in range(iBox+1,len(iUnit)):              
###                        print("jBox = ", jBox)
                        jBoxID = iUnit[jBox]
###                        print("jBoxID = ", jBoxID)
                        if len(values[jBoxID])==2:  #candidate naked twin
###                            print("Candidate Naked Twin Pair:")
                            if pairVal1==values[jBoxID] and pairFlag==False:
###                                print("match found at: ", jBoxID)
                                pairBox2=jBox
                                pairFlag=True
                            elif pairVal1==values[jBoxID] and pairFlag==True:
###                                print("more than two matching pairs - breaking out.")
                                multiFlag=True
                                break  # more than two pairs.
                    
    # 4.  Eliminate the naked pairs from the peers of the first box and
    # second box, one digit at a time.
    
                    if pairFlag==True and multiFlag==False:  #One and only one twin to lead.
                        twin1 = iUnit[pairBox1]
                        twin2 = iUnit[pairBox2]
                        elimPair = values[twin1]
###                        print()
###                        print("iUnit = ", iUnit)
###                        print("Eliminating peers of ", twin1, twin2, elimPair)
                        
    # Process first twin                    
#                        for iPeer in peers[twin1]:
                        for iPeer in iUnit:
###                            print("iPeer twin1 = ", iPeer)
                            if iPeer==twin1:  # don't remove other twin
                                continue
                            
                            if iPeer==twin2:  # don't remove other twin
                                continue
                            
    #                        if elimPair==values[iPeer]:  #don't clobber match pair
    #                            continue
    # Remove first digit                        
###                            print("elimPair[0] = ", elimPair[0])
                            if elimPair[0] in values[iPeer]:
###                                print("eliminating Val1")
                                tmpVal = new_values[iPeer]
                                newVal = tmpVal.replace(elimPair[0],"")
                                new_values[iPeer]=newVal
    # Remove second digit             
###                            print("elimPair[1] = ", elimPair[1])                     
                            if elimPair[1] in values[iPeer]:
###                                print("eliminating Val2")
                                tmpVal = new_values[iPeer]
                                newVal = tmpVal.replace(elimPair[1],"")
                                new_values[iPeer]=newVal
                                      
    
    # 5. Continue stepping through the boxes, ignoring any box that
    # was part of a nakedtwins.
    
                        break #only do one pair per unit
    
    # 6. Move to next unit and repeat steps 1-5.
    #
    
###    print()
###    print("naked twins after processing")
###    display(new_values)
    
    return new_values
   

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
    iChar=0
    grid_dict = dict()
    for iBox in boxes:
        if grid[iChar]==".":
            grid_dict[iBox]="123456789"
        else:
            grid_dict[iBox]=grid[iChar]
        iChar=iChar+1
        
    return grid_dict

def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    width = 1+max(len(values[s]) for s in boxes)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    return

    # Imported from utils.py in part 10 of Sudoku lesson.
def eliminate(values):
    """
    Go through all the boxes, and whenever there is a box with a value, eliminate this value from the values of all its peers.
    Input: A sudoku in dictionary form.
    Output: The resulting sudoku in dictionary form.
    """
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    for box in solved_values:
        digit = values[box]
        for peer in peers[box]:
            values[peer] = values[peer].replace(digit,'')
    return values

def only_choice(values):
    """
    Go through all the units, and whenever there is a unit with a value that only fits in one box, assign the value to this box.
    Input: A sudoku in dictionary form.
    Output: The resulting sudoku in dictionary form.
    """
    for unit in unitlist:
        for digit in '123456789':
            dplaces = [box for box in unit if digit in values[box]]
            if len(dplaces) == 1:
                values[dplaces[0]] = digit
    return values

def reduce_puzzle(values):
    """
    Iterate eliminate() and only_choice(). If at some point, there is a box with no available values, return False.
    If the sudoku is solved, return the sudoku.
    If after an iteration of both functions, the sudoku remains the same, return the sudoku.
    Input: A sudoku in dictionary form.
    Output: The resulting sudoku in dictionary form.
    """
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    stalled = False
    while not stalled:
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])
        values = eliminate(values)
        values = only_choice(values)
    # Added naked_twins call to the constraint propagation sequence.    
    #    values = naked_twins(values)
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        stalled = solved_values_before == solved_values_after
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values

    # End of import from utils.py in part 10 of Sudoku lesson.

# Used the search code I wrote in the lesson.    
def search(values):
    "Using depth-first search and propagation, create a search tree and solve the sudoku."
    
    # First, reduce the puzzle using the previous function
    new_values = reduce_puzzle(values.copy())
    if new_values == False:   # error base case
        return new_values
        
    #otherwise, maybe need to recurse
    
    # Chose one of the unfilled square s with the fewest possibilities
    # choose squares with >1 value.
    returnVal=True
    for k,v in new_values.items():
        if len(v) > 1:
            curVals=v
            returnVal=False
            break
    
    if returnVal==True:  #Puzzle solved base case
        return new_values
    
    # Now use recursion to solve each one of the resulting sudokus, 
    # and if one returns a value (not False), return that answer!
    # Start with left most path and go in order
    
    for iDigit in curVals:
        new_values[k]=iDigit
        new_values2 = search(new_values.copy())
        if new_values2!=False: #either found a solution, or need to check another path.
            solved_values_count = len([box for box in new_values2.keys() if len(new_values2[box]) == 1])
            if solved_values_count==81:
                return new_values2 # done
            else:
                continue
        else:
            continue
    
    return new_values  # need to go up one level in tree.

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
    new_values = search(values)
    
    return new_values


if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
###    values = grid_values(diag_sudoku_grid)
    
#    values['A2']='23'
#    values['B3']='23'
#    values['A5']='23'
#    values['A6']='46'
#    values['A8']='35'
#    values['A9']='46'
    
    display(solve(diag_sudoku_grid))
###   print("Before Naked Twins:")
###    display(values)
###    ntv = naked_twins(values)
###    print()
###    print("After Naked Twins:")
###    display(ntv)

###    leftdiag=[['A1','B2','C3','D4','E5','F6','G7','H8','I9']]
###    rightdiag=[['A9','B8','C7','D6','E5','F4','G3','H2','I1']]

###    unitlist_d = row_units + column_units + square_units + leftdiag + rightdiag
###    units_d = dict((s, [u for u in unitlist_d if s in u]) for s in boxes)
###    peers_d = dict((s, set(sum(units_d[s],[]))-set([s])) for s in boxes)


    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
