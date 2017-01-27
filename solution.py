#
# Some convenient definitions brought over from utils.py
#

rows = 'ABCDEFGHI'
cols = '123456789'

def cross(a, b):
    "Cross product of elements in A and elements in B."
    return [s+t for s in a for t in b]

boxes = cross(rows, cols)

row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
unitlist = row_units + column_units + square_units
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
    
    print("====")
    # 1. Select a unit
    for iUnit in unitlist:
###    for iUnit in row_units:
        seenPair = dict()
        print("iUnit= ", iUnit)
    # 2. Step through the boxes in a unit until a box with 2 values is found.
    # 2a. Mark this box.
        for iBox in range(len(iUnit)):
            print("iBox = ", iBox)
            iBoxID = iUnit[iBox]
            print("iBoxID = ", iBoxID)
            if len(values[iBoxID])==2:  #candidate naked twin
                try: 
                    if seenPair[values[iBoxID]]==1:  # pair seen before, skip
                        print("Lead seen before-skipping")
                        continue
                except:
                    print("Candidate Naked Twin Lead:")
                    seenPair[values[iBoxID]]=1  # mark for next time
                    pairVal1=values[iBoxID]
                    pairBox1=iBox
                    if iBox==len(iUnit)-1:  #can't search beyond end.
                        print("Skipping pair search.")
                        break
    # 3. Step through the remainder of the boxes and mark those boxes
    # where a duplicate of the first pair is found.  If there is more
    # than one box, then exit
                    pairFlag=False  #to prevent more than one duplicate.
                    multiFlag=False
                    for jBox in range(iBox+1,len(iUnit)):              
                        print("jBox = ", jBox)
                        jBoxID = iUnit[jBox]
                        print("jBoxID = ", jBoxID)
                        if len(values[jBoxID])==2:  #candidate naked twin
                            print("Candidate Naked Twin Pair:")
                            if pairVal1==values[jBoxID] and pairFlag==False:
                                print("match found at: ", jBoxID)
                                pairBox2=jBox
                                pairFlag=True
                            elif pairVal1==values[jBoxID] and pairFlag==True:
                                print("more than two matching pairs - breaking out.")
                                multiFlag=True
                                break  # more than two pairs.
                    
    # 4.  Eliminate the naked pairs from the peers of the first box and
    # second box, one digit at a time.
    
                    print()
                    if pairFlag==True and multiFlag==False:  #One and only one twin to lead.
                        twin1 = iUnit[pairBox1]
                        twin2 = iUnit[pairBox2]
                        elimPair = values[twin1]
                        print("Eliminating peers of ", twin1, twin2, elimPair)
                        
    # Process first twin                    
                        for iPeer in peers[twin1]:
                            print("iPeer twin1 = ", iPeer)
                            if iPeer==twin2:  # don't remove other twin
                                continue
    # Remove first digit                        
                            if elimPair[0] in values[iPeer]:
                                tmpVal = values[iPeer]
                                newVal = tmpVal.replace(elimPair[0],"")
                                values[iPeer]=newVal
    # Remove second digit                                  
                            if elimPair[1] in values[iPeer]:
                                tmpVal = values[iPeer]
                                newVal = tmpVal.replace(elimPair[1],"")
                                values[iPeer]=newVal
                                      
    # Process second twin                           
                        for iPeer in peers[twin2]:
                            print("iPeer twin2 = ", iPeer)
                            if iPeer==twin1:  # don't remove other twin
                                continue
    # Remove first digit                        
                            if elimPair[0] in values[iPeer]:
                                tmpVal = values[iPeer]
                                newVal = tmpVal.replace(elimPair[0],"")
                                values[iPeer]=newVal
                                      
    # Remove second digit                                  
                            if elimPair[1] in values[iPeer]:
                                tmpVal = values[iPeer]
                                newVal = tmpVal.replace(elimPair[1],"")
                                values[iPeer]=newVal
    
    # 5. Continue stepping through the boxes, ignoring any box that
    # was part of a nakedtwins.
    
###                        break #only do one pair per unit
    
    # 6. Move to next unit and repeat steps 1-5.
    #
    return values
   

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

def eliminate(values):
    pass

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
    return grid_values(grid)


if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    values = grid_values(diag_sudoku_grid)
    
    values['A2']='23'
#    values['A3']='35'
#    values['A5']='23'
#    values['A6']='46'
#    values['A8']='35'
#    values['A9']='46'
    
##    display(solve(diag_sudoku_grid))
    print("Before Naked Twins:")
    display(values)
    ntv = naked_twins(values)
    print("After Naked Twins:")
    display(ntv)

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
