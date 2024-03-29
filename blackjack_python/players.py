"""Players module"""
from functools import total_ordering

from .cards import Card
from .cards import Deck


@total_ordering
class Player:
    """
    :type _NAME: str
    :type MAX_SCORE: int
    :type hands: list[Card]
    :type score: int
    """
    _NAME = 'Player'
    MAX_SCORE = 21

    def __init__(self):
        self.hands = []
        self.score = 0

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.score == other.score

    def __lt__(self, other):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.score < other.score

    def _draw(self, deck):
        """
        :type deck: Deck
        """
        self.hands.append(deck.draw())

    def _hand(self, deal=False):
        """
        :type deal: bool
        :rtype: str
        """
        cards = self.hands[:]

        if deal:
            cards[1] = (cards[1] if self.__class__.__name__ == Player._NAME
                        else '***')

        return ', '.join(str(card) for card in cards)

    def _calculate_score(self):
        """
        :rtype: int
        """
        sum_values = sum(card.value for card in self.hands)
        ace_counter = self._hand().count(Card.RANKS[0])

        for _ in range(ace_counter):
            if sum_values + 10 <= Player.MAX_SCORE:
                sum_values += 10

        self.score = sum_values

    def show(self, deal=False):
        """
        :type deal: bool
        """
        self._calculate_score()

        if deal and self.__class__.__name__ != Player._NAME:
            print(f"{self.__class__.__name__}(--) : {self._hand(deal)}")
            return

        print(f"{self.__class__.__name__}({self.score:2d}) : "
              f"{self._hand(deal)}")

    def hit(self, deck):
        """
        :type deck: Deck
        """
        while self.score < Player.MAX_SCORE:
            is_hit = self.ask('Hit one more card?')
            if is_hit:
                self._draw(deck)
                self._calculate_score()
                self.show()
            else:
                break

    @staticmethod
    def ask(message):
        """
        :type message: str
        :rtype: bool
        """
        while True:
            s = input(f">> {message} [y/n] : ").lower()
            if s == 'y' or s == 'yes':
                return True
            elif s == 'n' or s == 'no':
                return False
            else:
                print('>> Please input [y/n]')


class Dealer(Player):
    """
    :type _STAY_SCORE: int
    """
    _STAY_SCORE = 17

    def deal(self, deck, player):
        """
        :type deck: Deck
        :type player: Player
        """
        deck.shuffle()
        player.__init__()
        self.__init__()

        for _ in range(2):
            player._draw(deck)
            self._draw(deck)

        player.show(deal=True)
        self.show(deal=True)

    def hit(self, deck):
        """
        :type deck: Deck
        """
        while self.score < Dealer._STAY_SCORE:
            self._draw(deck)
            self._calculate_score()


if __name__ == '__main__':
    pass
