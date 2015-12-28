from util import memoize, run_search_function
from util import INFINITY
import time

########################################
########## SUMMARY OF CHANGES ##########
########################################
#
# basic_evaluate has been modified to return
# -INFINITY instead of -1000 to make it consistent
# with the other evaluation functions.
#
# minimax has been implemeted using recusrsion
# and the helper function minimax_rec
# which accepts all the same parameters as minimax
# with the addition of max_node, which is set
# to true/false depending on whether the
# current node is a max/min node.
#
# new_evaluate has been implemented using the
# various functions available in the ConnectFourBoard
# class.
#
# A completely new addition is streak_evaluate
# which is the evaluation function used when
# the players are playing for the longest
# streak. The longest streak game mode is
# selected when the streak (NEW ADDITION TO
# ConnectFourBoard CLASS) is set to > 7.
# The variable streak has a default value 4,
# and dtermines the length of a streak
# required to win. When a ConnectFourBoard
# class object is created without any
# explicit arguments, the game is the
# traditional Connect4 game. If explicitly
# specified, the game a becomes a more general
# Connectk. Both new_evaluate and streak_evaluate
# takes into consideration the value of streak
# and adjusts evaluations accordingly.
#
########################################

def basic_evaluate(board):
    """
    The original focused-evaluate function from the lab.
    The original is kept because the lab expects the code in the lab to be modified. 
    """
    if board.is_game_over():
        # If the game has been won, we know that it must have been
        # won or ended by the previous move.
        # The previous move was made by our opponent.
        # Therefore, we can't have won, so return -INFINITY.
        # (note that this causes a tie to be treated like a loss)
        score = -INFINITY
    else:
        score = board.longest_chain(board.get_current_player_id()) * 10
        # Prefer having your pieces in the center of the board.
        for row in range(6):
            for col in range(7):
                if board.get_cell(row, col) == board.get_current_player_id():
                    score -= abs(3-col)
                elif board.get_cell(row, col) == board.get_other_player_id():
                    score += abs(3-col)

    return score


def get_all_next_moves(board):
    """ Return a generator of all moves that the current player could take from this position """
    from connectfour import InvalidMoveException

    for i in xrange(board.board_width):
        try:
            yield (i, board.do_move(i))
        except InvalidMoveException:
            pass

def is_terminal(depth, board):
    """
    Generic terminal state check, true when maximum depth is reached or
    the game has ended.
    """
    return depth <= 0 or board.is_game_over()

########################################
#
# minimax depends entirely on the recursion
# defined by minimax_rec which takes all the same
# parameters as minimax with the addition of
# max_node, which is true/false depending on whether
# the node is a max/min node.
#
# minimax_rec also returns a structure instead
# of only a column number. The structure is of the
# form [(EVALUATION, DEPTH, COLUMN), NODES_EXPANDED],
# where EVALUATION corresponds to the best evaluation
# found among the children, DEPTH corresponds
# to the depth from which the evaluation was made,
# and COLUMN corresponds to the move resulting in
# EVALUATION. NODES_EXPANDED, as the name suggests,
# is the number of nodes expanded by the particular
# node.
#
# minimax outputs the EXECUTION TIME and NODES
# EXPANDED before returning the required column number.
#
########################################

def minimax(board, depth, eval_fn = basic_evaluate, get_next_moves_fn = get_all_next_moves, is_terminal_fn = is_terminal, verbose = True):
    """
    Do a minimax search to the specified depth on the specified board.

    board -- the ConnectFourBoard instance to evaluate
    depth -- the depth of the search tree (measured in maximum distance from a leaf to the root)
    eval_fn -- (optional) the evaluation function to use to give a value to a leaf of the tree; see "focused_evaluate" in the lab for an example

    Returns an integer, the column number of the column that the search determines you should add a token to
    """
    start = time.clock()
    [(evaluation, depth_searched, column), total_nodes_expanded] = minimax_rec(board, depth, eval_fn, get_next_moves_fn, is_terminal_fn, 1)
    stop = time.clock()
    print 'Nodes expanded: ', total_nodes_expanded
    print 'Execution time: ', (stop - start)
    return column
    raise NotImplementedError

