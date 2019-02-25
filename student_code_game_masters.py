from game_master import GameMaster
from read import *
from util import *

class TowerOfHanoiGame(GameMaster):

    def __init__(self):
        super().__init__()
        
    def produceMovableQuery(self):
        """
        See overridden parent class method for more information.

        Returns:
             A Fact object that could be used to query the currently available moves
        """
        return parse_input('fact: (movable ?disk ?init ?target)')

    def getGameState(self):
        """
        Returns a representation of the game in the current state.
        The output should be a Tuple of three Tuples. Each inner tuple should
        represent a peg, and its content the disks on the peg. Disks
        should be represented by integers, with the smallest disk
        represented by 1, and the second smallest 2, etc.

        Within each inner Tuple, the integers should be sorted in ascending order,
        indicating the smallest disk stacked on top of the larger ones.

        For example, the output should adopt the following format:
        ((1,2,5),(),(3, 4))

        Returns:
            A Tuple of Tuples that represent the game state
        """
        ### student code goes here




        ret = [[],[],[]]
        diskLoc = [Fact(["on", '?x', "peg1"]),Fact(["on", '?x', "peg2"]), Fact(["on", '?x', "peg3"])]
        for x, a in enumerate(diskLoc):
            bindings = self.kb.kb_ask(a)
            if bindings:
                for binding in bindings:
                    disk = binding.bindings[0].constant.element[-1]
                    ret[x].append(int(disk))
            ret[x].sort()

        ret = tuple([tuple(x) for x in ret])
        return ret


    def makeMove(self, movable_statement):
        """
        Takes a MOVABLE statement and makes the corresponding move. This will
        result in a change of the game state, and therefore requires updating
        the KB in the Game Master.

        The statement should come directly from the result of the MOVABLE query
        issued to the KB, in the following format:
        (movable disk1 peg1 peg3)

        Args:
            movable_statement: A Statement object that contains one of the currently viable moves

        Returns:
            None
        """
        ### Student code goes here
        #movable statements has disks stores in the first 
        disk = str(movable_statement.terms[0])
        startPeg = str(movable_statement.terms[1])
        endPeg = str(movable_statement.terms[2])



        remove = []
        add = []
        self.kb.kb_retract(Fact(["top", disk, startPeg]))
        self.kb.kb_retract(Fact(["on", disk, startPeg]))


        checkCovering = self.kb.kb_ask(Fact(["covering", disk, "?disk"]))
        if checkCovering:
            newTop = checkCovering[0].bindings[0].constant
            self.kb.kb_retract(Fact(["covering", disk, newTop]))
            self.kb.kb_assert(Fact(["top", newTop, startPeg]))
        else:
            self.kb.kb_assert(Fact(["empty", startPeg]))


        checkEmpty = self.kb.kb_ask(Fact(["empty", endPeg]))
        if checkEmpty:
            self.kb.kb_retract(Fact(["empty", endPeg]))
        else:
            oldTop = self.kb.kb_ask(Fact(["top", "?disk", endPeg]))[0].bindings[0].constant
            self.kb.kb_assert(Fact(["covering", disk, oldTop]))
            self.kb.kb_retract(Fact(["top", oldTop, endPeg]))


        self.kb.kb_assert(Fact(["top", disk, endPeg]))
        self.kb.kb_assert(Fact(["on", disk, endPeg]))



        


    def reverseMove(self, movable_statement):
        """
        See overridden parent class method for more information.

        Args:
            movable_statement: A Statement object that contains one of the previously viable moves

        Returns:
            None
        """
        pred = movable_statement.predicate
        sl = movable_statement.terms
        newList = [pred, sl[0], sl[2], sl[1]]
        self.makeMove(Statement(newList))

class Puzzle8Game(GameMaster):

    def __init__(self):
        super().__init__()

    def produceMovableQuery(self):
        """
        Create the Fact object that could be used to query
        the KB of the presently available moves. This function
        is called once per game.

        Returns:
             A Fact object that could be used to query the currently available moves
        """
        return parse_input('fact: (movable ?piece ?initX ?initY ?targetX ?targetY)')

    def getGameState(self):
        """
        Returns a representation of the the game board in the current state.
        The output should be a Tuple of Three Tuples. Each inner tuple should
        represent a row of tiles on the board. Each tile should be represented
        with an integer; the empty space should be represented with -1.

        For example, the output should adopt the following format:
        ((1, 2, 3), (4, 5, 6), (7, 8, -1))

        Returns:
            A Tuple of Tuples that represent the game state
        """
        ### Student code goes here
        returnList = [[], [], []]
        locations = ['fact: (location ?x {} pos1)', 'fact: (location ?x {} pos2', 'fact: (location ?x {} pos3)']
        xPositions = ['pos1', 'pos2', 'pos3']

        for i, ii in enumerate(locations):
            for x in xPositions:
                var = ii.format(x)
                question = parse_input(var)
                response = self.kb.kb_ask(question)
                tile = response[0].bindings[0].constant.element
                returnList[i].append(int(tile[-1]) if tile != 'empty' else -1)

        returnList = tuple([tuple(x) for x in returnList])
        return returnList



    def makeMove(self, movable_statement):
        """
        Takes a MOVABLE statement and makes the corresponding move. This will
        result in a change of the game state, and therefore requires updating
        the KB in the Game Master.

        The statement should come directly from the result of the MOVABLE query
        issued to the KB, in the following format:
        (movable tile3 pos1 pos3 pos2 pos3)

        Args:
            movable_statement: A Statement object that contains one of the currently viable moves

        Returns:
            None
        """
        ### Student code goes here

        terms = movable_statement.terms
        tile = terms[0]
        old_x = terms[1]
        old_y = terms[2]
        new_x = terms[3]
        new_y = terms[4]

        to_assert = []
        to_assert.append(parse_input('fact: (location {} {} {})'.format(tile, new_x, new_y)))
        to_assert.append(parse_input('fact: (location empty {} {})'.format(old_x, old_y)))

        to_retract = []
        to_retract.append(parse_input('fact: (location {} {} {})'.format(tile, old_x, old_y)))
        to_retract.append(parse_input('fact: (location empty {} {})'.format(new_x, new_y)))

        for tr in to_retract:
            self.kb.kb_retract(tr)

        for ta in to_assert:
            self.kb.kb_assert(ta)



    def reverseMove(self, movable_statement):
        """
        See overridden parent class method for more information.

        Args:
            movable_statement: A Statement object that contains one of the previously viable moves

        Returns:
            None
        """
        pred = movable_statement.predicate
        sl = movable_statement.terms
        newList = [pred, sl[0], sl[3], sl[4], sl[1], sl[2]]
        self.makeMove(Statement(newList))
