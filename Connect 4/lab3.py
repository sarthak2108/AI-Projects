# 6.034 Fall 2010 Lab 3: Games
# Name: Sarthak Ghosh, Rathish Das
# Email: saghosh@cs.stonybrook.edu, radas@cs.stonybrook.edu

from util import INFINITY

### 1. Multiple choice

# 1.1. Two computerized players are playing a game. Player MM does minimax
#      search to depth 6 to decide on a move. Player AB does alpha-beta
#      search to depth 6.
#      The game is played without a time limit. Which player will play better?
#
#      1. MM will play better than AB.
#      2. AB will play better than MM.
#      3. They will play with the same level of skill.
ANSWER1 = 3

# 1.2. Two computerized players are playing a game with a time limit. Player MM
# does minimax search with iterative deepening, and player AB does alpha-beta
# search with iterative deepening. Each one returns a result after it has used
# 1/3 of its remaining time. Which player will play better?
#
#   1. MM will play better than AB.
#   2. AB will play better than MM.
#   3. They will play with the same level of skill.
ANSWER2 = 2

### 2. Connect Four
from connectfour import *
from basicplayer import *
from util import *
import tree_searcher
import time

## This section will contain occasional lines that you can uncomment to play
## the game interactively. Be sure to re-comment them when you're done with
## them.  Please don't turn in a problem set that sits there asking the
## grader-bot to play a game!
## 
## Uncomment this line to play a game as white:
#run_game(new_player, basic_player)

## Uncomment this line to play a game as black:
#run_game(new_player, basic_player)
#run_game(random_player, human_player)

## Or watch the computer play against itself:
#run_game(basic_player, basic_player)

## Change this evaluation function so that it tries to win as soon as possible,
## or lose as late as possible, when it decides that one side is certain to win.
## You don't have to change how it evaluates non-winning positions.

def focused_evaluate(board):
    """
    Given a board, return a numeric rating of how good
    that board is for the current player.
    A return value >= 1000 means that the current player has won;
    a return value <= -1000 means that the current player has lost
    """    
    raise NotImplementedError


## Create a "player" function that uses the focused_evaluate function
quick_to_win_player = lambda board: minimax(board, depth=4,
                                            eval_fn=focused_evaluate)

## You can try out your new evaluation function by uncommenting this line:
#run_game(basic_player, quick_to_win_player)

## Write an alpha-beta-search procedure that acts like the minimax-search
## procedure, but uses alpha-beta pruning to avoid searching bad ideas
## that can't improve the result. The tester will check your pruning by
## counting the number of static evaluations you make.
##
## You can use minimax() in basicplayer.py as an example.

########################################
#
# alpha_beta_search depends entirely on the
# recursion defined by alpha_beta_rec which
# takes all the same parameters as alpha_beta_search
# with the addition of current_depth, alpha,
# beta, and max_node. The utility for current
# depth will become clear as we explore the
# workings of alpha_beta_rec in more details.
# max_node is true/false depending on whether
# the node is a max/min node. alpha, for a max
# node is the largest evaluation of all the
# children and for a min node it is the alpha
# of the parent. beta, for a min node is the
# smallest evaluation of all the children and
# for a max node it is the beta of the parent.
#
# alpha_beta_rec, like minimax_rec, returns a
# structure instead of only a column number.
# The structure is of the form [(EVALUATION, CURRENT_
# DEPTH, COLUMN), NODES_EXPANDED], where EVALUATION
# corresponds to the best evaluation found
# among the children, CURRENT_DEPTH corresponds
# to the depth from which the evaluation was made,
# and COLUMN corresponds to the move resulting in
# EVALUATION. NODES_EXPANDED, as the name suggests,
# is the number of nodes expanded by the particular
# node.
#
# alpha_beta_search outputs the EXECUTION TIME and NODES
# EXPANDED before returning the required column number.
#
########################################

