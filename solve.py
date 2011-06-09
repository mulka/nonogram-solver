#!/usr/bin/env python
import sys
import string
import copy
import types

def get_permutations(counts, length):
    """
    >>> get_permutations([], 1)
    [[False]]
    
    >>> get_permutations([1], 1)
    [[True]]
    
    >>> get_permutations([2], 3)
    [[True, True, False], [False, True, True]]
    
    >>> get_permutations([2], 4)
    [[True, True, False, False], [False, True, True, False], [False, False, True, True]]
    
    >>> get_permutations([1, 1], 4)
    [[True, False, True, False], [True, False, False, True], [False, True, False, True]]

    >>> get_permutations([1, 2], 5)
    [[True, False, True, True, False], [True, False, False, True, True], [False, True, False, True, True]]

    >>> get_permutations([1, 1, 2], 7)
    [[True, False, True, False, True, True, False], [True, False, True, False, False, True, True], [True, False, False, True, False, True, True], [False, True, False, True, False, True, True]]
    """
    if len(counts) == 0:
        row = []
        for x in xrange(length):
            row.append(False)
        return [row]

    permutations = []
    
    for start in xrange(length - counts[0] + 1):
        permutation = []
        for x in xrange(start):
            permutation.append(False)
        for x in xrange(start, start + counts[0]):
            permutation.append(True)
        x = start + counts[0]
        if x < length:
            permutation.append(False)
            x += 1
        if x == length and len(counts) == 0:
            permutations.append(permutation)
            break
        sub_start = x
        sub_rows = get_permutations(counts[1:len(counts)], length - sub_start)
        for sub_row in sub_rows:
            sub_permutation = copy.deepcopy(permutation)
            for x in xrange(sub_start, length):
                sub_permutation.append(sub_row[x-sub_start])
            permutations.append(sub_permutation)
    return permutations

def solve_row(counts, row):
    """
    >>> solve_row([], [None])
    [False]
    
    >>> solve_row([1], [None])
    [True]
    
    >>> solve_row([2], [False, None, None])
    [False, True, True]

    >>> solve_row([2], [True, None, None])
    [True, True, False]

    >>> solve_row([2], [None, None, None])
    [None, True, None]
    
    >>> solve_row([2], [None, False, None, None])
    [False, False, True, True]

    >>> solve_row([2], [None, False, None, None, None, None])
    [False, False, None, None, None, None]
        
    row already completed:
    >>> solve_row([1], [None, True, None])
    [False, True, False]

    too far away to be able to complete
    >>> solve_row([2], [None, True, None, None])
    [None, True, None, False]
    
    assume positions of all except one count
    >>> solve_row([1, 2], [None, None, None, None, None])
    [None, None, None, True, None]

    >>> solve_row([1, 1, 1, 2], [None, None, None, None, None, None, None, None, None])
    [None, None, None, None, None, None, None, True, None]
    
    >>> solve_row([1, 7], [None, False, True, None, None, None, None, None, None, None])
    [True, False, True, True, True, True, True, True, True, False]
    
    doesn't fit on one size of False
    >>> solve_row([1, 1], [None, False, None, None])
    [True, False, None, None]

    doesn't fit on one size of False
    >>> solve_row([1, 2], [None, None, False, None, None, None])
    [None, None, False, None, True, None]
    
    already started on one side of False
    >>> solve_row([4], [None, None, None, None, False, None, True, None, None, None])
    [False, False, False, False, False, None, True, True, True, None]
    """
    permutations = get_permutations(counts, len(row))
    valid_permutations = []
    for permutation in permutations:
        valid = True
        for x in xrange(len(row)):
            if row[x] != None and row[x] != permutation[x]:
                valid = False
        if valid:
            valid_permutations.append(permutation)

    new_row = copy.deepcopy(valid_permutations[0])
    for permutation in valid_permutations:
        for x in xrange(len(row)):
            if new_row[x] != permutation[x]:
                new_row[x] = None
        
    return new_row

