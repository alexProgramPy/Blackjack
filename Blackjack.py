# Author: Alex von Allemann
# Python Milestone Project 2
# OOP Principles & concepts

# -- BLACKJACK --

# We import the random class in order to make use of shuffle()
import random

# Global Variables

# We have different suits of cards, stored in a list. Hearts, Diamonds, Spades, Clubs
suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')

# Various ranks of cards in black jack.
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')

# Dictionary-based storage to convert the String version of a number to the integer version.
values = {'Two': 2,'Three': 3,'Four': 4,'Five': 5,'Six': 6,'Seven': 7,'Eight': 8,'Nine': 9,'Ten': 10,'Jack': 10,'Queen': 10,'King': 10,'Ace': 11}

# Initially set to True
playing = True

# Create a class for a Card that defines its attributes and such.
class Card:

    # Each Card will have a suit and rank.
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    # String output for a Card: Two of Hearts for example.
    def __str__(self):
        return f"{self.rank} of {self.suit}"

# Create a class for a singular Deck fof Cards.
class Deck:

    
    def __init__(self):

        # Start with a empty deck of cards in a array.
        self.deck = []

        # We add each Card in a Deck to the empty array.
        for suit in suits:
            for rank in ranks:
                self.deck.append(Card(suit,rank))

    # String output to view all the Cards in the Deck, for Verification purposes.
    def __str__(self):

        deck_comp = ''

        # View all cards in a Deck, printed one after another.
        for card in self.deck:
            deck_comp += '\n' + str(card)

        return "The deck has:" + deck_comp
    # Shuffle the Deck to ensure complete randomness in a draw. IMPORTANT FOR BLACKJACK!
    def shuffle(self):
        random.shuffle(self.deck)
    # Dealing a card from the top of a Deck, with .pop() method.
    def deal(self):
        return self.deck.pop()

# Create a class for a single Hand, which the player has during the game.
class Hand:

    def __init__(self):

        # A player has a list of cards, each with values and we also track the number of aces.
        self.cards = []
        self.value = 0
        self.aces = 0

    def add_card(self,card):
        # We must add cards to the Hand
        self.cards.append(card)
        # Calculate the value of the Players cards depending on the cards rank.
        self.value += values[card.rank]
        # Since Ace can be either a 1 or a 11, we originally choose 1, and add that the Player has picked up a Ace Card to out counter.
        if card.rank == 'Ace':
            self.aces += 1
    
    def adjust_for_ace(self):
        # So if the total value of the Players cards is greater than 21 at the time of check, we make the Ace a 1 instead. Also reduce the number of aces by 1, as we have now taken it into account.
        while self.value > 21 and self.aces:
            self.value -= 10
            self.aces -= 1

# Create a class for the Chips.
# This is what a Player bets on, where Chips equate to money and provide gambling value in the game.
class Chips:

    def __init__(self):

        # Can start off with 100 tokens.
        self.total = 100
        self.bet = 0

    # Wining the bet
    def win_bet(self):
        self.total += self.bet

    # Losing the bet
    def lose_bet(self):
        self.total -= self.bet

# We make a method for taking a bet. Parse in chips that must be altered when doing bets.
def take_bet(chips):

    while True:

        try:
            # We ask the Player, how many chips they want to bet and store the input in chips.bet.
            chips.bet = int(input("How many chips would you like to bet? "))

        except:
            # Catch exception for String or double values entered.
            print("Please enter an integer value.")

        else:
            # Checking to ensure the Player does not overbet, on their total.
            if chips.bet > chips.total:
                print(f"Sorry, you only have {chips.total} chips.")
            else:
                # Exit the While loop.
                break

# This is when the player chooses to hit, we need to parse in the deck and hand.
def hit(deck, hand):
    # Obtain a Card from the Deck.
    card = deck.deal()
    # Add the card to the Hand.
    hand.add_card(card)
    # Check incase the Player has picked up a Ace card.
    hand.adjust_for_ace()

# We make a method to see if the Player wants to hit or stand.
# Parse in the deck and Players hand.
def hit_or_stand(deck, hand):

    # Global variable declaration to assign a playing variable and make it public.
    global playing

    while True:
        # Ask for hit or stand.
        x = input("Hit or Stand? Enter h or s: ")
        # Validate user input.
        if x[0].lower() == 'h':
            print("Hit!")
            hit(deck, hand)

        elif x[0].lower() == 's':

            print("\nPlayer stands. Dealer is playing.")
            # Not currently playing at the time.
            playing = False

        else:
            
            # We ensure that we only have Valid input.
            print("Invalid input. Please enter h or s.")
            # Rerun the loop.
            continue
        # Break out of loop.
        break


