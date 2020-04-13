# Mini-project #6 - Blackjack
# Execute in http://www.codeskulptor.org/ to view output

import simplegui
import random

# load card sprite - 936x384 - source: jfitz.com
CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
card_images = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/cards_jfitz.png")

CARD_BACK_SIZE = (72, 96)
CARD_BACK_CENTER = (36, 48)
card_back = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/card_jfitz_back.png")    

# initialize some useful global variables
in_play = False
outcome = ""
score = 0

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}


# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, 
                        card_loc, 
                        CARD_SIZE, 
                        [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], 
                        CARD_SIZE)
        
# define hand class
class Hand:
    def __init__(self):
        self.hand = []

    def __str__(self):
        string_cards = []
        for card in self.hand:
            string_cards.append(str(card))
        
        return "Hand contains " + " ".join(string_cards)

    def add_card(self, card):
        self.hand.append(card)

    def get_value(self):
        hand_value = 0
        cards = [card.get_rank() for card in self.hand]
        
        for card in cards:
            hand_value += VALUES[card]
                
        if 'A' in cards:
            if hand_value + 10 <= 21:
                return hand_value +10
            else:
                return hand_value
        else:
            return hand_value
   
    def draw(self, canvas, pos):
        i = 0
        for card in self.hand:
            card.draw(canvas, (pos[0] + i*CARD_SIZE[0], pos[1]))
            i += 1
 
        
# define deck class 
class Deck:
    def __init__(self):
        self.deck = []
        for suit in SUITS:
            for rank in RANKS:
                self.deck.append(Card(suit, rank))

    def shuffle(self):
        # shuffle the deck 
        random.shuffle(self.deck)

    def deal_card(self):
        if self.deck:
            return self.deck.pop()
        else:
            return "No cards left in the deck!"
    
    def __str__(self):
        string_cards = []
        for card in self.deck:
            string_cards.append(str(card))
        
        return "Deck contains " + " ".join(string_cards)



#define event handlers for buttons
def deal():
    global outcome, in_play, deck, player, dealer, score
    
    if in_play:
        score -= 1
        outcome = "Player lost! New Deal?"
        in_play = False
    else:
        # your code goes here
        player = Hand()
        dealer = Hand()
        deck = Deck()
        deck.shuffle()

        for i in range(2):
            player.add_card(deck.deal_card())
            dealer.add_card(deck.deal_card())

        outcome = "Hit or Stand?"
        in_play = True

def hit():
    global player, in_play, score, outcome
    if in_play:
        if player.get_value() <= 21:
            player.add_card(deck.deal_card())
            outcome = "Hit or Stand?"
            
            if player.get_value() > 21:
                in_play = False
                score -= 1
                outcome = "You have busted! New Deal?"
                print(outcome)
 
       
def stand():
    global outcome, score, in_play
    if in_play:
        while(dealer.get_value() <= 17):
            dealer.add_card(deck.deal_card())
            
        dealer_value = dealer.get_value()
        player_value = player.get_value()
        if dealer_value > 21:
            score += 1
            outcome = "Dealer busted! New Deal?"
            print(outcome)
            in_play = False
        elif player_value > dealer_value:
            score += 1
            outcome = "You won! New Deal?"
            print(outcome)
            in_play = False
        else:
            score -= 1
            outcome = "Dealer won! New Deal?"
            print(outcome)
            in_play = False


# draw handler    
def draw(canvas):
    global player, dealer, outcome, score
    # test to make sure that card.draw works, replace with your code below
    PLAYER_CARD_POS = (100, 150)
    DEALER_CARD_POS = (100, 400)
    BLACKJACK_TITLE_POS = (230, 40)
    PLAYER_TITLE_POS = (100, 140)
    DEALER_TITLE_POS = (100, 390)
    RESULT_POS = (100, 320)
    SCORE_POS = (420, 100)
    
    canvas.draw_text('Blackjack', BLACKJACK_TITLE_POS, 40, 'Yellow', 'monospace')
    canvas.draw_text("Player's Hand", PLAYER_TITLE_POS, 20, 'Yellow', 'monospace')
    canvas.draw_text("Dealer's Hand", DEALER_TITLE_POS, 20, 'Yellow', 'monospace')
    canvas.draw_text(outcome, RESULT_POS, 30, 'Yellow', 'monospace')
    canvas.draw_text("Score: " + str(score), SCORE_POS, 30, 'Yellow', 'monospace')

    player.draw(canvas, PLAYER_CARD_POS)
    dealer.draw(canvas, DEALER_CARD_POS)
    
    if in_play:
        CARD_BACK_POS = DEALER_CARD_POS
        canvas.draw_image(card_back, 
                        CARD_BACK_CENTER, 
                        CARD_BACK_SIZE, 
                        [CARD_BACK_POS[0] + CARD_BACK_CENTER[0], CARD_BACK_POS[1] + CARD_BACK_CENTER[1]], 
                        CARD_BACK_SIZE)
        
        

# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)


# get things rolling
deck = Deck()
player = Hand()
dealer = Hand()
deal()
frame.start()


# remember to review the gradic rubric