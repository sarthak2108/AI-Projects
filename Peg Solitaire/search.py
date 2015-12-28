import pegSolitaireUtils
import config

#################################################
#
# A reduced representation of the game
# state. Instead of a 7X7 array, a list containing
# all the occupied positions on the board is
# maintained.
#
# Also, the goal test is applied when a node is
# generated, to avoid unnecessary geneeration of
# siblings.
#
# PRIORITIZATION OF MOVES: Moves which are directed
# towards the center are given preference as our goal
# state is at the center of the board.
#
#################################################

def ItrDeepSearch(pegSolitaireObject):
	#################################################
	# Must use functions:
	# getNextState(self,oldPos, direction)
	# 
	# we are using this function to count,
	# number of nodes expanded, If you'll not
	# use this grading will automatically turned to 0
	#################################################
	#
	# using other utility functions from pegSolitaireUtility.py
	# is not necessary but they can reduce your work if you 
	# use them.
	# In this function you'll start from initial gameState
	# and will keep searching and expanding tree until you 
	# reach goal using Iterative Deepning Search.
	# you must save the trace of the execution in pegSolitaireObject.trace
	# SEE example in the PDF to see what to save
	#
	#################################################
	#
	# This is an iterative implementation of the
	# iterative deepening search algorithm.
	#
	#################################################
	from copy import deepcopy
	if pegSolitaireObject.is_goal():
                return True
        depth = 0
        goalReached = False
        #################################################
        #
        # elements of frontier, a stack, are the tuples
        # of the form (gameState, trace, depth).
        #
        # expanded stores the list of expanded game states.
        #
        # goalReached is a boolean variable which keeps
        # track of when the goal state is reached.
        #
        # solutionDepth is the depth of the search tree
        # where solutions reside. If search depth exceed
        # this, we declare failure. The number of moves
        # required is always 1 less than the number of
        # remaining pegs.
        #
        #################################################
        initialGameState = []
        for i in range(7):
                for j in range(7):
                        if pegSolitaireObject.gameState[i][j] == 1:
                                initialGameState.append((i, j))
        initialTrace = deepcopy(pegSolitaireObject.trace)
        initialState = (initialGameState, initialTrace, 0)
        solutionDepth = len(initialGameState)
        while depth < solutionDepth:
                #################################################
                #
                # Start a new depth-first search with the new
                # depth-limit at the start of each iteration of
                # the outer while loop.
                #
                # If the depth exceeds the solution depth then
                # no solution exists and we exit with failure.
                #
                #################################################
                expanded = []
                frontier = pegSolitaireUtils.Stack()
                frontier.push(deepcopy(initialState))
                while not frontier.isEmpty():
                        #################################################
                        #
                        # Pop the element at the head of expanded and determine
                        # if the popped element can be expanded. It can be
                        # expanded if it itself or through rotation and/or
                        # reflection does not match an element in expanded
                        # AND its Pagoda Value is greater than or equal to
                        # that of the goal state AND it is not on the current
                        # depth-limit. The Pagoda Value and matching through
                        # rotation are effective ways of pruning eventual
                        # dead-ends.
                        #
                        #################################################
                        currentState = deepcopy(frontier.pop())
                        currentGameState = deepcopy(currentState[0])
                        currentTrace = deepcopy(currentState[1])
                        for i in range(7):
                                for j in range(7):
                                        if currentGameState.count((i, j)) == 1:
                                                pegSolitaireObject.gameState[i][j] = 1
                                        elif pegSolitaireObject.gameState[i][j] != -1:
                                                pegSolitaireObject.gameState[i][j] = 0
                        tempGameState = deepcopy(currentGameState)
                        if expanded.count(tempGameState) == 0 and  currentState[2] < depth and notEquivalentBySymmetry(tempGameState, expanded) and pagodaValue(tempGameState) >= 2:
                                #################################################
                                #
                                # List all moves configuratuions from the current
                                # board configuration and add them to frontier, if
                                # they aren't the goal configuration. If a configuration
                                # is the goal, return.
                                #
                                # Add the current board configuration to expanded.
                                #
                                # We check for priority moves first. Then move on
                                # to the non-priority ones. We maintain a temporary
                                # stack tempFrontier where we append the states
                                # resulting from the moves. After all children have
                                # been generated, the elements from tempFrontier is
                                # popped into frontier. This is a necessary step
                                # to complenment our move prioritization by ensuring
                                # that states reached through priority moves are
                                # explored first.
                                #
                                #################################################
                                tempFrontier = pegSolitaireUtils.Stack()
                                for (a, b) in currentGameState:
                                        for direction in config.DIRECTION.keys():
                                                if isPriority((a, b), config.DIRECTION[direction]):
                                                        #################################################
                                                        # Priority Moves
                                                        #################################################
                                                        for i in range(7):
                                                                for j in range(7):
                                                                        if currentGameState.count((i, j)) == 1:
                                                                                pegSolitaireObject.gameState[i][j] = 1
                                                                        elif pegSolitaireObject.gameState[i][j] != -1:
                                                                                pegSolitaireObject.gameState[i][j] = 0
                                                        if pegSolitaireObject.is_validMove((a, b), config.DIRECTION[direction]):
                                                                #################################################
                                                                #
                                                                # pegSolitaireObject.getNextState is used to obtain
                                                                # the board configuration resulting from the current
                                                                # move. This updates the number of nodes expanded.
                                                                #
                                                                #################################################
                                                                placeHold = pegSolitaireObject.getNextState((a, b), config.DIRECTION[direction])
                                                                newGameState = []
                                                                for i in range(7):
                                                                        for j in range(7):
                                                                                if placeHold[i][j] == 1:
                                                                                        newGameState.append((i, j))
                                                                newTrace = deepcopy(currentState[1])
                                                                newTrace.append((a, b))
                                                                newTrace.append(pegSolitaireObject.getNextPosition((a, b), config.DIRECTION[direction]))
                                                                pegSolitaireObject.trace = deepcopy(newTrace)
                                                                if pegSolitaireObject.is_goal():
                                                                        goalReached = True
                                                                        return True
                                                                newState = (newGameState, newTrace, currentState[2] + 1)
                                                                tempFrontier.push(deepcopy(newState))
                                for (a, b) in currentGameState:
                                        for direction in config.DIRECTION.keys():
                                                if not isPriority((a, b), config.DIRECTION[direction]):
                                                        #################################################
                                                        # Non-priority Moves
                                                        #################################################
                                                        for i in range(7):
                                                                for j in range(7):
                                                                        if currentGameState.count((i, j)) == 1:
                                                                                pegSolitaireObject.gameState[i][j] = 1
                                                                        elif pegSolitaireObject.gameState[i][j] != -1:
                                                                                pegSolitaireObject.gameState[i][j] = 0
                                                        if pegSolitaireObject.is_validMove((a, b), config.DIRECTION[direction]):
                                                                #################################################
                                                                #
                                                                # pegSolitaireObject.getNextState is used to obtain
                                                                # the board configuration resulting from the current
                                                                # move. This updates the number of nodes expanded.
                                                                #
                                                                #################################################
                                                                placeHold = pegSolitaireObject.getNextState((a, b), config.DIRECTION[direction])
                                                                newGameState = []
                                                                for i in range(7):
                                                                        for j in range(7):
                                                                                if placeHold[i][j] == 1:
                                                                                        newGameState.append((i, j))
                                                                newTrace = deepcopy(currentState[1])
                                                                newTrace.append((a, b))
                                                                newTrace.append(pegSolitaireObject.getNextPosition((a, b), config.DIRECTION[direction]))
                                                                pegSolitaireObject.trace = deepcopy(newTrace)
                                                                if pegSolitaireObject.is_goal():
                                                                        goalReached = True
                                                                        return True
                                                                newState = (newGameState, newTrace, currentState[2] + 1)
                                                                tempFrontier.push(deepcopy(newState))
                                while not tempFrontier.isEmpty():
                                        frontier.push(deepcopy(tempFrontier.pop()))
                                expanded.append(deepcopy(currentState[0]))
                depth += 1
        if not goalReached:
                pegSolitaireObject.trace = [(-1, -1)]
        #################################################
        #
        # Places the solution in pegSolitaireObject.trace
        # if one is found. Otherwise, when a solution does
        # not exist, sets pegSolitaireObject.trace to [(-1, -1)],
        # an invalid board position.
        #
        #################################################
        return True

