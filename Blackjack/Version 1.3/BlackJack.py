"""
Credits:             Shaylin C.
Name:                BlackJack.py 
Version:             1.3
Requirements:        Python 3.8.3rc1
Date:                9-26-2020
Updated:             10-2-2020 to fix error when selecting "N" after finishing a round
                     which failed to reset the cards.
"""


# MODULE IMPORTS
#######################################################################################
import os
import random


# RESOURCE FUNCTIONS
#     Functions designed to have limited interaction with the over all game state
#######################################################################################

def clear():
    os.system("CLS")

def random_card():
    global cards

    if cards:
        card = random.choice(cards)
        cards.remove(card)
        return card
    
    else:
        print("Error card list empty")

def menu():
    clear()
    screen = f"""
    Welcome to BlackJack {player.name}!!
    ______________________________________

    [A] Play      [B] Help
    [C] Credits   [D] Settings

    [X] Exit 

    """

    print(screen)
    
    answers = ['A', 'B', 'C', 'D', 'X']
    while True:
        answer = input("    >> ")
        if answer.upper() in answers:
            return answer.upper()
        
        else:
            clear()
            print(screen)
            print(f"""

        {answer} is an invalid answer...
        Please enter the letter corresponding to your choice.
            
            """)

def game_help():
    clear()
    
    print("""
    
    BLACKJACK                                        page 1
    _______________________________________________________
      In the game of BlackJack, the player plays against 
    the dealer, competing to see who can get closer to 21
    points without going over this amount.
      The cards are 2 through 10, Jack through King and the
    Ace. There are also four suits: Spades, Clubs, Hearts 
    and Diamonds, and there is one card of each suit.
      
      Each card gives you a number of points:

        2 - 9 are equal to the number of that card
        eg. 4 of Spades gives you 4 points

        10 - King all give you 10 points

        The Ace is special, it normaly gives you 11 points
        but in the event you go over 21, it changes to be
        worth only 1 point.

    """)
    input("    Press [ENTER] to move on...")

    clear()

    print("""
    
    BLACKJACK                                        page 2
    _______________________________________________________
      When the cards are dealt, both the player and the 
    dealer are given two cards. The player is not able to 
    see one of the dealers cards, or know the point value 
    of that card.
      The players turn is first. He/she chooses either Hit
    or Stay. Should the player choose Hit, they are dealt 
    another card and the points of that card are added to
    their total. They can continue to hit until they reach
    21 points or pass that amount, which results in a bust
    and the loss of that hand.
      Should the player choose stay, than they end their 
    turn.
      The dealer moves next, revealing his hidden card.
    He must hit untill he reaches upword of 17 points.
    If, after reaching more than 17 points, he has more
    points than the player, yet has not busted ( or has
    less than 22 points) he wins the hand.

    """)
    input("    Press [ENTER] to move on...")

    clear()
    print("""
    
    BLACKJACK                                        page 3
    _______________________________________________________
      In the event you start a hand with both an Ace and a
    card worth 10 points, eg. Queen of Hearts, than you get
    a BlackJack and automaticly win the hand.
      If the dealer is dealt a BlackJack, and you do not 
    have a BlackJack, he automaticly wins the hand

    """)
    input("    Press [ENTER] to move on...")
    clear()

def game_credits():
    print("This function is a work in progress.. ;)")



def display():
    clear()

    if player.name.isspace():
        name = f"{player.name}'s" 
    else:
        name = "Your"

    d_hand = ""
    d_points = 0
    dealer_hand = dealer.hand.split(", ")
    for card in dealer_hand[1:len(dealer_hand) - 1]:
        d_hand += f" {card}, " 
        d_points += deck[card]

    screen = f"""
    {dealer.name}'s hand: HIDDEN, {d_hand}
    {dealer.name}'s points: {d_points}

    {name} hand: {player.hand}
    {name} points: {player.points}
    ________________________________________________________

    [A] Hit [B] Stay

    """ 
    print(screen)



def winner_display(winner, bust=False):
    clear()

    winning_message = ""

    if winner == "player" and bust:
        winning_message = f"""
    Dealer Busted!

    You win with {player.points} points!
    Dealer got {dealer.points} points.
    """

    elif winner == "player":
        winning_message = f"""
    You win with {player.points} points!
    Dealer got {dealer.points} points.
    """

    elif winner == "dealer" and bust:
        winning_message = f"""
    You Busted!

    Dealer wins with {dealer.points} points!
    You got {player.points} points.
    """

    elif winner == "dealer":
        winning_message = f"""
    Dealer wins with {dealer.points} points!
    You got {player.points} points.
    """

    elif winner == "tie":
        winning_message = f"""
    The game is a tie...

    Dealer had {dealer.points} points.
    You had {player.points} points.
    """
    
    screen = f"""
    
    Dealer hand: {dealer.hand}
    Dealer points: {dealer.points}

    Your hand: {player.hand}
    Your points: {player.points}
    

    {winning_message}
    _________________________________________________________
    """

    print(screen)