def minimax_rec(board, depth, eval_fn, get_next_moves_fn, is_terminal_fn, max_node):
    from copy import deepcopy
    ########################################
    #
    # The current node is terminal if either
    # the desired search depth is reached or
    # the game is over.
    #
    # If the desired search depth has been reached
    # then return the evaluation of the game
    # state. Otherwise, return -INFINITY or
    # INFINITY depending on whether the node
    # is a max or min node. The reasoning is as follows:
    # If a game over is detected in a max node then the
    # game must have been finished by the min player, else
    # the game must have been finished by the max player.
    # Since evaluation is always done from the perspective
    # of the max player, this makes sense.
    #
    ########################################
    
    if is_terminal_fn(depth, board):
        if depth <= 0:
            return [(eval_fn(board), depth, -1), 0]
        elif max_node == 1:
            return [(-INFINITY, -depth,  -1), 0]
        else:
            return [(INFINITY, depth, -1), 0]

    ########################################
    #
    # The moves generator is stored in moves.
    #
    # The rest is fairly straightforward. If
    # max_node is set then the maximum evaluation
    # is returned, else the minimum. Note that in
    # cases of ties, they are broken by the depth
    # at which the evaluation is obtained. depth is
    # highest at the root and gradually decreases
    # to zero at the leaves. So when sorted, the
    # evaluation obtained higher up the tree occurs
    # later and that obtained the deepest appears
    # first. The max node selects the rightmost
    # alternative and the min node selects the leftmost
    # alternative after sorting. Thus, on closer
    # inspection, max node will always try to finish
    # off the game the earliest and the min node
    # will try to delay the finish the longest.
    # If there is still a tie max node will select
    # rightmost alternative and min node
    # the leftmost.
    #
    # Note how max_node is reset to 0 by a max
    # node and set to 1 by a min node. This
    # conveys the context to each children and
    # enables them to take the appropriate actions.
    #
    ########################################
    
    moves = get_next_moves_fn(board)
    if max_node == 1:
        ########################################
        # MAX NODE.
        ########################################
        evaluations = []
        total_nodes_expanded = 0
        for move in moves:
            [(evaluation, depth_searched, column), nodes_expanded] = minimax_rec(deepcopy(move[1]), depth - 1, eval_fn, get_next_moves_fn, is_terminal_fn, 0)
            evaluations.append((evaluation, depth_searched, move[0]))
            total_nodes_expanded += nodes_expanded + 1
        evaluations.sort()
        return [evaluations[len(evaluations)-1], total_nodes_expanded]
    else:
        ########################################
        # MIN NODE.
        ########################################
        evaluations = []
        total_nodes_expanded = 0
        for move in moves:
            [(evaluation, depth_searched, column), nodes_expanded] = minimax_rec(deepcopy(move[1]), depth - 1, eval_fn, get_next_moves_fn, is_terminal_fn, 1)
            evaluations.append((evaluation, depth_searched, move[0]))
            total_nodes_expanded += nodes_expanded + 1
        evaluations.sort()
        return [evaluations[0], total_nodes_expanded]
    raise NotImplementedError


def rand_select(board):
    """
    Pick a column by random
    """
    import random
    moves = [move for move, new_board in get_all_next_moves(board)]
    return moves[random.randint(0, len(moves) - 1)]

