#!/usr/bin/env python
import sys
import string
import copy
import types

def solve_row(counts, row, reverse=False):
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
    
    >>> solve_row([7], [None, None, None, True, None, None, None, None, False, None])
    [None, True, True, True, True, True, True, None, False, False]

    >>> solve_row([2], [None, True, None])
    [None, True, None]
    
    >>> solve_row([2], [None, None, False])
    [True, True, False]
    
    row already completed:
    >>> solve_row([1], [None, True, None])
    [False, True, False]

    too far away to be able to complete
    >>> solve_row([2], [None, True, None, None])
    [None, True, None, False]
    
    TODO: assume positions of all except one count
    solve_row([1, 2], [None, None, None, None, None])
    [None, None, None, True, None]

    TODO: doesn't fit on one size of False
    solve_row([1, 1], [None, False, None, None])
    [True, False, None, None]

    TODO: doesn't fit on one size of False
    solve_row([1, 2], [None, None, False, None, None, None])
    [None, None, False, None, True, None]
    
    TODO: already started on one side of False
    solve_row([4], [None, None, None, None, False, None, True, None, None, None])
    [False, False, False, False, False, None, True, True, True, None]
    
    """
    #all Xs
    if len(counts) == 0:
        for x in xrange(len(row)):
            row[x] = False
        return row
    
    #entire row can be filled
    if sum(counts) + len(counts) - 1 == len(row):
        x = 0
        for count in counts:
            for i in xrange(count):
                row[x] = True
                x += 1
            if x < len(row):
                row[x] = False
                x += 1
        return row
        
    #row is already complete
    count = 0
    i = 0
    for x in xrange(len(row)):
        if row[x] == True:
            count += 1
    if sum(counts) == count:
        for x in xrange(len(row)):
            if row[x] != True:
                row[x] = False
        return row

    #first in row is False
    if row[0] == False:
        sub_row = solve_row(counts, row[1:len(row)])
        for x in xrange(1, len(row)):
            row[x] = sub_row[x-1]
        return row

    #first in row is True
    if row[0] == True:
        x = 0
        for i in xrange(counts[0]):
            row[x] = True
            x += 1
        row[x] = False
        x += 1
        sub_row = solve_row(counts[1:len(counts)], row[x:len(row)])
        for i in xrange(x, len(row)):
            row[i] = sub_row[i-x]
        return row

    #first count won't fit before first False
    x = 0
    while x < len(row) and row[x] != False:
        x += 1
    if x < counts[0]:
        for i in xrange(x):
            row[i] = False
        sub_row = solve_row(counts, row[x:len(row)])
        for i in xrange(x, len(row)):
            row[i] = sub_row[i-x]
        return row
    
    #too far away to be able to complete
    if len(counts) == 1:
        first = None
        for x in xrange(len(row)):
            if row[x] == True:
                first = x
                break
        
        if first != None:
            changed = False
            for x in xrange(counts[0] + first, len(row)):
                changed = True
                row[x] = False
            if changed:
                return row
    
    if not reverse:
        counts.reverse()
        row.reverse()
        row = solve_row(counts, row, True)
        counts.reverse()
        row.reverse()
        return row
        
    #one count and it is more than half the row
    if len(counts) == 1 and counts[0] > len(row) / 2:
        count = counts[0]
        for x in xrange(len(row) - count, count):
            row[x] = True
        return row
        
    return row

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