def alpha_beta_search(board, depth,
                      eval_fn,
                      # NOTE: You should use get_next_moves_fn when generating
                      # next board configurations, and is_terminal_fn when
                      # checking game termination.
                      # The default functions set here will work
                      # for connect_four.
                      get_next_moves_fn=get_all_next_moves,
		      is_terminal_fn=is_terminal):
    start = time.clock()
    [(evaluation, depth_searched, column), total_nodes_expanded] = alpha_beta_rec(board, depth, depth, eval_fn, get_next_moves_fn, is_terminal_fn, -INFINITY, INFINITY, 1)
    stop = time.clock()
    print 'Nodes expanded: ', total_nodes_expanded
    print 'Execution time: ', (stop - start)
    return column
    raise NotImplementedError

def alpha_beta_rec(board, depth, current_depth, eval_fn, get_next_moves_fn, is_terminal_fn, alpha, beta, max_node):
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
    # However, since this same search is used
    # in the longest streak mode, a change has
    # been made. Whne the game terminates in
    # longests streak mode, we always know it
    # is the second player who ended it. So,
    # simply a evaluation of the state is returned.
    #
    ########################################
    if is_terminal_fn(current_depth, board):
        if eval_fn == streak_evaluate:
            return [(eval_fn(board), current_depth, -1), 0]
        else:
            if current_depth <= 0:
                return [(eval_fn(board), current_depth, -1), 0]
            elif max_node == 1:
                return [(-INFINITY, -current_depth, -1), 0]
            else:
                return [(INFINITY, current_depth, -1), 0]

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
    # All this was identical to minimax, so lets
    # turn our attention to the pruniing. Note how,
    # the pruning conditions are modified from
    # a simple alpha >= beta to the ones below. We
    # follow a stricter alpha > beta rule for pruning
    # except for the fringe cases when both are
    # INFINITY of -INFINITY. The reasoning for a
    # stricter pruning rule is this:
    # Suppose, we prune with alpha = beta. But what
    # if beta could have been lower than alpha. That
    # means, a min node may be selecting a move
    # whose alpha value could have been higher, or
    # a max node may be selecting a move whose beta
    # value could have been lower if search was not
    # pruned. That means they may be selecting worse
    # moves as a result of pruning. So, we use a strict
    # greater than to avoid this scenario. However,
    # terminating on equality for the fringe cases
    # of INFINITY and -INFINITY makes sense, as it is
    # possible to better or worse, respectively.
    #
    # Also, note the additional clause for pruning
    # for a max node. current_depth keeps track of
    # the search depth. When the search is in the root,
    # we do not allow pruning as we want the player
    # to consider all possible moves, because there
    # may be moves which lead to a faster conclusion
    # than others. This was really not needed, but
    # included to give the AI a more human feel. This
    # clause can be ignored for the longest streak
    # game mode as a faster conclusion is never
    # on the cards.
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
            [(new_alpha, depth_searched, column), nodes_expanded] = alpha_beta_rec(deepcopy(move[1]), depth, current_depth - 1, eval_fn, get_next_moves_fn, is_terminal_fn, alpha, beta, 0)
            evaluations.append((new_alpha, depth_searched, move[0]))
            total_nodes_expanded += nodes_expanded + 1
            if new_alpha > alpha:
                alpha = new_alpha
            if alpha > beta or alpha == beta == INFINITY:
                if eval_fn == streak_evaluate:
                    break
                elif current_depth != depth:
                    break
        evaluations.sort()
        return [evaluations[len(evaluations) - 1], total_nodes_expanded]
    else:
        ########################################
        # MIN NODE.
        ########################################
        evaluations = []
        total_nodes_expanded = 0
        for move in moves:
            [(new_beta, depth_searched, column), nodes_expanded] = alpha_beta_rec(deepcopy(move[1]), depth, current_depth - 1, eval_fn, get_next_moves_fn, is_terminal_fn, alpha, beta, 1)
            evaluations.append((new_beta, depth_searched, move[0]))
            total_nodes_expanded += nodes_expanded + 1
            if new_beta < beta:
                beta = new_beta
            if alpha > beta or alpha == beta == -INFINITY:
                break
        evaluations.sort()
        return [evaluations[0], total_nodes_expanded]
    raise NotImplementedError