#################################################
#
# FUN THING: Any solution to this problem is the
# optimal solution - the game always requires the
# same number of moves to clear the board, no
# matter what the sequence of moves. Hence, we can
# just use greedy best-first search as it is likely
# to expand fewer nodes compared to an A* search with
# the same heuristic and doesn't even have to be
# admissible. It has to be consistent as otherwise
# the search along a path will be broken often.
# Better results have been obtained using best-first
# search compared to A*.
#
# All the same, two admissible and consistent
# heuristics have been used here, cornerBias and
# edgeBias, the latter being the more informed. The
# cost incurred to reach a state is assumed to be
# the number of moves used. 
#
#################################################

def aStarOne(pegSolitaireObject):
	#################################################
        # Must use functions:
        # getNextState(self,oldPos, direction)
        # 
        # we are using this function to count,
        # number of nodes expanded, If you'll not
        # use this grading will automatically turned to 0
        #################################################
        #
        # using other utility functions from pegSolitaireUtility.py
        # is not necessary but they can reduce your work if you 
        # use them.
        # In this function you'll start from initial gameState
        # and will keep searching and expanding tree until you 
	# reach goal using A-Star searching with first Heuristic
	# you used.
        # you must save the trace of the execution in pegSolitaireObject.trace
        # SEE example in the PDF to see what to return
        #
        #################################################
        #
        # This the less informed A* search using the heuristic
        # pagodaValue.
        #
        #################################################
        from copy import deepcopy
        if pegSolitaireObject.is_goal():
                return True
        goalReached = False
        #################################################
        #
        # Elements of frontier, a priority queue, are the
        # tuples of the form (gameState, trace, depth).
        # Here depth represents g(x) of the state.
        #
        # expanded stores the list of expanded game states.
        #
        # goalReached is a boolean variable which keeps
        # track of when the goal state is reached. If this
        # variable is false when the while loop is exited
        # a failure is flagged.
        #
        #################################################
        initialGameState = []
        for i in range(7):
                for j in range(7):
                        if pegSolitaireObject.gameState[i][j] == 1:
                                initialGameState.append((i, j))
        initialTrace = deepcopy(pegSolitaireObject.trace)
        initialState = (initialGameState, initialTrace, 0)
        expanded = []
        frontier = pegSolitaireUtils.PriorityQueue()
        frontier.push(deepcopy(initialState), initialState[2] + cornerBias(initialState[0]))
        while not frontier.isEmpty():
                #################################################
                #
                # Pop the element at the head of expanded and determine
                # if the popped element can be expanded. It can be
                # expanded if it itself or through rotation and/or
                # reflection does not match an element in expanded
                # AND its Pagoda Value is greater than or equal to
                # that of the goal state AND. The Pagoda Value and
                # matching through rotation are effective ways of
                # pruning eventual dead-ends.
                #
                #################################################
                currentState = deepcopy(frontier.pop())
                currentGameState = deepcopy(currentState[0])
                currentTrace = deepcopy(currentState[1])
                for i in range(7):
                        for j in range(7):
                                if currentGameState.count((i, j)) == 1:
                                        pegSolitaireObject.gameState[i][j] = 1
                                elif pegSolitaireObject.gameState[i][j] != -1:
                                        pegSolitaireObject.gameState[i][j] = 0
                tempGameState = deepcopy(currentGameState)
                if expanded.count(tempGameState) == 0 and notEquivalentBySymmetry(tempGameState, expanded) and pagodaValue(tempGameState) >= 2:
                        #################################################
                        #
                        # List all moves configuratuions from the current
                        # board configuration and add them to frontier, if
                        # they aren't the goal configuration. If a configuration
                        # is the goal, return.
                        #
                        # Add the current board configuration to expanded.
                        #
                        # We check for priority moves first. Then move on
                        # to the non-priority ones.
                        #
                        #################################################
                        for (a, b) in currentGameState:
                                for direction in config.DIRECTION.keys():
                                        if isPriority((a, b), config.DIRECTION[direction]):
                                                #################################################
                                                # Priority Moves
                                                #################################################
                                                for i in range(7):
                                                        for j in range(7):
                                                                if currentGameState.count((i, j)) == 1:
                                                                        pegSolitaireObject.gameState[i][j] = 1
                                                                elif pegSolitaireObject.gameState[i][j] != -1:
                                                                        pegSolitaireObject.gameState[i][j] = 0
                                                if pegSolitaireObject.is_validMove((a, b), config.DIRECTION[direction]):
                                                        #################################################
                                                        #
                                                        # pegSolitaireObject.getNextState is used to obtain
                                                        # the board configuration resulting from the current
                                                        # move. This updates the number of nodes expanded.
                                                        #
                                                        #################################################
                                                        placeHold = pegSolitaireObject.getNextState((a, b), config.DIRECTION[direction])
                                                        newGameState = []
                                                        for i in range(7):
                                                                for j in range(7):
                                                                        if placeHold[i][j] == 1:
                                                                                newGameState.append((i, j))
                                                        newTrace = deepcopy(currentState[1])
                                                        newTrace.append((a, b))
                                                        newTrace.append(pegSolitaireObject.getNextPosition((a, b), config.DIRECTION[direction]))
                                                        pegSolitaireObject.trace = deepcopy(newTrace)
                                                        if pegSolitaireObject.is_goal():
                                                                goalReached = True
                                                                return True
                                                        newState = (newGameState, newTrace, currentState[2] + 1)
                                                        frontier.push(deepcopy(newState), newState[2] + cornerBias(newState[0]))
                        for (a, b) in currentGameState:
                                for direction in config.DIRECTION.keys():
                                        if not isPriority((a, b), config.DIRECTION[direction]):
                                                #################################################
                                                # Non-priority Moves
                                                #################################################
                                                for i in range(7):
                                                        for j in range(7):
                                                                if currentGameState.count((i, j)) == 1:
                                                                        pegSolitaireObject.gameState[i][j] = 1
                                                                elif pegSolitaireObject.gameState[i][j] != -1:
                                                                        pegSolitaireObject.gameState[i][j] = 0
                                                if pegSolitaireObject.is_validMove((a, b), config.DIRECTION[direction]):
                                                        #################################################
                                                        #
                                                        # pegSolitaireObject.getNextState is used to obtain
                                                        # the board configuration resulting from the current
                                                        # move. This updates the number of nodes expanded.
                                                        #
                                                        #################################################
                                                        placeHold = pegSolitaireObject.getNextState((a, b), config.DIRECTION[direction])
                                                        newGameState = []
                                                        for i in range(7):
                                                                for j in range(7):
                                                                        if placeHold[i][j] == 1:
                                                                                newGameState.append((i, j))
                                                        newTrace = deepcopy(currentState[1])
                                                        newTrace.append((a, b))
                                                        newTrace.append(pegSolitaireObject.getNextPosition((a, b), config.DIRECTION[direction]))
                                                        pegSolitaireObject.trace = deepcopy(newTrace)
                                                        if pegSolitaireObject.is_goal():
                                                                goalReached = True
                                                                return True
                                                        newState = (newGameState, newTrace, currentState[2] + 1)
                                                        frontier.push(deepcopy(newState), newState[2] + cornerBias(newState[0]))
                        expanded.append(deepcopy(currentState[0]))
        if not goalReached:
                pegSolitaireObject.trace = [(-1, -1)]
        #################################################
        #
        # Places the solution in pegSolitaireObject.trace
        # if one is found. Otherwise, when a solution does
        # not exist, sets pegSolitaireObject.trace to [(-1, -1)],
        # an invalid board position.
        #
        #################################################
	return True

