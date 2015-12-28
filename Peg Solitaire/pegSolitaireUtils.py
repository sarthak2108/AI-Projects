import heapq
import readGame

#######################################################
# These are some Helper functions which you have to use 
# and edit.
# Must try to find out usage of them, they can reduce
# your work by great deal.
#
# Functions to change:
# 1. is_wall(self, pos):
# 2. is_validMove(self, oldPos, direction):
# 3. getNextPosition(self, oldPos, direction):
# 4. getNextState(self, oldPos, direction):
#######################################################
class game:
	def __init__(self, filePath):
        	self.gameState = readGame.readGameState(filePath)
                self.nodesExpanded = 0
		self.trace = []	
	
	def is_corner(self, pos):
		########################################
		# You have to make changes from here
		# check for if the new positon is a corner or not
		# return true if the position is a corner
		if pos[0] > 6 or pos[1] > 6 or pos[0] < 0 or pos[1] < 0:
                        return True
		if self.gameState[pos[0]][pos[1]] == -1:
                        return True
		return False	
	
	
	def getNextPosition(self, oldPos, direction):
		#########################################
		# YOU HAVE TO MAKE CHANGES HERE
		# See DIRECTION dictionary in config.py and add
		# this to oldPos to get new position of the peg if moved
		# in given direction , you can remove next line
		newPos = (oldPos[0] + direction[0] + direction[0], oldPos[1] + direction[1] + direction[1])
		return newPos 
	
	
	def is_validMove(self, oldPos, direction):
		#########################################
		# DONT change Things in here
		# In this we have got the next peg position and
		# below lines check for if the new move is a corner
		newPos = self.getNextPosition(oldPos, direction)
		if self.is_corner(newPos):
			return False	
		#########################################
		
		########################################
		# YOU HAVE TO MAKE CHANGES BELOW THIS
		# check for cases like:
		# if new move is already occupied
		# or new move is outside peg Board
		# Remove next line according to your convenience
		intPos = (newPos[0] - direction[0], newPos[1] - direction[1])
		if newPos[0] > 6 or newPos[1] > 6 or newPos[0] < 0 or newPos[1] < 0:
                        return False
		if self.gameState[newPos[0]][newPos[1]] == 1:
                        return False
                if self.gameState[intPos[0]][intPos[1]] == 0:
                        return False
		return True
	
	def getNextState(self, oldPos, direction):
		###############################################
		# DONT Change Things in here
		self.nodesExpanded += 1
		if not self.is_validMove(oldPos, direction):
			print "Error, You are not checking for valid move"
			exit(0)
		###############################################
		
		###############################################
		# YOU HAVE TO MAKE CHANGES BELOW THIS
		# Update the gameState after moving peg
		# eg: remove crossed over pegs by replacing it's
		# position in gameState by 0
		# and updating new peg position as 1
		newPos = (oldPos[0] + direction[0] + direction[0], oldPos[1] + direction[1] + direction[1])
		intPos = (newPos[0] - direction[0], newPos[1] - direction[1])
		self.gameState[oldPos[0]][oldPos[1]] = 0
		self.gameState[intPos[0]][intPos[1]] = 0
		self.gameState[newPos[0]][newPos[1]] = 1
		return self.gameState

	def is_goal(self):
                ###############################################
                # New addition.
                # Determines if the given configuration in
                # gameState represents the goal.
                ###############################################
                if self.gameState[3][3] == 0:
                        return False
                for i in range(7):
                        for j in range(7):
                                if self.gameState[i][j] == 1 and (i != 3 or j != 3):
                                        return False
                return True

#################################################
# The following have been taken from util.py of the
# Pacman AI projects developed at UC Berkeley.
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html
#################################################

class Stack:
        # A container with a last-in-first-out (LIFO) queuing policy.
        def __init__(self):
                self.list = []
    
        def push(self,item):
                # Push 'item' onto the stack
                self.list.append(item)

        def pop(self):
                # Pop the most recently pushed item from the stack
                return self.list.pop()

        def isEmpty(self):
                # Returns true if the stack is empty
                return len(self.list) == 0

class Queue:
        # A container with a first-in-first-out (FIFO) queuing policy.
        def __init__(self):
                self.list = []
  
        def push(self,item):
                # Enqueue the 'item' into the queue
                self.list.insert(0,item)

        def pop(self):
                # Dequeue the earliest enqueued item still in the queue. This
                # operation removes the item from the queue.
                return self.list.pop()

        def isEmpty(self):
                #Returns true if the queue is empty
                return len(self.list) == 0
  
class PriorityQueue:
        ###############################################
        # Implements a priority queue data structure. Each inserted item
        # has a priority associated with it and the client is usually interested
        # in quick retrieval of the lowest-priority item in the queue. This
        # data structure allows O(1) access to the lowest-priority item.
        #
        # Note that this PriorityQueue does not allow you to change the priority
        # of an item.  However, you may insert the same item multiple times with
        # different priorities.
        ###############################################
        def  __init__(self):  
                self.heap = []
    
        def push(self, item, priority):
                pair = (priority,item)
                heapq.heappush(self.heap,pair)

        def pop(self):
                (priority,item) = heapq.heappop(self.heap)
                return item
  
        def isEmpty(self):
                return len(self.heap) == 0

class PriorityQueueWithFunction(PriorityQueue):
        ###############################################
        # Implements a priority queue with the same push/pop signature of the
        # Queue and the Stack classes. This is designed for drop-in replacement for
        # those two classes. The caller has to provide a priority function, which
        # extracts each item's priority.
        ###############################################
        def  __init__(self, priorityFunction):
                # priorityFunction (item) -> priority
                self.priorityFunction = priorityFunction
                PriorityQueue.__init__(self)
    
        def push(self, item):
                # Adds an item to the queue with priority from the priority function
                PriorityQueue.push(self, item, self.priorityFunction(item))