## Now you should be able to search twice as deep in the same amount of time.
## (Of course, this alpha-beta-player won't work until you've defined
## alpha-beta-search.)
#alphabeta_player = lambda board: alpha_beta_search(board,
#                                                   depth=8,
#                                                   eval_fn=focused_evaluate)
alphabeta_player = lambda board: alpha_beta_search(board, depth=4, eval_fn=new_evaluate)


## This player uses progressive deepening, so it can kick your ass while
## making efficient use of time:
ab_iterative_player = lambda board: \
    run_search_function(board,
                        search_fn=alpha_beta_search,
                        eval_fn=focused_evaluate, timeout=5)

run_game(alphabeta_player, basic_player)

## This player uses streak evaluate to play a longest streak wins game.
streak_player = lambda board: alpha_beta_search(board, depth=4, eval_fn=streak_evaluate)

#run_game(streak_player, streak_player, ConnectFourBoard(10))

## Finally, come up with a better evaluation function than focused-evaluate.
## By providing a different function, you should be able to beat
## simple-evaluate (or focused-evaluate) while searching to the
## same depth.

#def better_evaluate(board):    
#    raise NotImplementedError

# Comment this line after you've fully implemented better_evaluate
better_evaluate = memoize(basic_evaluate)

# Uncomment this line to make your better_evaluate run faster.
#better_evaluate = memoize(better_evaluate)

# For debugging: Change this if-guard to True, to unit-test
# your better_evaluate function.
if False:
    board_tuples = (( 0,0,0,0,0,0,0 ),
                    ( 0,0,0,0,0,0,0 ),
                    ( 0,0,0,0,0,0,0 ),
                    ( 0,2,2,1,1,2,0 ),
                    ( 0,2,1,2,1,2,0 ),
                    ( 2,1,2,1,1,1,0 ),
                    )
    test_board_1 = ConnectFourBoard(board_array = board_tuples,
                                    current_player = 1)
    test_board_2 = ConnectFourBoard(board_array = board_tuples,
                                    current_player = 2)
    # better evaluate from player 1
    print "%s => %s" %(test_board_1, better_evaluate(test_board_1))
    # better evaluate from player 2
    print "%s => %s" %(test_board_2, better_evaluate(test_board_2))

## A player that uses alpha-beta and better_evaluate:
your_player = lambda board: run_search_function(board,
                                                search_fn=alpha_beta_search,
                                                eval_fn=better_evaluate,
                                                timeout=5)

#your_player = lambda board: alpha_beta_search(board, depth=4,
#                                              eval_fn=better_evaluate)

## Uncomment to watch your player play a game:
#run_game(your_player, your_player)

## Uncomment this (or run it in the command window) to see how you do
## on the tournament that will be graded.
#run_game(your_player, basic_player)

## These three functions are used by the tester; please don't modify them!
def run_test_game(player1, player2, board):
    assert isinstance(globals()[board], ConnectFourBoard), "Error: can't run a game using a non-Board object!"
    return run_game(globals()[player1], globals()[player2], globals()[board])
    
def run_test_search(search, board, depth, eval_fn):
    assert isinstance(globals()[board], ConnectFourBoard), "Error: can't run a game using a non-Board object!"
    return globals()[search](globals()[board], depth=depth,
                             eval_fn=globals()[eval_fn])

## This function runs your alpha-beta implementation using a tree as the search
## rather than a live connect four game.   This will be easier to debug.
def run_test_tree_search(search, board, depth):
    return globals()[search](globals()[board], depth=depth,
                             eval_fn=tree_searcher.tree_eval,
                             get_next_moves_fn=tree_searcher.tree_get_next_move,
                             is_terminal_fn=tree_searcher.is_leaf)
    
## Do you want us to use your code in a tournament against other students? See
## the description in the problem set. The tournament is completely optional
## and has no effect on your grade.
COMPETE = (None)

## The standard survey questions.
HOW_MANY_HOURS_THIS_PSET_TOOK = ""
WHAT_I_FOUND_INTERESTING = ""
WHAT_I_FOUND_BORING = ""
NAME = ""
EMAIL = ""