def new_evaluate(board):
    if board.is_game_over():
        ########################################
        #
        # If the game has been won, we know that it must have been
        # won or ended by the previous move.
        # The previous move was made by our opponent.
        # Therefore, we can't have won, so return -INFINITY.
        # (note that this causes a tie to be treated like a loss)
        #
        ########################################
        score = -INFINITY
    else:
        ########################################
        #
        # Prefer having your pieces in the center
        # of the board. This is a cardinal rule of
        # Connect4 and hence left to guide the
        # search during the initial stages of the
        # game. Note that upto this postion, the
        # function is identical to basic_evaluate.
        # However, new_evaluate is more informed
        # as it takes into consideration impending
        # threats, both from itself as well as the
        # opponent. The contribution to evaluation
        # from threats takes over the primary role
        # in the latter stages of the game. As then
        # acknowledging threats and countering them
        # is more important than playing to the middle.
        #
        # This evaluation is much more superior to
        # basic_evaluate as will be proved during
        # a head-to-head session between the two. This
        # strategy actually takes into account whether
        # current player played first or second and
        # chooses a strategy accordingly. These strategies
        # are independent and each can be used for
        # both the cases of playing first and second, to
        # beat basic_evaluate.
        #
        # The strategy used for playeing first is
        # less informed and hence more aggresive.
        # The strategy for playing second is more
        # informed and conservative. When put head
        # to head, the latter strategy beats the
        # former, as expected.
        #
        # Both have been kept because both are good
        # examples of evaluation functions.
        #
        # As already mentioned, this evaluation
        # function adapts itself for a ConnectK game. 
        #
        ########################################
        
        streak = board.get_streak()
        DIRECTION = [[(-1, 0), (1, 0)], [(0, -1), (0, 1)], [(-1, -1), (1, 1)], [(-1, 1), (1, -1)]]
        score = 0
        for row in range(6):
            for col in range(7):
                if board.get_cell(row, col) == board.get_current_player_id():
                    score -= abs(3-col)
                elif board.get_cell(row, col) == board.get_other_player_id():
                    score += abs(3-col)
        current_player_threats = []
        other_player_threats = []
        if board.get_current_player_id() == 1:
            ########################################
            # Strategy for playing first.
            ########################################
            #
            # Takse into account only threats from
            # consecutive K-1 - streaks having open
            # ends. Aggresive and utilizes the fact
            # that the first player generally has the
            # upper-hand.
            #
            # Threats are stored as board positions
            # each player's threats exists. Separate
            # lists are maintained for the players.
            #
            ########################################
            
            for row in range(6):
                for col in range(7):
                    chains = []
                    if board.get_cell(row, col) != 0:
                        chains.append((board._contig_vector_length(row, col, (-1, 0)) + 1 + board._contig_vector_length(row, col, (1, 0)), (1, 0)))
                        chains.append((board._contig_vector_length(row, col, (0, -1)) + 1 + board._contig_vector_length(row, col, (0, 1)), (0, 1)))    
                        chains.append((board._contig_vector_length(row, col, (-1, -1)) + 1 + board._contig_vector_length(row, col, (1, 1)), (1, 1)))
                        chains.append((board._contig_vector_length(row, col, (-1, 1)) + 1 + board._contig_vector_length(row, col, (1, -1)), (-1, 1)))
                        for chain in chains:
                            if chain[0] == streak - 1:
                                cells = []
                                cells.extend(board._contig_vector_cells(row, col, (chain[1][0], chain[1][1])))
                                cells.extend(board._contig_vector_cells(row, col, (-chain[1][0], -chain[1][1])))
                                cells.append((row, col))
                                cells.sort()
                                if board.get_cell(row, col) == board.get_current_player_id():
                                    if 0 <= cells[0][0] - chain[1][0] < 6 and 0 <= cells[0][1] - chain[1][1] < 7:
                                        if board.get_cell(cells[0][0] - chain[1][0], cells[0][1] - chain[1][1]) == 0:
                                            current_player_threats.append((cells[0][0] - chain[1][0], cells[0][1] - chain[1][1]))
                                    if 0 <= cells[len(cells) - 1][0] + chain[1][0] < 6 and 0 <= cells[len(cells) - 1][1] + chain[1][1] < 7:
                                        if board.get_cell(cells[0][0] - chain[1][0], cells[0][1] - chain[1][1]) == 0:
                                            current_player_threats.append((cells[0][0] + chain[1][0], cells[0][1] + chain[1][1]))
                                elif board.get_cell(row, col) == board.get_other_player_id():
                                    if 0 <= cells[0][0] - chain[1][0] < 6 and 0 <= cells[0][1] - chain[1][1] < 7:
                                        if board.get_cell(cells[0][0] - chain[1][0], cells[0][1] - chain[1][1]) == 0:
                                            other_player_threats.append((cells[0][0] - chain[1][0], cells[0][1] - chain[1][1]))
                                    if 0 <= cells[len(cells) - 1][0] + chain[1][0] < 6 and 0 <= cells[len(cells) - 1][1] + chain[1][1] < 7:
                                        if board.get_cell(cells[0][0] - chain[1][0], cells[0][1] - chain[1][1]) == 0:
                                            other_player_threats.append((cells[0][0] + chain[1][0], cells[0][1] + chain[1][1]))
        else:
            ########################################
            # Strategy for playing second.
            ########################################
            #
            # Takes into account all threats, not
            # just consecutive K-1 - streaks. Considers
            # whether two smaller streaks can be combined
            # to finish the game. More informed and has an
            # advantage playing second since it can counter
            # better than the former strategy.
            #
            ########################################
            for row in range(6):
                for col in range(7):
                    if board.get_cell(row, col) == 0:
                        for direction in DIRECTION:
                            if 0 <= row + direction[0][0] <= 5 and 0 <= col + direction[0][1] <= 6:
                                if board.get_cell(row + direction[0][0], col + direction[0][1]) != 0:
                                    first_extension = board._contig_vector_length(row + direction[0][0], col + direction[0][1], direction[0]) + 1
                                else:
                                    first_extension = 0
                            else:
                                first_extension = 0
                            if 0 <= row + direction[1][0] <= 5 and 0 <= col + direction[1][1] <= 6:
                                if board.get_cell(row + direction[1][0], col + direction[1][1]) != 0:
                                    second_extension = board._contig_vector_length(row + direction[1][0], col + direction[1][1], direction[1]) + 1
                                else:
                                    second_extension = 0
                            else:
                                second_extension = 0
                            if first_extension >= streak - 1:
                                if board.get_current_player_id() == board.get_cell(row + direction[0][0], col + direction[0][1]):
                                    current_player_threats.append((row, col))
                                else:
                                    other_player_threats.append((row, col))
                            if second_extension >= streak - 1:
                                if board.get_current_player_id() == board.get_cell(row + direction[1][0], col + direction[1][1]):
                                    current_player_threats.append((row, col))
                                else:
                                    other_player_threats.append((row, col))
                            if first_extension > 0 and second_extension > 0:
                                if board.get_cell(row + direction[0][0], col + direction[0][1]) == board.get_cell(row + direction[1][0], col + direction[1][1]) and first_extension + 1 + second_extension >= streak:
                                    if board.get_current_player_id() == board.get_cell(row + direction[0][0], col + direction[0][1]):
                                        current_player_threats.append((row, col))
                                    else:
                                        other_player_threats.append((row, col))

        ########################################
        #
        # Convert each threat list to set as the
        # same threat may have been recorded from
        # multiple streaks.
        #
        # If there are no threats play to the
        # middle.
        #
        # not all threats are real though. If a
        # threat exists for a player in a column,
        # and another threat esists in the same
        # column below that for the same or the
        # other player then the former threat is
        # to realize before the latter.
        #
        # The lists of threats are accordingly
        # evaluated taking into consideration only
        # the real threats.
        #
        # Note that the reward and penalty from
        # threats is much greater than those for
        # playing to the middle. This ensures,
        # priority is given to threats, when they
        # arise.
        #
        ########################################
        
        current_player_threats = set(current_player_threats)
        other_player_threats = set(other_player_threats)
        if len(current_player_threats) == 0 and len(other_player_threats) == 0:
            return score
        real_threats = []
        for col in range(7):
            temp_threats = []
            for threat in current_player_threats:
                if threat[1] == col:
                    temp_threats.append(threat)
            for threat in other_player_threats:
                if threat[1] == col:
                    temp_threats.append(threat)
            temp_threats.sort()
            if len(temp_threats) > 0:
                real_threats.append(temp_threats[len(temp_threats) - 1])
        for threat in current_player_threats:
            if threat in real_threats:
                score += 40
        for threat in other_player_threats:
            if threat in real_threats:
                score -= 40
    return score
    raise NotImplementedError