def aStarTwo(pegSolitaireObject):
	#################################################
        # Must use functions:
        # getNextState(self,oldPos, direction)
        # 
        # we are using this function to count,
        # number of nodes expanded, If you'll not
        # use this grading will automatically turned to 0
        #################################################
        #
        # using other utility functions from pegSolitaireUtility.py
        # is not necessary but they can reduce your work if you 
        # use them.
        # In this function you'll start from initial gameState
        # and will keep searching and expanding tree until you 
        # reach goal using A-Star searching with second Heuristic
        # you used.
        # you must save the trace of the execution in pegSolitaireObject.trace
        # SEE example in the PDF to see what to return
        #
        #################################################
        #
        # This the more informed A* search using the heuristic
        # edgeBias.
        #
        #################################################
        from copy import deepcopy
        if pegSolitaireObject.is_goal():
                return True
        goalReached = False
        #################################################
        #
        # Elements of frontier, a priority queue, are the
        # tuples of the form (gameState, trace, depth).
        # Here depth represents g(x) of the state.
        #
        # expanded stores the list of expanded game states.
        #
        # goalReached is a boolean variable which keeps
        # track of when the goal state is reached. If this
        # variable is false when the while loop is exited
        # a failure is flagged.
        #
        #################################################
        initialGameState = []
        for i in range(7):
                for j in range(7):
                        if pegSolitaireObject.gameState[i][j] == 1:
                                initialGameState.append((i, j))
        initialTrace = deepcopy(pegSolitaireObject.trace)
        initialState = (initialGameState, initialTrace, 0)
        expanded = []
        frontier = pegSolitaireUtils.PriorityQueue()
        frontier.push(deepcopy(initialState), initialState[2] + edgeBias(initialState[0]))
        while not frontier.isEmpty():
                #################################################
                #
                # Pop the element at the head of expanded and determine
                # if the popped element can be expanded. It can be
                # expanded if it itself or through rotation and/or
                # reflection does not match an element in expanded
                # AND its Pagoda Value is greater than or equal to
                # that of the goal state AND. The Pagoda Value and
                # matching through rotation are effective ways of
                # pruning eventual dead-ends.
                #
                #################################################
                currentState = deepcopy(frontier.pop())
                currentGameState = deepcopy(currentState[0])
                currentTrace = deepcopy(currentState[1])
                for i in range(7):
                        for j in range(7):
                                if currentGameState.count((i, j)) == 1:
                                        pegSolitaireObject.gameState[i][j] = 1
                                elif pegSolitaireObject.gameState[i][j] != -1:
                                        pegSolitaireObject.gameState[i][j] = 0
                tempGameState = deepcopy(currentGameState)
                if expanded.count(tempGameState) == 0 and notEquivalentBySymmetry(tempGameState, expanded) and pagodaValue(tempGameState) >= 2:
                        #################################################
                        #
                        # List all moves configuratuions from the current
                        # board configuration and add them to frontier, if
                        # they aren't the goal configuration. If a configuration
                        # is the goal, return.
                        #
                        # Add the current board configuration to expanded.
                        #
                        # We check for priority moves first. Then move on
                        # to the non-priority ones.
                        #
                        #################################################
                        for (a, b) in currentGameState:
                                for direction in config.DIRECTION.keys():
                                        if isPriority((a, b), config.DIRECTION[direction]):
                                                #################################################
                                                # Priority Moves
                                                #################################################
                                                for i in range(7):
                                                        for j in range(7):
                                                                if currentGameState.count((i, j)) == 1:
                                                                        pegSolitaireObject.gameState[i][j] = 1
                                                                elif pegSolitaireObject.gameState[i][j] != -1:
                                                                        pegSolitaireObject.gameState[i][j] = 0
                                                if pegSolitaireObject.is_validMove((a, b), config.DIRECTION[direction]):
                                                        #################################################
                                                        #
                                                        # pegSolitaireObject.getNextState is used to obtain
                                                        # the board configuration resulting from the current
                                                        # move. This updates the number of nodes expanded.
                                                        #
                                                        #################################################
                                                        placeHold = pegSolitaireObject.getNextState((a, b), config.DIRECTION[direction])
                                                        newGameState = []
                                                        for i in range(7):
                                                                for j in range(7):
                                                                        if placeHold[i][j] == 1:
                                                                                newGameState.append((i, j))
                                                        newTrace = deepcopy(currentState[1])
                                                        newTrace.append((a, b))
                                                        newTrace.append(pegSolitaireObject.getNextPosition((a, b), config.DIRECTION[direction]))
                                                        pegSolitaireObject.trace = deepcopy(newTrace)
                                                        if pegSolitaireObject.is_goal():
                                                                goalReached = True
                                                                return True
                                                        newState = (newGameState, newTrace, currentState[2] + 1)
                                                        frontier.push(deepcopy(newState), newState[2] + edgeBias(newState[0]))
                        for (a, b) in currentGameState:
                                for direction in config.DIRECTION.keys():
                                        if not isPriority((a, b), config.DIRECTION[direction]):
                                                #################################################
                                                # Non-priority Moves
                                                #################################################
                                                for i in range(7):
                                                        for j in range(7):
                                                                if currentGameState.count((i, j)) == 1:
                                                                        pegSolitaireObject.gameState[i][j] = 1
                                                                elif pegSolitaireObject.gameState[i][j] != -1:
                                                                        pegSolitaireObject.gameState[i][j] = 0
                                                if pegSolitaireObject.is_validMove((a, b), config.DIRECTION[direction]):
                                                        #################################################
                                                        #
                                                        # pegSolitaireObject.getNextState is used to obtain
                                                        # the board configuration resulting from the current
                                                        # move. This updates the number of nodes expanded.
                                                        #
                                                        #################################################
                                                        placeHold = pegSolitaireObject.getNextState((a, b), config.DIRECTION[direction])
                                                        newGameState = []
                                                        for i in range(7):
                                                                for j in range(7):
                                                                        if placeHold[i][j] == 1:
                                                                                newGameState.append((i, j))
                                                        newTrace = deepcopy(currentState[1])
                                                        newTrace.append((a, b))
                                                        newTrace.append(pegSolitaireObject.getNextPosition((a, b), config.DIRECTION[direction]))
                                                        pegSolitaireObject.trace = deepcopy(newTrace)
                                                        if pegSolitaireObject.is_goal():
                                                                goalReached = True
                                                                return True
                                                        newState = (newGameState, newTrace, currentState[2] + 1)
                                                        frontier.push(deepcopy(newState), newState[2] + edgeBias(newState[0]))
                        expanded.append(deepcopy(currentState[0]))
        if not goalReached:
                pegSolitaireObject.trace = [(-1, -1)]
        #################################################
        #
        # Places the solution in pegSolitaireObject.trace
        # if one is found. Otherwise, when a solution does
        # not exist, sets pegSolitaireObject.trace to [(-1, -1)],
        # an invalid board position.
        #
        #################################################
	return True

