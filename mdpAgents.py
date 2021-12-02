# mdpAgents.py
# parsons/20-nov-2017
#
# Version 1
#
# The starting point for CW2.
#
# Intended to work with the PacMan AI projects from:
#
# http://ai.berkeley.edu/
#
# These use a simple API that allow us to control Pacman's interaction with
# the environment adding a layer on top of the AI Berkeley code.
#
# As required by the licensing agreement for the PacMan AI we have:
#
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).

# The agent here is was written by Simon Parsons, based on the code in
# pacmanAgents.py

from pacman import Directions
from game import Agent
import api
import random
import game
import util


class Grid:
    #
    # This class was taken from KEATS 6CCS3AIN Week 5
    #  and slightly modified
    #
         
    def __init__(self, width, height):
        # Constructor
        #
        # Note that it creates variables:
        #
        # grid:   an array that has one position for each element in the grid.
        # width:  the width of the grid
        # height: the height of the grid
        #
        # Grid elements are not restricted, so you can place whatever you
        # like at each location. You just have to be careful how you
        # handle the elements when you use them.
        
        self.width = width
        self.height = height
        subgrid = []
        for i in range(self.height):
            row=[]
            for j in range(self.width):
                row.append(0)
            subgrid.append(row)

        self.grid = subgrid

    def prettyDisplay(self): 
        # This function is a modified version of the one in 
        # the mapAgents.py file, It displays the grid, along with its
        # current utility values as doubles, and the walls as '%'
     
        for i in range(self.height):
            for j in range(self.width):
                # print grid elements with no newline
                val = self.grid[self.height - (i + 1)][j]
                if val == '%':
                    print '{:^8}'.format(val), 
                else:
                    print '{:^8.2f}'.format(val), 
            # A new line after each line of the grid
            print 
        # A line after the grid
        print
        
    def setValue(self, x, y, value):
        # Function from mapAgents.py
        # Set the values of specific elements in the grid.
        # Here x and y are indices.

        self.grid[y][x] = value

    def getValue(self, x, y):
        # Function from mapAgents.py
        # Get the values of specific elements in the grid.
        # Here x and y are indices.

        return self.grid[y][x]

    def getHeight(self):
        # Function from mapAgents.py
        # Return the height to support functions that manipulate the
        # values stored in the grid.

        return self.height

    def getWidth(self):
        # Function from mapAgents.py
        # Return the width to support functions that manipulate the
        # values stored in the grid.

        return self.width

# Value Iteration Values

gamma = 0.6 # Discount factor
reward_food = 2
reward_ghost = -525
reward_capsule = 3
reward_empty_pos = -0.4
iterations = 30