def streak_evaluate(board):
    ########################################
    #
    # This evaluation function is used in the
    # longest streak game mode. Note that this
    # function does return a value of -INFINITY,
    # by default, when the game is over, as
    # the criteria for deciding a game over
    # does not determine the winner. The game
    # is over when each player has played 10
    # pieces. The winner is the one with the
    # longest streak.
    #
    # This function is used in streak_player's
    # definition.
    #
    ########################################
    #
    # It makes sense for rewards and penalties
    # to somewhat exclusively involve longets
    # streaks.
    #
    # However, it is still encourages to play
    # to the middle as doing so singnificantly
    # impedes the opponent's attempts to create
    # longer streaks.
    #
    # This is a balanced evaluation. When used
    # against itself, results in draws.
    #
    ########################################
    if board.is_game_over():
        if board.longest_chain(board.get_current_player_id()) - board.longest_chain(board.get_other_player_id()) < 0:
            return -INFINITY
        else:
            return INFINITY
        # If the game has been won, we know that it must have been
        # won or ended by the previous move.
        # The previous move was made by our opponent.
        # Therefore, we can't have won, so return -INFINITY.
        # (note that this causes a tie to be treated like a loss)
        score = -INFINITY
    
    score = (board.longest_chain(board.get_current_player_id()) * 10) - (board.longest_chain(board.get_other_player_id()) * 10)
    for row in range(6):
        for col in range(7):
            if board.get_cell(row, col) == board.get_current_player_id():
                score -= abs(3-col)
            elif board.get_cell(row, col) == board.get_other_player_id():
                score += abs(3-col)

    return score


random_player = lambda board: rand_select(board)
basic_player = lambda board: minimax(board, depth=4, eval_fn=basic_evaluate)
new_player = lambda board: minimax(board, depth=4, eval_fn=new_evaluate)
progressive_deepening_player = lambda board: run_search_function(board, search_fn=minimax, eval_fn=basic_evaluate)
