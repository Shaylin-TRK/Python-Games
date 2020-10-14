"""

"""


#########################################
# Imports

import os, random

#########################################
# Global Variables


#########################################
# Resource Functions

def clear():
    os.system("CLS")

def wait(message="Press [ENTER] to continue...", spaces = 0):
    input(" " * spaces + message)

def get_deck():

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

    cards = [card for card in deck] #List instance will keep track of available cards print
    final = []

    for i in range(len(cards)):
        final.append(cards.pop(random.randint(0, len(cards) -1)))
    
    return final, deck


#########################################
# Main Game Functions

def reset():
    global status
    global player
    global dealer
    global deck
    global points
    global game

    status = "main"
    player = None
    dealer = Entity(True, 0)
    deck, points = get_deck()
    game = None


def main_menu():
    screen = \
   """
                      Welcome to BlackJack!!
   ____________________________________________________________

                            Main Menu
        /\\         --------------------------         /\\
       /  \\                                          /  \\
       \\  /        [A] Play       [B] Help           \\  /
        \\/         [C] Settings   [D] Credits         \\/

                   [X] Quit
   """
    print(screen)

    answers = ['a', 'b', 'c', 'd', 'x', 's']
    answer = input("\n                   >> ")

    while answer.lower() not in answers:
        clear()
        print(screen, "\n\n", f"    \"{answer}\" is not a valid answer...\n     Please select the letter corresponding to your choice:")
        answer = input("\n                    >> ")
    
    answer = answer.lower()

    if answer == 'a':
        return "play"
    elif answer == 'b':
        return "help"
    elif answer == 'c':
        return "settings"
    elif answer == 'd':
        return 'credits'
    elif answer == 's':
        return 'secret'
    else:
        clear()
        quit()





def new_game():
    
    global dealer
    global player
    global game

    dealer = Entity(True, 0)
    
    screen = \
"""
                    Please Select a Game Mode
   ____________________________________________________________

                           Game Modes
        /\\        ----------------------------        /\\
       /  \\                                          /  \\
       \\  /       [A] FreePlay   [B] MoneyGame       \\  /
        \\/                                            \\/
 
                           [X] Back
"""

    print(screen)

    answers = ['a', 'b', 'x']
    answer = input("\n                   >> ")

    while answer.lower() not in answers:
        clear()
        print(screen, "\n\n", f"    \"{answer}\" is not a valid answer...\n     Please select the letter corresponding to your choice:")
        answer = input("\n                    >> ")
    
    answer = answer.lower()

    if answer == 'a':
        player = Entity(money=0)
        game = Game([dealer, player], 'free')

    elif answer == 'b':
        player = Entity()
        game = Game([dealer, player])

    else:
        global status
        status = None
        return None

    game.deal()
    game.play()





def status_check(status):
    
    if status == "play":
        clear()
        new_game()
    
    elif status == "help":
        print("help")
    
    elif status == "settings":
        print("settings")
    
    elif status == "credits":
        print("credits")

    else:
        print("secret")


#########################################
# Game Classes

class Entity():
    
    hand = ""
    points = 0
    soft_aces = 0
    money = 0

    def __init__(self, dealer=False, money=500):
        self.money = money
        self.dealer = dealer

    def bet(self):
        clear()
        screen = \
f"""
    Account: {player.money}$
    -------------------------------------------------

    Please enter your bet:

"""
        print(screen)
        
        while True:
            players_bet = input("   >> ")

            try:
                players_bet = int(players_bet)

            except ValueError:
                clear()
                print(screen)
                print(f"    \"{players_bet}\" contains characters that are not numeric.\n    Please only enter charachters 0 - 9...")
                continue

            if players_bet <= 0:
                clear()
                print(screen)
                print(f"    \"{players_bet}\" is less than one.\n    Please enter a whole number more than 0...")
            
            elif players_bet > player.money:
                clear()
                print(screen)
                print(f"    \"{players_bet}\" is more than your account holds.\n    Please enter a value less than {player.money}$...")
            
            else:
                break
        
        return players_bet

            



    def hit(self):
        if deck:
            if self.dealer:
                if len(self.hand) == 0:
                    self.hidden_card = deck.pop()
                    self.hidden_points = points[self.hidden_card]
                    if self.hidden_card[0] == "A":
                        self.soft_aces += 1

                    self.hand += "HIDDEN, "
                
                else:
                    card = deck.pop()
                    self.hand += card + ", "
                    if card[0] == "A":
                        self.soft_aces += 1
                
                    self.points += points[card]

            else:
                card = deck.pop()
                self.hand += card + ", "
                if card[0] == "A":
                    self.soft_aces += 1
                
                self.points += points[card]
                

        else:
            print("fatal deck error")
            


class Game():

    def __init__(self, players, game_type="pay"):
        self.game_type = game_type
        self.players = []
        for i in players:
            self.players.append(i)        #players should be a list

        if game_type == "pay":
            self.pot = 0
            for i in players:
                if not i.dealer:
                    current_bet = i.bet()
                    i.money -= current_bet
                    self.pot += current_bet

    def deal(self):
        for i in range(2):
            for j in self.players:
                j.hit()

    def play(self):
        stop = False
        while not stop:
            for player in self.players:
                if not player.dealer:
                    
                    self.display(player)
                    self.choice(player)


    def split(self, player):
        pass


    def display(self, player):
        clear()
        if self.game_type == "free":
            screen = \
    f"""
   ____________________________________________________________

    Dealers Hand: {dealer.hand}
    Dealer Points: {dealer.points}

    Players Hand: {player.hand}
    Players Points: {player.points}

   ____________________________________________________________

    [A] Hit      [B] Stay       [C] Split      [D] Double Down 
                         
    [X] Quit
    """
        
        else:
            screen = \
    f"""
    {player.money}
   ____________________________________________________________

    Dealers Hand: {dealer.hand}
    Dealers Points: {dealer.points}

    Players Hand: {player.hand}
    Players Points: {player.points}

   ____________________________________________________________

    [A] Hit      [B] Stay       [C] Split      [D] Double Down                      
    [X] Quit


    """
        print(screen)

    
    def choice(self, player):
        answers = ['a', 'b', 'c', 'd', 'x']
        answer = input("     >> ").lower()

        while answer not in answers:
            clear()
            self.display(player)
            print(f"    \"{answer}\" is not a valid answer.\n    Please enter the letter corresponding to your choice...")
            answer = input("     >> ").lower()

        if answer == 'a':
            player.hit()

        elif answer == 'b'
            return "finished"

        elif answer == 'c':
            self.split(player)

        elif answer == 'd':
            player.hit()
            return "finished"

        elif answer == 'x':
            return "exit"

    
    


#########################################
# Main Game Loop

def main():
    clear()
    reset()
    
    status = main_menu()
    status_check(status)


while __name__ == "__main__":
    main()