#################################################
# Utility functions and heuristics
#################################################

def notEquivalentBySymmetry(gameState, expanded):
        #################################################
        #
        # The symmetric nature of the game board implies
        # that if a game state rotated by 90, 180 or 270
        # degrees or a reflection is the same as an already
        # expanded state, then it will also not lead to a
        # solution and hence we will not expand it.
        #
        #################################################
        from copy import deepcopy
        rotatedGameState = deepcopy(gameState)
        reflectedGameState = deepcopy(gameState)
        reflectedGameState = reflectVertical(reflectedGameState)
        if expanded.count(reflectedGameState) > 0:
                return False
        for i in range(3):
                rotatedGameState = rotateByNinety(rotatedGameState)
                if expanded.count(rotatedGameState) > 0:
                        return False
                reflectedGameState = rotateByNinety(reflectedGameState)
                if expanded.count(reflectedGameState) > 0:
                        return False
        return True

def rotateByNinety(gameState):
        #################################################
        #
        # Rotate a 2D array by 90 degrees clockwise.
        #
        #################################################
        tempGameState = []
        for (i, j) in gameState:
                tempGameState.append((j, 6 - i))
        tempGameState.sort()
        return tempGameState

def reflectVertical(gameState):
        #################################################
        #
        # Reflect a 2D array along the vertical axis.
        #
        #################################################
        tempGameState = []
        for (i, j) in gameState:
                tempGameState.append((i, 6 - j))
        tempGameState.sort()
        return tempGameState

