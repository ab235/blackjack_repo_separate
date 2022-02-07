import random

class Card:
    def __init__(self, value, type):
        self.value = value
        self.type = type
    
    def __str__(self):
        signs = '♠♥♣♦'
        card = str(self.value)
        if self.value == 1:
            card = 'A'
        if (self.value == 13):
            card = 'K'
        if (self.value == 12):
            card = 'Q'
        if (self.value == 11):
            card = 'J'

        return card+signs[self.type]
    def __repr__(self):
        signs = '♠♥♣♦'
        card = str(self.value)
        if self.value == 1:
            card = 'A'
        if (self.value == 13):
            card = 'K'
        if (self.value == 12):
            card = 'Q'
        if (self.value == 11):
            card = 'J'

        return card+signs[self.type]

class Deck:
    def __init__(self):
        self.cards = [Card(i,j) for i in range(1,14) for j in range(0,4)]
    
    def __str__(self):
        return str(self.cards)

    def shuffle(self):
        random.shuffle(self.cards)

    def deal(self):
        top = self.cards[0]
        self.cards.pop(0)
        return top

class Player:
    def __init__(self, name):
        self.name = name
        self.cards = []
        self.value = 0

    def add_card(self, card):
        self.cards.append(card)
        self.value += card.value

    def add_str_card(self, card, cards):
        cards.append(str(card))
        print(cards)
        self.cards.append(card)
        self.value += card.value
    def get_sum(self):
        return sum([x.value for x in self.cards])

class Game:
    def __init__(self, player):
        self.deck = Deck()
        self.player = player
        self.dealer = Player("Dealer")
        self.player.cards = []
        self.dealer.cards = []
        self.deck.shuffle()


    def turn(self):
        card = self.deck.deal()
        self.player.add_card(card)
        return 'Your cards: ' + str(self.player.cards)

    def dturn(self):
        self.dealer.add_card(self.deck.deal())
        
    def game_over(self):
        if (self.player.get_sum() > 21):
            return True
        elif (self.dealer.get_sum() > 21):
            return True
        elif (self.player.get_sum() <= 21):
            return False
    
    def stop(self):
        s = self.player.get_sum()
        d = self.dealer.get_sum()
        if (s>21):
            win = False
        elif (d>21):
            win = True
        elif (s > d):
            win = True
        else:
            win = False

        
        return win


