from collections import deque
from solver import *

class SolverDFS(UninformedSolver):
    def __init__(self, gameMaster, victoryCondition):
        super().__init__(gameMaster, victoryCondition)

    def solveOneStep(self):
        """
        Go to the next state that has not been explored. If a
        game state leads to more than one unexplored game states,
        explore in the order implied by the GameMaster.getMovables()
        function.
        If all game states reachable from a parent state has been explored,
        the next explored state should conform to the specifications of
        the Depth-First Search algorithm.

        Returns:
            True if the desired solution state is reached, False otherwise
        """
        ### Student code goes here
        if self.gm.isWon():
            return True

        self.visited[self.currentState] = True

        moves = self.gm.getMovables()

        for move in moves:
            self.gm.makeMove(move)
            newGameState = GameState(self.gm.getGameState(), self.currentState.depth+1, move)
            newGameState.parent = self.currentState
            if newGameState not in self.visited:
                self.currentState.children.append(newGameState)
                self.visited[newGameState] = False
            elif self.visited[newGameState] == False:
                self.currentState.children.append(newGameState)
            self.gm.reverseMove(move)

        lengthChildren = self.currentState.nextChildToVisit


        while lengthChildren == len(self.currentState.children) and not self.currentState.depth == 0:
            lengthChildren = self.currentState.nextChildToVisit

            self.currentState = self.currentState.parent

            self.gm.reverseMove(self.currentState.requiredMovable)

        lengthChildren = self.currentState.nextChildToVisit

        if self.visited[self.currentState.children[lengthChildren]] == False:
            self.currentState.nextChildToVisit += 1

            self.gm.makeMove(self.currentState.children[lengthChildren].requiredMovable)

            self.currentState = self.currentState.children[lengthChildren]

        return False



class SolverBFS(UninformedSolver):
    def __init__(self, gameMaster, victoryCondition):
        super().__init__(gameMaster, victoryCondition)
        self.myList = dict()
        self.myQueue = deque()
        #self.queue = SolverBFS.Queue()

    def solveOneStep(self):
        """
        Go to the next state that has not been explored. If a
        game state leads to more than one unexplored game states,
        explore in the order implied by the GameMaster.getMovables()
        function.
        If all game states reachable from a parent state has been explored,
        the next explored state should conform to the specifications of
        the Breadth-First Search algorithm.

        Returns:
            True if the desired solution state is reached, False otherwise
        """
        ### Student code goes here

        if self.gm.isWon():
            return True
        self.visited[self.currentState] = True

        moves = self.gm.getMovables()

        if self.currentState.depth:
            i = 0
        else:
            self.myList[self.currentState] = []

        for move in moves:
            self.gm.makeMove(move)

            newGameState = GameState(self.gm.getGameState(), self.currentState.depth+1, move)
            if newGameState in self.visited:
                i = 0
            else:
                self.currentState.children.append(newGameState)

                self.visited[newGameState] = False

                self.myQueue.append(newGameState)
                
                self.myList[newGameState] = []

                i = 0

                while i < len(self.myList[self.currentState]):
                    self.myList[newGameState].append(self.myList[self.currentState][i])
                    i+=1


                    
                self.myList[newGameState].append(newGameState)
                
            self.gm.reverseMove(move)



        for j in range(len(self.myList[self.currentState])):
            self.gm.reverseMove(self.myList[self.currentState][len(self.myList[self.currentState]) - j - 1].requiredMovable)

        self.currentState = self.myQueue.popleft()


        for k in self.myList[self.currentState]: 
            self.gm.makeMove(k.requiredMovable)

        return False
        