def isPriority(oldPos, direction):
        #################################################
        #
        # Determines if a move is priority or not, that is,
        # if it is directed to the center of the board.
        #
        #################################################
        if oldPos[0] < 3 and oldPos[1] < 3:
                if (direction[0] == 1 and direction[1] == 0) or (direction[0] == 0 and direction[1] == 1):
                        return True
        elif oldPos[0] > 3 and oldPos[1] < 3:
                if (direction[0] == -1 and direction[1] == 0) or (direction[0] == 0 and direction[1] == 1):
                        return True
        elif oldPos[0] > 3 and oldPos[1] > 3:
                if (direction[0] == -1 and direction[1] == 0) or (direction[0] == 0 and direction[1] == -1):
                        return True
        elif oldPos[0] < 3 and oldPos[1] > 3:
                if (direction[0] == 1 and direction[1] == 0) or (direction[0] == 0 and direction[1] == -1):
                        return True
        elif oldPos[0] == 3 and oldPos[1] < 3:
                if direction[0] == 0 and direction[1] == 1:
                        return True
        elif oldPos[0] == 3 and oldPos[1] > 3:
                if direction[0] == 0 and direction[1] == -1:
                        return True
        elif oldPos[0] < 3 and oldPos[1] == 3:
                if direction[0] == 1 and direction[1] == 0:
                        return True
        elif oldPos[0] > 3 and oldPos[1] == 3:
                if direction[0] == -1 and direction[1] == 0:
                        return True
        return False