# Method for showing some of the Cards between the Dealer and Player.
def show_some(player, dealer):
    # Show only the one card of the dealer at first.
    print("\nDealer's Hand:")
    print("<card hidden>")
    print(dealer.cards[1])

    # Loop through the players cards and display them.
    print("\nPlayer's Hand:")

    for card in player.cards:
        print(card)

    # Print the value back to the player, just to ensure they know how much their total of their Cards are.
    print(f"Value = {player.value}")

# Reveal all the Dealers and Players cards.
def show_all(player, dealer):
    
    print("\nDealer's Hand:")
    # Loop through the Dealers cards.
    for card in dealer.cards:
        print(card)

    print(f"Dealer's Hand Value = {dealer.value}")

    print("\nPlayer's Hand:")
    # Loop through the Players cards.
    for card in player.cards:
        print(card)

    print(f"Player's Hand Value = {player.value}")

# If the player loses, "busts" we must remove their chips from their hand.
def player_busts(player, dealer, chips):

    print("\nPLAYER BUSTS!")
    chips.lose_bet()
    
# If the player wins, we can add the chips to their total.
def player_wins(player, dealer, chips):

    print("\nPLAYER WINS!")
    chips.win_bet()

# If dealer loses, we can add the chips to the players total.
def dealer_busts(player, dealer, chips):

    print("\nDEALER BUSTS! PLAYER WINS!")
    chips.win_bet()

# Dealer wins then we just remove the chips from the players total.
def dealer_wins(player, dealer, chips):

    print("\nDEALER WINS!")
    chips.lose_bet()

# A tie in Blackjack, known as a "push". Just deals with a tie scenario.
def push(player, dealer):

    print("\nPUSH! It's a tie.")

# Actual game flow logic, after the methods and classes.

# Create a variable to instantiate a Chips() class.
player_chips = Chips()

# Keep repeating until the Player exits.
while True:

    print("\n===================================")
    print("WELCOME TO BLACKJACK")
    print("===================================")

    # Create a deck and give it a shuffle.
    deck = Deck()
    deck.shuffle()

    # Create a player hand and give them two cards.
    player_hand = Hand()
    player_hand.add_card(deck.deal())
    player_hand.add_card(deck.deal())

    # Create a dealers hand and give them two cards.
    dealer_hand = Hand()
    dealer_hand.add_card(deck.deal())
    dealer_hand.add_card(deck.deal())

    # We take a bet with the players chips.
    take_bet(player_chips)

    # Show some of the players and dealers cards, in the beginning.
    show_some(player_hand, dealer_hand)

    # Start the game, setting playing to True.
    playing = True

    while playing:
        # Call the method to ask the user if they wish to hit or stand, based on their current hand.
        hit_or_stand(deck, player_hand)

        # Show them the cards again after a hit or stand.
        show_some(player_hand, dealer_hand)

        # Over 21 value, the player loses.
        if player_hand.value > 21:

            player_busts(player_hand, dealer_hand, player_chips)
            # Game ends.
            break
    # Now we know the players hand is less than 21, so theres still a chance they can win.
    if player_hand.value <= 21:

        # Rules for the dealer, where they hit themselfs if their total value is less than but not including 17.
        while dealer_hand.value < 17:
            hit(deck, dealer_hand)
        # Show all the cards of both the dealer and the player, after the dealer has hit.
        show_all(player_hand, dealer_hand)


        # Dealer loses.
        if dealer_hand.value > 21:

            dealer_busts(player_hand, dealer_hand, player_chips)

        # Dealer wins.
        elif dealer_hand.value > player_hand.value:

            dealer_wins(player_hand, dealer_hand, player_chips)

        # Player wins, if the dealers hand is less than the players hand.
        elif dealer_hand.value < player_hand.value:

            player_wins(player_hand, dealer_hand, player_chips)
        # Else there is a tie between the Player and the Dealer.
        else:

            push(player_hand, dealer_hand)

    # Once the game concludes, show the Players total Chips.
    print(f"\nPlayer chips total: {player_chips.total}")
    
    # Ask the user if they with to play again.
    new_game = input("\nWould you like to play again? (y/n): ")

    if new_game[0].lower() == 'y':
        # Continue the while loop.
        continue
    # Else say thanks for playing, and exit the game.
    else:

        print("\nThank you for playing Blackjack!")
        break
    





