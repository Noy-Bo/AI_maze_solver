import time

import fibheap
import heapdict as heapdict
from DataStructures.PriorityQueue import PriorityQueue
from Entities.Node import Node
from Heuristics.Heuristics import diagonalHeuristic, movesCountHeuristic
from Utilities import getCoordsFromDirection, evaluateStats


# this was programmed using 'AI modern approach' pseudo code for UCS algorithm.

#                   DataStructures:
# frontierHashTable - Hashtable, inorder to be able to 'find' in o(1)
# explored - Hashtable to check if a node has already been visited; using python built-in dict with override hashFunction. (3.x python ver)
# fibonacci heap - to check for the next node with least cost.

heuristicCounter = 0
heuristicSum = 0
#ticToc = 0

def Astar (maze,startPoint):
    # initialization
    isHeuristic = True
    frontierCounter = 0
    exploredCounter = 0

    global heuristicSum
    global heuristicCounter
    heuristicCounter = 0
    heuristicSum = 0

    frontierPriorityQueue = PriorityQueue()
    frontierHashTable = {}
    exploredHashTable = {}

    maxRuntime = 60*60  # seconds

    # calculating heuristic to first node
    startPoint.heuristicCost = movesCountHeuristic(startPoint.x,startPoint.y,maze.goalNode)
    startPoint.pathCostWithHeuristic = startPoint.pathCost + startPoint.heuristicCost

    # inserting first node
    frontierHashTable[startPoint.key] = startPoint
    frontierPriorityQueue.push(startPoint)

    # Algorithm
    startTime = time.time()
    while time.time() < (startTime + maxRuntime):
        if frontierPriorityQueue.isEmpty():
            return False

        # deleting node from frontierPriorityQueue
        node = frontierPriorityQueue.pop()
        frontierHashTable.pop(node.key)

        if maze.isGoal(node):
            # stop the timer
            runTime = time.time() - startTime
            evaluateStats('Astar', maze, True, node, frontierPriorityQueue, exploredCounter, runTime, isHeuristic,'Diagonal', (heuristicSum/heuristicCounter))
            return True

        if node.key not in exploredHashTable:
            exploredCounter += 1
        exploredHashTable[node.key] = node
        expandNode(maze, node, frontierPriorityQueue, frontierHashTable, exploredHashTable)

    # time's up!
    runTime = time.time() - startTime
    evaluateStats('Astar', maze, False, node, frontierPriorityQueue, exploredCounter, runTime, isHeuristic,isHeuristic,'Diagonal')
    return False


# this functions receives a node and expand it in order to all direction, inserting the new expanded nodes into frontierPriorityQueue aswell.
def expandNode(maze, node, frontierPriorityQueue, frontierHashTable, exploredHashTable):

    global heuristicSum
    global heuristicCounter

    # the expansion order is like so
    for direction in ['RU','R','RD','D','LD','L','RU','U']:

        x,y = getCoordsFromDirection(direction, node.x, node.y)
        if maze.isValidMove(x,y):
            newNodeCost = maze.getCost(x, y)
            heuristicValue = movesCountHeuristic(x,y,maze.goalNode)
            newNode = Node(x,y,newNodeCost,node,node.pathCost + newNodeCost,node.pathCost + newNodeCost +heuristicValue,node.depth+1,heuristicValue)

            heuristicSum += heuristicValue
            heuristicCounter += 1

            # new node
            if newNode.key not in exploredHashTable and newNode.key not in frontierHashTable:
                frontierPriorityQueue.push(newNode)
                frontierHashTable[newNode.key] = newNode

            # node is in frontier
            elif newNode.key in frontierHashTable:
                if newNode.pathCostWithHeuristic < frontierHashTable[newNode.key].pathCostWithHeuristic or (newNode.pathCostWithHeuristic == frontierHashTable[newNode.key].pathCostWithHeuristic and newNode.heuristicCost < frontierHashTable[newNode.key].heuristicCost):

                    #updating node
                    node = frontierHashTable[newNode.key]
                    node.fatherNode = newNode.fatherNode
                    node.pathCost = newNode.pathCost
                    node.heuristicCost = newNode.heuristicCost
                    node.depth = newNode.depth
                    node.pathCostWithHeuristic = newNode.pathCostWithHeuristic
                    frontierPriorityQueue.decreaseKey(node,newNode.pathCostWithHeuristic)

                    frontierHashTable[newNode.key] = node

            # node in explored and not in frontier
            elif newNode.key in exploredHashTable and newNode.key not in frontierHashTable:
                if newNode.pathCostWithHeuristic < exploredHashTable[newNode.key].pathCostWithHeuristic or ( newNode.pathCostWithHeuristic == exploredHashTable[newNode.key].pathCostWithHeuristic and newNode.heuristicCost < exploredHashTable[newNode.key].heuristicCost):
                    frontierPriorityQueue.push(newNode)
                    frontierHashTable[newNode.key] = newNode
                    #remove from explored????



            

            # old try
            # elif newNode.key in frontierHashTable and (newNode.pathCost < frontierHashTable[newNode.key].pathCost \
            #         or newNode.pathCost == frontierHashTable[newNode.key].pathCost and newNode.heuristicCost < frontierHashTable[newNode.key].heuristicCost):
            #     print("changing node x:{}, y:{}, cost:{}".format(newNode.x,newNode.y,newNode.cost))
            #     print("old pathcost:{}, old heuristic:{}, old H+P:{}".format(frontierHashTable[newNode.key].pathCost,frontierHashTable[newNode.key].heuristicCost,frontierHashTable[newNode.key].pathCostWithHeuristic))
            #     print("new pathcost:{}, new heuristic:{}, new H+P:{}".format(newNode.pathCost,newNode.heuristicCost,newNode.pathCostWithHeuristic))
            #     frontierPriorityQueue.removeSpecific(newNode.x,newNode.y) # this is o(n), need to think of a better way to do it
            #     frontierPriorityQueue.push(newNode)
            #     frontierHashTable[newNode.key] = newNode