def pagodaValue(gameState):
        #################################################
        #
        # A function evaluating the board state, whose
        # value is non-increasing with every move. When
        # we reach a game state, not the goal, whose
        # Pagoda Value is less than the goal state, we
        # will not expand that state as it will obviously
        # never lead to a solution.
        #
        #################################################
        """pagoda = [[0, 0, 1, 1, 1, 0, 0],
                  [0, 0, 1, 2, 1, 0, 0],
                  [1, 1, 2, 3, 2, 1, 1],
                  [1, 2, 3, 5, 3, 2, 1],
                  [1, 1, 2, 3, 2, 1, 1],
                  [0, 0, 1, 2, 1, 0, 0],
                  [0, 0, 1, 1, 1, 0, 0]]"""
        """pagoda = [[0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 1, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0],
                  [0, 1, 0, 1, 0, 1, 0],
                  [0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 1, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0]]"""
        pagoda = [[0, 0, -1, 0, -1, 0, 0],
                  [0, 0, 1, 1, 1, 0, 0],
                  [-1, 1, 0, 1, 0, 1, -1],
                  [0, 1, 1, 2, 1, 1, 0],
                  [-1, 1, 0, 1, 0, 1, -1],
                  [0, 0, 1, 1, 1, 0, 0],
                  [0, 0, -1, 0, -1, 0, 0]]
        value = 0
        for i in range(7):
                for j in range(7):
                        if gameState.count((i,j)) == 1:
                                value += pagoda[i][j]
        return value