class MDPAgent(Agent):
    #
    # MDP Agent 6CCS3AIN Coursework
    # Made by David Gutierrez Moreno
    # K-number = k19032572
    #
    # This Agent class conducts an MDP using Value iteration to try
    # and find the best actions to take (optimal policies) in order to win
    # the game, that is, eating all the food while avoiding the ghosts.

    def __init__(self):
        # Constructor: this gets run when we first invoke pacman.py

        print "Starting up MDPAgent!"
        name = "Pacman"

    def registerInitialState(self, state):
        # Gets run after an MDPAgent object is created and once there is
        # game state to access.

        print "Running registerInitialState for MDPAgent!"
        print "I'm at:"
        print api.whereAmI(state)
        self.makeMap(state)
        self.addWallsToMap(state)
        self.updateFoodInMap(state)

    def makeMap(self,state):
        # Function taken from KEATS 6CCS3AIN Week 5
        # Make a map by creating a grid of the right size

        corners = api.corners(state)
        height = self.getLayoutHeight(corners)
        width  = self.getLayoutWidth(corners)
        self.map = Grid(width, height)

    def getLayoutHeight(self, corners):
        # Function taken from KEATS 6CCS3AIN Week 5
        # Returns height of the layout
        
        height = -1
        for i in range(len(corners)):
            if corners[i][1] > height:
                height = corners[i][1]
        return height + 1

    def getLayoutWidth(self, corners):
        # Function taken from KEATS 6CCS3AIN Week 5
        # Returns width of the layout

        width = -1
        for i in range(len(corners)):
            if corners[i][0] > width:
                width = corners[i][0]
        return width + 1

    def addWallsToMap(self, state):
        # Function taken from KEATS 6CCS3AIN Week 5
        # Add walls '%' to the map.

        walls = api.walls(state)
        for i in range(len(walls)):
            self.map.setValue(walls[i][0], walls[i][1], '%')

    def updateFoodInMap(self, state):
        # Function taken from KEATS 6CCS3AIN Week 5
        # Update the food '*' in the map.
        # 
        # First, make all grid elements that aren't walls blank.
        for i in range(self.map.getWidth()):
            for j in range(self.map.getHeight()):
                if self.map.getValue(i, j) != '%':
                    self.map.setValue(i, j, 0)
                    # self.map.setValue(i, j, ' ')
        # food = api.food(state)
        # for i in range(len(food)):
        #     self.map.setValue(food[i][0], food[i][1], '*')
        
    def final(self, state):
        # This is what gets run in between multiple games

        print "Looks like the game just ended!"

    def getUtility(self, x, y, original_value):
        # Returns Value of an Action, either the value of the coordinate
        # or the value of the original coordinate in case of a wall
        value = self.map.getValue(x, y)
        if value == '%':
            return original_value
        else:
            return value

    def computeUtility(self, x, y, value, reward):
        # Uses the Bellman update to compute the utility of
        # the position (x,y) in the grid.
        
        # Actions to compute
        up = self.getUtility(x, y+1, value)
        down = self.getUtility(x, y-1, value)
        left = self.getUtility(x-1, y, value)
        right = self.getUtility(x+1, y, value)
        
        # Check if position contains a ghost,food,or pill

        # As instructed in the document, probability of getting the 
        #  action wanted is 0.8, going left is 0.1, and right is 0.1
        up_util = 0.8*up + 0.1*left + 0.1*right
        down_util = 0.8*down + 0.1*left + 0.1*right
        left_util = 0.8*left + 0.1*up + 0.1*down
        right_util = 0.8*right + 0.1*up + 0.1*down

        # Reward + (discount factor * max(utility))
        return reward + (gamma * max(up_util, down_util, left_util, right_util))


    def computeValueIteration(self, state):
        # Compute Value iteration with the current state

        # Getting state info
        ghost_pos = api.ghosts(state)
        ghost_pos_time = api.ghostStatesWithTimes(state) # [((x,y),time),...])]
        # print ghost_pos_time
        # pacman = api.whereAmI(state)
        food = api.food(state)
        capsules = api.capsules(state)
        
        for k in range(iterations):
            newUtilityList = []
            for i in range(self.map.getWidth()):
                for j in range(self.map.getHeight()):
                    value = self.map.getValue(i, j)
                    if value != '%':
                        if (i,j) in ghost_pos:
                            # Determines ghost reward depending on how 'dangerous' it is
                            ghost_time = ghost_pos_time[ghost_pos.index((i,j))][1]
                            if ghost_time > 0:
                                reward = reward_ghost * (1-(0.005*ghost_time))
                            else:
                                reward = reward_ghost
                            # print 'ghost: ' + str(reward)print 'Iteration: ' + str(k)
            # self.map.prettyDisplay()
                        elif (i,j) in food:
                            reward = reward_food
                        elif (i,j) in capsules:
                            reward = reward_capsule
                        else:
                            reward = reward_empty_pos
                        newUtility = self.computeUtility(i, j, value, reward)
                        newUtilityList.append(((i,j), newUtility))
            # print 'Iteration: ' + str(k)
            # self.map.prettyDisplay()
            # Update the map with the new utility values
            for ((i,j), newUtility) in newUtilityList:
                self.map.setValue(i, j, newUtility)

    def getOptimalPolicy(self, state, legal):
        # Returns optimal policy from the legal actions available

        pacman = api.whereAmI(state)
        pacX = pacman[0]
        pacY = pacman[1]
        origin_util = self.map.getValue(pacX, pacY)
        up = self.getUtility(pacX, pacY+1, origin_util)
        down = self.getUtility(pacX, pacY-1, origin_util)
        left = self.getUtility(pacX-1, pacY, origin_util)
        right = self.getUtility(pacX+1, pacY, origin_util)

        action_utilities = []
        for action in legal:
            if action == Directions.NORTH:
                up_util = 0.8*up + 0.1*left + 0.1*right
                action_utilities.append((action, up_util))
            if action == Directions.SOUTH:
                down_util = 0.8*down + 0.1*left + 0.1*right
                action_utilities.append((action, down_util))
            if action == Directions.WEST:
                left_util = 0.8*left + 0.1*up + 0.1*down
                action_utilities.append((action, left_util))
            if action == Directions.EAST:
                right_util = 0.8*right + 0.1*up + 0.1*down
                action_utilities.append((action, right_util))
            # for i in range(len(action_utilities)):
            #     print action_utilities[i]
            # print 'best action: ' + str(max(action_utilities, key = lambda i : i[1]))
        return max(action_utilities, key = lambda i : i[1])[0]

                    

    def getAction(self, state):
        # This is the starting point from where the Agent begins every
        # Action it takes.
        #
        # Prepare map for next value iteration for the next action
        self.updateFoodInMap(state)

        # No 'STOP' action allowed
        legal = api.legalActions(state)
        if Directions.STOP in legal:
            legal.remove(Directions.STOP)

        # Start Value iteration process
        self.computeValueIteration(state)

        # Get the best action (optimal policy)
        bestAction = self.getOptimalPolicy(state, legal)

        # Pacman tries to use optimal policy, bearing in mind
        # that it may not take the action due to its non deterministic nature
        # with 80% probability of succeeding.
        return api.makeMove(bestAction, legal)