def solve(row_counts, col_counts, grid):
    width = len(grid[0])
    height = len(grid)
    
    changed = True
    while changed:
        changed = False
        for x in xrange(width):
            col = []
            for y in xrange(height):
                col.append(grid[y][x])
            col = solve_row(col_counts[x], col)
            for y in xrange(height):
                if col[y] != None and grid[y][x] != col[y]:
                    changed = True
                grid[y][x] = col[y]
                
        for y in xrange(height):
            row = copy.deepcopy(grid[y])
            row = solve_row(row_counts[y], row)
            for x in xrange(1):
                if row[x] != None and grid[y][x] != row[x]:
                    changed = True
            grid[y] = row
        
    return grid


def solve_from_file(filename):
    f = open(filename)

    lines = f.readlines()

    #convert into a list of lists and remove whitespace
    grid = []
    width = 0
    for line in lines:
        line = line.rstrip()
        if line:
            row = string.split(line, "\t")
            width = max(width, len(row))
            grid.append(row)
    height = len(grid)
    
    #convert into integers and normalize row width
    y = 0
    for row in grid:
        new_row = []
        for x in xrange(width):
            try:
                i = int(row[x])
            except IndexError:
                i = None
            except ValueError:
                if row[x] == 'T':
                    i = True
                elif row[x] == 'F':
                    i = False
                else:
                    i = None            
            new_row.append(i)
        grid[y] = new_row
        y += 1

    #measure height and width of inner grid
    x = width - 1
    y = height - 1
    while x >= 0:
        if type(grid[y][x]) == types.IntType:
            break
        x -= 1
    inner_width = width - x - 1

    x = width - 1
    y = height - 1
    while y >= 0:
        if type(grid[y][x]) == types.IntType:
            break
        y -= 1
    inner_height = len(grid) - y - 1

    print "board size: %dx%d" % (inner_width, inner_height)

    #ensure inner grid is valid
    for x in xrange(width - inner_width, width):
        for y in xrange(height - inner_height, height):
            if type(grid[y][x]) != types.NoneType and type(grid[y][x]) != types.BooleanType:
                print 'invalid board'
                exit()
                
    #ensure upper left is empty
    for x in xrange(width - inner_width):
        for y in xrange(height - inner_height):
            if grid[y][x] != None:
                print 'invalid board'
                exit()

    counts_width = width - inner_width
    counts_height = height - inner_height

    #populate row counts
    row_counts = []
    for y in xrange(counts_height, height):
        counts = []
        for x in xrange(counts_width):
            count = grid[y][x]
            if count:
                counts.append(count)
        row_counts.append(counts)

    #populate column counts
    col_counts = []
    for x in xrange(counts_width, width):
        counts = []
        for y in xrange(counts_height):
            count = grid[y][x]
            if count:
                counts.append(count)
        col_counts.append(counts)

    #redo grid
    width = inner_width
    height = inner_height
    inner_grid = []
    for y in xrange(height):
        inner_grid.append([])
        for x in xrange(width):
            inner_grid[y].append(grid[y+counts_height][x+counts_width])

    grid = solve(row_counts, col_counts, inner_grid)

    for y in xrange(counts_height):
        for x in xrange(counts_width):
            sys.stdout.write("\t")
        for counts in col_counts:
            try:
                sys.stdout.write(str(counts[-counts_height+y]))
            except:
                pass
            sys.stdout.write("\t")
        print
    y = 0
    for row in grid:
        for x in xrange(counts_width):
            try:
                sys.stdout.write(str(row_counts[y][-counts_width+x]))
            except:
                pass
            sys.stdout.write("\t")
        for square in row:
            if square == True:
                sys.stdout.write('T')
            elif square == False:
                sys.stdout.write('F')
            sys.stdout.write("\t")
        print
        y += 1
        
if __name__ == "__main__":
    if len(sys.argv) > 1:
        solve_from_file(sys.argv[1])
    else:
        import doctest
        doctest.testmod()