# MAIN GAME FUNCTIONS
#     Functions designed to have interaction with the entire program, and the unlimited capability
#     to change global scope variables
#######################################################################################

def reset():
    
    global player
    global dealer      # Global variable change capability
    global cards 
    global name

    # Reset globals to game start value
    
    cards = [i for i in deck]
    if not name:
        name = input("     Please enter your name: ")
    player = Entity(name)
    dealer = Entity()

def deal():

    global player
    global dealer

    player.hit()
    dealer.hit()
    player.hit()
    dealer.hit()

    if dealer.points == 21 and player.points != 21:
        finish("dealer")
    elif player.points == 21 and dealer.points != 21:
        finish("player")
    elif player.points == 21 and dealer.points == 21:
        finish("tie")

def settings():
    print("This function is a work in progress.. ;)")

def finish(winner, bust=False):
    global game_in_progress

    answer = ""
    accepted_answers = ["Y", "N"]


    winner_display(winner, bust)
    print("    Would you like to play again [Y/N]")
    answer = input("    >> ").upper()

    while answer not in accepted_answers:
        winner_display(winner, bust)
        print(f"""
                {answer} that is an invalid answer...
                Please enter the letter corresponding to your choice.
                """)

        answer = input("    >> ").upper()
    
    if answer == "Y":
        reset()
        deal()
        display()

    elif answer == "N":
        game_in_progress = False

    
    

def check_stat(user):
    if user == "player":
        if player.points == 21 and dealer.points != 21:
            finish("player")
        
        elif player.points > 21:
            finish("dealer", True)
    
    elif user == "dealer":
        while dealer.points < 17:
            dealer.hit()
        
        if (dealer.points > 21):
            finish("player", True)

        elif (dealer.points < player.points):
            finish("player")
        
        elif dealer.points == player.points:
            finish("tie")
        
        else:
            finish("dealer")



def stay():
    check_stat(dealer)
    
        


# CLASSES
#    Game classes for player behavior
#########################################################################################
#    Entity class for player behavior, including hit, split and bust

 
class Entity():
    hand = ""
    points = 0
    money = 500
    aces = 0


    def __init__(self, name="Dealer"):
        self.name = name
    

    def hit(self):
        card = random_card()
        if card != None:
            self.hand += f"{card}, "
            self.points += deck[card]
            
            if card[:1] == "A":
                self.aces += 1
        
            if self.points > 21 and self.aces > 0:
                self.points -= 10
                self.aces -= 1
     
    def split(self):
        pass




# SETUP
#    Initial game setup
#########################################################################################
#    Card generation

ranks = ["2", "3", "4", "5", "6", "7", "7", "8", "9", "10", "Jack", "Queen", "King", "Ace"]
suits = ["Spades", "Clubs", "Diamonds", "Hearts"]

no_point = []
for rank in ranks:
    for suit in suits:
        no_point.append(rank + " of " + suit)

deck = {card: 0 for card in no_point} #Deck keeps track of card names and their point value

for i in deck:
    try:
        deck[i] = int(i[0:2])
    
    except:
        royals = ["J", "Q", "K"]
        if i[0] in royals:
            deck[i] = 10
        else: 
            deck[i] = 11

cards = [card for card in deck] #List instance will keep track of available cards 

game_in_progress = False
name = False
# Clear screen by invoking clear()

clear()


# Main welcome message printed

print("""
    \\    /\\    /   +---   |      +---   +--+     /\\    /\\     +---
     \\  /  \\  /    |---   |      |      |  |    /  \\  /  \\    |---
      \\/    \\/     |___   |___   |___   |__|   /    \\/    \\   |___
    
    """)


# Final global scope setup by invoking reset function

reset()

# MAIN GAME SETUP
##########################################################################################
# Declare main() function and run




def main():
    global game_in_progress


    while True:
        answer = menu()
        if answer == "A":         # Play was chosen
            reset()
            deal()
            display()
            game_in_progress = True
        
            while game_in_progress:
                answer = input("    >> ")
                answer = answer.upper()

                if answer == "A":
                    player.hit()
                    display()
                    check_stat("player")

                elif answer == "B":
                    print("Stay")
                    check_stat("dealer")

                else:
                    print(f"""
                {answer} that is an invalid answer...
                Please enter the letter corresponding to your choice.
                """)
        
        
        elif answer == "B":       # Help was chosen
            game_help()
        
        
        elif answer == "C":       # Credits were chosen
            game_credits()

        
        elif answer == "D":                     # Settings were chosen
            settings()

        elif answer == "X":
            break
    
    





# main game loop
if __name__ == "__main__":
    main()