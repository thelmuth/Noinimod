"""
Tom Helmuth
This is my implementation of Dominion, for two purposes:
1. Test if this is a good game for 110
2. See if I could make an implementation for learning for AI
"""

import copy
import random

class Dominion():

    def __init__(self, p1, p2):
        self._p1 = p1
        self._p2 = p2

        print(self._p1.hand())
        print(self._p2.hand())

        # Setup cards in tableau
        victory = [Estate, Duchy, Province]
        self._basic_victory = [PileOfCards(crd() * 8) for crd in victory]
        self._curses = PileOfCards(Curse() * 10)

        treasure = [Copper, Silver, Gold]
        self._basic_treasure = [PileOfCards(Copper() * 46),
                                PileOfCards(Silver() * 40),
                                PileOfCards(Gold() * 30)]

        kingdom = [Village, Smithy, Market, Witch, Gardens, CouncilRoom, Chapel,
                   Laboratory, Moneylender, Workshop]
        self._kingdom = [PileOfCards(crd() * 10) for crd in kingdom]
        self._kingdom.sort(key=lambda poc : poc.top().name_and_cost())

        # Give starting decks to players


        # self.print_cards()




    def play(self):
        print()

        # e = Estate()
        # c = Copper()
        # v = Village()
        # s = Smithy()
        #
        # cards = [e, c, v, s]
        # for x in cards:
        #     print(x)
        # print()
        # for x in cards:
        #     print(x.name_and_cost())
        #
        # print("----- estates test")
        # estates = Estate() * 4
        # estates[1]._cost = 2999
        # for e in estates:
        #     print(e.name_and_cost())

    def print_cards(self):
        """Prints the tableau"""

        print("-" * 80)

        self.print_width("Victory Cards")
        self.print_width("-------------")
        vp = ""
        for v in self._basic_victory:
            vp += "%-25s" % str(v)
        self.print_width(vp)
        self.print_width(self._curses)

        self.print_width()
        self.print_width("Treasure Cards")
        self.print_width("-------------")
        tre = ""
        for t in self._basic_treasure:
            tre += "%-25s" % str(t)
        self.print_width(tre)

        self.print_width()
        self.print_width("Kingdom Cards")
        self.print_width("-------------")

        for card_cost in range(20):
            cards_at_cost = filter(lambda poc: poc.cost() == card_cost, self._kingdom)
            cds = ""
            for i, c in enumerate(cards_at_cost):
                cds += "%-25s" % str(c)
                if i % 3 == 2:
                    self.print_width(cds)
                    cds = ""
            if cds != "":
                self.print_width(cds)

        print("-" * 80)


    def print_width(self, string=""):
        """Prints a line with |  | on either side, making the whole printed line
        at least 80 characters wide."""

        print("| %-76s |" % string)


################################################################################

class Player():

    def __init__(self):
        self._draw = DrawDeck((Estate() * 3) + (Copper() * 7))
        self._discard = DiscardPile()
        self._hand = Hand()

        self.shuffle()
        for _ in range(5):
            self._hand.add(self._draw.draw())


    def shuffle(self):
        self._draw.shuffle()

    def hand(self):
        return self._hand

class HumanPlayer(Player):

    def __init__(self):
        Player.__init__(self)


class AIPlayer(Player):

    def __init__(self):
        Player.__init__(self)
        self._strategy = [] # This is where the AI's strategy would be stored

################################################################################

class PileOfCards():

    def __init__(self, cards=None):
        if cards == None:
            cards = []

        self._cards = cards # The cards in this pile
        if len(self._cards) != 0:
            card = self._cards[0]
            self._name = card._name
            self._cost = card._cost
            self._basic = card._basic

    def size(self):
        return len(self._cards)

    def empty(self):
        return len(self._cards) == 0

    def top(self):
        return self._cards[0]

    def cost(self):
        return self._cost

    def __str__(self):
        return "$%i %s (%i)" % (self._cost, self._name, self.size())

    def __add__(self, other):
        """Concatenates two piles of cards, returning a new pile."""

        if not isinstance(other, PileOfCards):
            print("Can't + a PileOfCards and something that is not a PileOfCards")
            return
        return PileOfCards(self._cards + other._cards)

    def draw(self):
        """Draws one card from this pile"""
        if self.size() > 0:
            return self._cards.pop()
        return

    def add(self, card):
        """Adds card to this pile"""
        self._cards.append(card)

    def shuffle(self):
        random.shuffle(self._cards)

class DrawDeck(PileOfCards):
    """The draw deck for a player"""

    def __init__(self, cards=None):
        PileOfCards.__init__(self, cards)

