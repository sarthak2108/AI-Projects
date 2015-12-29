import sys


def parse_file(filepath):
    ############################################
    # Read the layout file to the board array.
    # Note how the order in which the rows are
    # read is reversed in the final array. This
    # accomodates the requirement that positions
    # arenumbered from the bottom left.
    ############################################
    board = []
    fin = open(filepath)
    line = fin.readline()
    tokens = line.replace('\n', '').split(' ')
    height = int(tokens[0])
    width = int(tokens[1])
    reverse_board = []
    for line in fin:
        tokens = line.replace('\n', '').split(',')
        row = []
        for each_token in tokens:
            if each_token == 'X':
                row.append(each_token)
            else:
                row.append(int(each_token))
        reverse_board.append(row)
    fin.close()
    while len(reverse_board) != 0:
        board.append(reverse_board.pop())
    return board

def convert2CNF(board, output):
    ############################################
    # Interpret the number of constraints.
    #
    # We count the total number of clauses and
    # variables which are necessary in formatting
    # the input file for MINISAT. Each varialbe
    # is named after the board position it
    # represents. A positive sign means it has a
    # bomb, while a negative sign idicates
    # otherwise.
    #
    # We use the following trick to reduce the
    # exponential number of clauses generated in
    # converting DNF to CNF to something that is
    # polynomial.
    # We simply compute how many combinations
    # of eight adjacent positions there is which
    # are gauranteed to have a t least one bomb.
    # We only consider the minimum number of
    # positions required to guarantee a bomb, as
    # all the other rules are entailed from them.
    # This drastically reduces the computational
    # cost from exponential to polynomail.
    ############################################
    from itertools import permutations
    height = len(board)
    width = len(board[0])
    number_of_variables = height * width
    number_of_clauses = 0
    clauses = []
    for i in range(height):
        for j in range(width):
            if board[i][j] != 'X':
                position = (i * width) + j + 1
                pos = get_adjacent_positions(i , j, height, width)
                if board[i][j] == 0:
                    number_of_clauses += 1
                    clauses.append([-position])
                    for p in pos:
                        clauses.append([-p])
                        number_of_clauses += 1
                else:
                    permute = []
                    for k in range(len(pos)):
                        if k < board[i][j] - 1:
                            permute.append(0)
                        else:
                            permute.append(1)
                    permuted = list(set(list(permutations(permute))))
                    number_of_clauses += (len(permuted) + 1)
                    clauses.append([-position])
                    for p in permuted:
                        clause = []
                        for bits in range(len(p)):
                            if p[bits] == 1:
                                clause.append(pos[bits])
                        clauses.append(clause)
    fout = open(output, 'w')
    string = 'p cnf ' + str(number_of_variables) + ' ' + str(number_of_clauses)
    fout.write(string)
    for clause in clauses:
        string = '\n'
        for literal in clause:
            string += str(literal) + ' '
        string += '0'
        fout.write(string)
    fout.close()

def get_adjacent_positions(i, j, height, width):
    ############################################
    # Determines the adjacent positions of a
    # particular position of the board array.
    ############################################
    pos = []
    if i - 1 >= 0:
        if j - 1 >= 0:
            pos.append(((i - 1) * width) + (j - 1) + 1)
        pos.append(((i - 1) * width) + j + 1)
        if j + 1 < width:
            pos.append(((i - 1) * width) + (j + 1) + 1)
    if j - 1 >= 0:
        pos.append((i * width) + (j - 1) + 1)
    if j + 1 < width:
        pos.append((i * width) + (j + 1) + 1)
    if i + 1 < height:
        if j - 1 >= 0:
            pos.append(((i + 1) * width) + (j - 1) + 1)
        pos.append(((i + 1) * width) + j + 1)
        if j + 1 < width:
            pos.append(((i + 1) * width) + (j + 1) + 1)
    return pos

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print 'Layout or output file not specified.'
        exit(-1)
    board = parse_file(sys.argv[1])
    convert2CNF(board, sys.argv[2])