def edgeBias(gameState):
        #################################################
        #
        # A function, like pagodaValue, non-decreasing
        # with each move. But unlike pagodaValue, it is only
        # concerned with the pegs along the board boundary.
        # Also, edgeBias satisfies both admissibility and
        # consistency.
        #
        #################################################
        edge = [[0, 0, 1, 1, 1, 0, 0],
                  [0, 0, 1, 0, 1, 0, 0],
                  [1, 1, 1, 1, 1, 1, 1],
                  [1, 0, 1, 0, 1, 0, 1],
                  [1, 1, 1, 1, 1, 1, 1],
                  [0, 0, 1, 0, 1, 0, 0],
                  [0, 0, 1, 1, 1, 0, 0]]
        value = 0
        for i in range(7):
                for j in range(7):
                        if gameState.count((i,j)) == 1:
                                value += 1#edge[i][j]
        return value

def cornerBias(gameState):
        #################################################
        #
        # A function, like pagodaValue and edgeBias,
        # non-decreasing with each move. But unlike edgeBias,
        # it is only concerned with the pegs on the corners.
        # Naturally, if used as an heuristic this will be
        # less informed than edgeBias. Hence, cornerBias too
        # is admissible and consistent.
        #
        #################################################
        corner = [[0, 0, 1, 0, 1, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0],
                  [1, 0, 1, 0, 1, 0, 1],
                  [0, 0, 0, 0, 0, 0, 0],
                  [1, 0, 1, 0, 1, 0, 1],
                  [0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 1, 0, 1, 0, 0]]
        value = 0
        for i in range(7):
                for j in range(7):
                        if gameState.count((i,j)) == 1:
                                value += corner[i][j]
        return value