class DiscardPile(PileOfCards):
    """The discard pile for a player"""

    def __init__(self, cards=None):
        PileOfCards.__init__(self, cards)

class Hand(PileOfCards):
    """The hand for a player"""

    def __init__(self, cards=None):
        PileOfCards.__init__(self, cards)

    def __str__(self):
        if self.empty():
            return ""

        result = str(self._cards[0])
        for card in self._cards[1:]:
            result += "   " + str(card)

        return result


################################################################################

class Card():

    def __init__(self):
        self._name = ""
        self._type = [] # Options: action, treasure, victory, curse, (attack, reaction, ...)
        self._basic = False # True if a basic victory or treasure, False if Kingdom card
        self._cost = 0
        self._vp = 0

    def __str__(self):
        return self._name

    def name_and_cost(self):
        return "$%i %s" % (self._cost, self._name)

    def __mul__(self, num):
        """Must take num as an integer argument. Returns a list of num copies of this card."""

        if not isinstance(num, int):
            print("Can't multiply a card by anything besides an int.")
            return
        cards = []
        for _ in range(num):
            cards.append(copy.deepcopy(self))
        return cards

################################################################################

class Estate(Card):

    def __init__(self):
        Card.__init__(self)
        self._name = "Estate"
        self._type = ["victory"]
        self._basic = True
        self._cost = 2
        self._vp = 1

class Duchy(Card):

    def __init__(self):
        Card.__init__(self)
        self._name = "Duchy"
        self._type = ["victory"]
        self._basic = True
        self._cost = 5
        self._vp = 3

class Province(Card):

    def __init__(self):
        Card.__init__(self)
        self._name = "Province"
        self._type = ["victory"]
        self._basic = True
        self._cost = 8
        self._vp = 6

class Curse(Card):

    def __init__(self):
        Card.__init__(self)
        self._name = "Curse"
        self._type = ["curse"]
        self._basic = True
        self._cost = 0
        self._vp = -1

class Copper(Card):

    def __init__(self):
        Card.__init__(self)
        self._name = "Copper"
        self._type = ["treasure"]
        self._basic = True
        self._cost = 0

class Silver(Card):

    def __init__(self):
        Card.__init__(self)
        self._name = "Silver"
        self._type = ["treasure"]
        self._basic = True
        self._cost = 3

class Gold(Card):

    def __init__(self):
        Card.__init__(self)
        self._name = "Gold"
        self._type = ["treasure"]
        self._basic = True
        self._cost = 6


################################################################################
# Market, Witch, Gardens, CouncilRoom, Chapel,
#           Laboratory, Moneylender, Workshop

class Village(Card):

    def __init__(self):
        Card.__init__(self)
        self._name = "Village"
        self._type = ["action"]
        self._basic = False
        self._cost = 3

class Smithy(Card):

    def __init__(self):
        Card.__init__(self)
        self._name = "Smithy"
        self._type = ["action"]
        self._basic = False
        self._cost = 4

class Market(Card):

    def __init__(self):
        Card.__init__(self)
        self._name = "Market"
        self._type = ["action"]
        self._basic = False
        self._cost = 5

class Witch(Card):

    def __init__(self):
        Card.__init__(self)
        self._name = "Witch"
        self._type = ["action", "attack"]
        self._basic = False
        self._cost = 5

class Gardens(Card):

    def __init__(self):
        Card.__init__(self)
        self._name = "Gardens"
        self._type = ["victory"]
        self._basic = False
        self._cost = 4

class CouncilRoom(Card):

    def __init__(self):
        Card.__init__(self)
        self._name = "Council Room"
        self._type = ["action"]
        self._basic = False
        self._cost = 5

class Chapel(Card):

    def __init__(self):
        Card.__init__(self)
        self._name = "Chapel"
        self._type = ["action"]
        self._basic = False
        self._cost = 2

class Laboratory(Card):

    def __init__(self):
        Card.__init__(self)
        self._name = "Laboratory"
        self._type = ["action"]
        self._basic = False
        self._cost = 5

class Moneylender(Card):

    def __init__(self):
        Card.__init__(self)
        self._name = "Moneylender"
        self._type = ["action"]
        self._basic = False
        self._cost = 4

class Workshop(Card):

    def __init__(self):
        Card.__init__(self)
        self._name = "Workshop"
        self._type = ["action"]
        self._basic = False
        self._cost = 3


################################################################################

def main():
    player1 = HumanPlayer()
    player2 = HumanPlayer()

    game = Dominion(player1, player2)
    game.play()


if __name__ == "__main__":
    main()
