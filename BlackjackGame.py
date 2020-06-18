import random
from random import randint

# This is where I created the deck, having suits and ranks in their own 
# list so I can use and call them later, and using a dictionary of values,
# mapped to their respective strings, so I can call on their values in 
# the future.

suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {'Two':2, 'Three':3, 'Four':4, 'Five':5, 'Six':6, 'Seven':7, 'Eight':8, 'Nine':9, 'Ten':10, 'Jack':10,'Queen':10, 'King':10, 'Ace':11}

# To control the game loop.
playing = True

# This is the Card class, which has their suit and rank and can be printed
# Out to see what it is Ex: "Two of Hearts"
class Card:
    
    # Contructor, passing in the suit and rank
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
    
    # String access so we can print information about the card.
    def __str__(self):
        return "{} of {}".format(self.rank, self.suit)

# This is the deck class, which constructs a list of cards, that are from
# the card class, and puts them into a list for us to use. Also can shuffle
# and deal cards.

class Deck:
    
    # Constructor for the Deck class, which creates a list of cards, called deck.
    def __init__(self):
        self.deck = []  # start with an empty list
        for suit in suits:
            for rank in ranks:
                card = Card(suit, rank)
                self.deck.append(card)
    
    #This is so that we can print out all the cards in the list/deck
    def __str__(self):
        for cards in self.deck:
            print(cards)
            
    # Shuffles the deck, by using the shuffle method from the random module.
    def shuffle(self):
        random.shuffle(self.deck)
        
    # Deals a random card from the deck
    def deal(self):
        value = randint(0, len(self.deck))
        # print("I have picked out {} from the deck and will deal it".format(self.deck[value]))
        return self.deck[value]

# This is the hand class, which constructs the hand of a player or computer.
# It also adds the card and adjusts the value, and adjusts the value of 
# the aces so that when the card value is over 21, aces become 1s, and 
class Hand:
    def __init__(self):
        self.cards = []  # start with an empty list as we did in the Deck class
        self.value = 0   # start with zero value
        self.aces = 11    # add an attribute to keep track of aces, can be 1 or 11
    
    # Adds the card and updates the value of the player's hand
    def add_card(self,card):
        self.cards.append(card)
        self.value = self.value + values[card.rank]

    # Adjusts the score, if the hand is over 21, makes the aces in the hand all 1, 
    # and also adjsuts the score accordingly by counting the score all over again
    # by starting at zero and recounting the whole hand.
    
    def adjust_for_ace(self):
        if (self.value + 11 > 21):

            self.value = 0

            for card in self.cards:
                if card.rank == "Ace":
                    self.value = self.value + 1
                    continue
                self.value = self.value + values[card.rank]

    def too_big(self):
        return self.value + 11 > 21

    def show_hand(self):
        for card in self.cards:
            print(card)

class Chips:
    
    def __init__(self):
        self.total = 100  # This can be set to a default value or supplied by a user input
        self.bet = 0
        
    def win_bet(self):
        self.total = self.total + self.bet
    
    def lose_bet(self):
        self.total = self.total - self.bet
    
    def take_bet(self):

        isValidNumber = False

        while not isValidNumber:
            try:
                amount = int(input("\nYou have {} chips, how much would you like to bet?:".format(self.total)))
            except:
                print("\nThe amount you specified is not valid, please try again!")
            else:
                self.bet = amount
                print("\nYou have placed a bet of {}".format(amount))
                isValidNumber = True

def hit(deck, hand):
    card = deck.deal()
    hand.add_card(card)
    hand.adjust_for_ace()

def hit_or_stand(deck,hand):
    
    try: 
        option = input("Would you like to hit or stand?")
    except:
        print("I do not understand what you said, please type either hit or stand.")
    else:
        if (option.lower() == "exit"):
            exit()
        
        if option.lower() == "hit":
            hit(deck, hand)
            print("You have been hit.")  
            return True
        else:
            if option.lower() == "stand":
                return False # Loop will terminate here.
            else:
                print("I DID NOT UNDERSTAND.")
                return True
       
def show_some(player,dealer):
    print("\n******************************************\n")
    
    print("\n This is the Dealer's Hand: \n")

    print(dealer.cards[0])

    print("\n Total Value: {}\n".format(values[dealer.cards[0].rank]))

    print("\n******************************************\n")

    print("\n This is the Player's Hand: \n")

    player.show_hand()

    print("\n Total Value: {}\n".format(player.value))

    print("\n******************************************\n")
    
def show_all(player,dealer):
    print("\n******************************************\n")
    print("\n I will show ALL the cards now: \n")
    print("\n******************************************\n")
    print("\n This is the Dealer's FULL Hand: \n")
    print("\n******************************************\n")
    dealer.show_hand()
    print("\n Total Value: {}\n".format(dealer.value))
    print("\n******************************************\n")
    print("\n This is the Player's FULL Hand: \n")
    player.show_hand()
    print("\n Total Value: {}\n".format(player.value))
    print("\n******************************************\n")

def player_busts(player):
    return player.value > 21

def player_wins(player,dealer):
    return player.value > dealer.value

def dealer_busts(dealer):
    return dealer.value > 21
    
def dealer_wins(player,dealer):
    return player.value < dealer.value
    
def push(player,dealer):
    return player.value == dealer.value


# Set up the Player's chipschips = Chips()
chips = Chips()

while True:
    # Print an opening statement
    print("************************************\nGreetings player, welcome to Blackjack by JACOB JAYME using PYTHON\n************************************")

    # Create & shuffle the deck, deal two cards to each player. Creating Objects.
    deck = Deck()
    dealer = Hand()
    player = Hand()

    #Creating the cards for the Dealer and Player.
    for i in range(2):
        hit(deck, player)
        hit(deck, dealer)

    # Prompt the Player for their bet
    chips.take_bet()

    # Show cards (but keep one dealer card hidden)
    show_some(player, dealer)

    # Setting up the game.
    player_bust = False
    playing = True

    #Game loop for the Player.
    while playing:  
        
        # Prompt for Player to Hit or Stand
        playing = hit_or_stand(deck, player)
        
        # Show cards (but keep one dealer card hidden)
        show_some(player, dealer)
 
        
        # If player's hand exceeds 21, run player_busts() and break out of loop
        if (player_busts(player)):
            print("The player has BUST.\n")
            playing = False # Breaks us out of the loop.
            print("YOU HAVE LOST THE GAME.\n")
            player_bust = True # So in the future we know if the Player has BUST.
            player.value = 0 # So the Dealer either wins or ties.

    # If Player hasn't busted, play Dealer's hand until Dealer reaches 17
    if (not player_bust):
        while (dealer.value < 17):
            hit(deck, dealer)
            if (dealer_busts(dealer)):
                print("The dealer has BUST.\n")
                dealer.value = 0 # So if the player has busted, it will be a tie.
                break

    # Show all cards
    show_all(player, dealer)
    
    # Run different winning scenarios
    if (player_wins(player, dealer)):
        chips.win_bet()
        print("The Player has won!\n")
    if (dealer_wins(player, dealer)):
        chips.lose_bet()
        print("The Dealer has won!\n")
    if (push(player, dealer)):
        print("IT IS A TIE\n")

    # Inform Player of their chips total 
    print("Total Amount of Chips: {} \n".format(chips.total))

    # Ask to play again
    play_again = input("Would you like to play again? (yes or no) \n")
    if (play_again.lower() == "yes"):
        print("You have selected yes, I will now setup the game \n")
    elif (play_again == "no"):
        print("You have selected no, so I will throw you away. Thanks for playing! \n")
        break