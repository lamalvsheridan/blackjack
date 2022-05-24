"""
Assignment 5 - Blackjack

#####
This is a game of Blackjack. The flow of the application goes like:
#####
Program starts:
- The user will first be prompted to start the game or exit the program.
- The game initializes and shows the player the cards
- If anyone has Blackjack, the game will end, declaring a winner. If both have
    Blackjack, the dealer wins according to the "dealer wins ties" rule in
    the specification.

Player's turn:
- The player will be shown their score and asked to hit or stand.
- If the player hits, they will get a card.
    - If the player busts (Has a score greater than 21), the game ends in the
        player's loss.
    - Otherwise, all the cards and scores will be reprinted, and the player will
        be prompted to hit or stand again
- If the player stands, the hidden dealer card will be shown with a reprint of
    all cards in play, and the dealer's current score will also be shown.

Dealer's turn:
- If the dealer has less than 17, it will hit.
    - If the dealer busts (Has a score greater than 21), the game ends in the
        player's win.
    - Otherwise, all the cards and scores will be reprinted.
- If the dealer has 17 or more (even for "soft" values), the dealer will stand.

End Game:
- The scores are shown
- If the player has more points than the dealer, they win. Otherwise, they lose.
- Program wraps back to the beginning, asking the user to start a new game or
    exit.

#####
# Feature Highlight
#####
- "Soft" value implmentation: Aces can be worth 11 points if it doesn't result
    in bust.
- Simulated deck: When a card is drawn, it is removed from the pool

#####
# Personal Notes
#####
- I didn't use any global variables as I hadn't planned it ahead of time, and
    that resulted in excessive passing of variables between functions.
    Implementing some global variables, such as for the deck and player and
    dealer hands would be a good idea.
"""

"""
#####
# Import statements
#####
"""
import random as rd

"""
#####
# Functions
#####
"""

"""
createDeck() - Generates list representing a deck of 52 cards and returns it.
1's are Aces, 11's are Jacks, 12's are Queens, and 13's are Kings

Suits are represented, but they have no impact on the game and are just use for
flavour. Howevere, they do represent a physical ID for a card, so if a 5 of
clubs is drawn, it won't be drawn again.

The shape is like:
    [[1, '♠'], [1, '♥'],[1, '♣'],[1, '♦']], [2, '♠'] ... [13,'♣'], [13, '♦']]

When used with the drawCard function, the drawn card will be deleted from the
deck. (See createDeck)
"""
def createDeck():
    # Create empty list for using append later
    deck = []
    # Generate number from 1 to 13 for the card values
    for i in range(1,14,1):
        # Create the list shape as described in the
        deck.append([i, '♠'])
        deck.append([i, '♥'])
        deck.append([i, '♣'])
        deck.append([i, '♦'])
    return deck

"""
drawCard - Select a card from the deck and remove it from the deck. Returns the
deck with the card removed, and a "card", a list with the value and suit.

PERSONAL NOTES: No exception handling is in place for when all cards are removed
from the deck. This is not possible during normal execution, but having
something in place would be nice.
"""
def drawCard(deck):
    # Generate a random index for card, after checking availability.
    number = rd.randrange(len(deck))
    card = deck[number]
    # Remove card from deck.
    del deck[number]
    return deck, card

"""
getFinalScore - returns a "score" list (see getScore), but always flips the
"soft" boolean to False and returns the value with the added 10 points, if
applicable.

Used for final score calculations and for dealer logic.
"""
def getFinalScore(hand):
    score = getScore(hand)
    if score[1] and score[0] <= 11:
        score[0] += 10
    score[1] = False
    return score

"""
getDealerChoice - returns a boolean representing if the dealer should hit
(True for hit and False for stand). Checks the finalScore of the dealers
"""
def getDealerChoice(dhand):
    score = getFinalScore(dhand)
    if score[0] < 17:
        return True
    else:
        return False

"""
getScore - calculates the score of the provided hand, along with whether or not
it is a "soft" value.

Also converts anything above 10, which are suppose to represent the face cards,
to 10.

Returns a "score" list:
[{points without the +10 soft value}, {boolean indicating whether it is soft}]
"""
def getScore(hand):
    score = [0, False]
    for i in range(len(hand)):
        value = hand[i][0]
        # Set soft indicator if there is an Ace present
        if value == 1:
            score[1] = True
        # Set all face cards to 10, as they are worth 10 points
        elif value > 10:
            value = 10
        score[0] += value
    return score

"""
hit - Draw a card from the deck, and add it to the provided hand.
"""
def hit(deck, hand):
    deck, card = drawCard(deck)
    hand.append(card)
    return deck, hand

"""
inputErrorMessage - An error message if the user does not provide a valid input
"""
def inputErrorMessage():
    print('You must enter only the number corresponding to your choice.')
    return

"""
isBJ - Checks a hand to see if it is a Blackjack, return True if it is.
PERSONAL NOTE: To be used at the start of game, as it does not check how many
cards are in the hand.
"""
def isBJ(hand):
    score = getFinalScore(hand)
    if score[0] == 21:
        return True
    else:
        return False

"""
pauseForEnter - An input prompt to delay the game until the user hits Enter so
that they can read what is going on before continuing.
"""
def pauseForEnter():
    input("Press Enter to continue...")
    print('')
    return

"""
pauseForEnter - Prints the cards in the provided hand in a 4-char format for
spacing. Lists the cards' value and suit.

If hideDealer is True, show the first card as ** to hide it (for the dealer's
hand on the player's turn).
"""
def printHand(hand, hideDealer=False):
    for i in range(len(hand)):
        # Hide the first card if hideDealer is checked
        if hideDealer and i == 0:
            value = '*'
            suit = '*'
        else:
            value = str(hand[i][0])
            suit = str(hand[i][1])
            # Display Ace, Jack, Queen, or King when applicable
            if value == '1':
                value = 'A'
            elif value == '11':
                value = 'J'
            elif value == '12':
                value = 'Q'
            elif value == '13':
                value = 'K'
        print('{0: >4}'.format(value + suit), end='')
    return

"""
printStatus - Shows the scores of the 2 hands.

If hideDealer is True, do not display the dealer's score as the first dealer
card is hidden

If final = true, display only the finalScore of both players.
"""
def printStatus(dhand, phand, hideDealer=False , final=False):
    # For the dealer's turn, or the end.
    if not hideDealer:
        print('Dealer has: ', end='')
        # For the end of the game.
        if final:
            dscore = getFinalScore(dhand)
            print('{0: >2}'.format(str(dscore[0])), end='')
        # For the dealer's turn only.
        else:
            dscore = getScore(dhand)
            # Show soft value if applicable
            if dscore[1] and dscore[0] <= 11:
                print('{0: >2}'.format(str(dscore[0])), ' (Soft ' + str(dscore[0] + 10) + ')', end='')
            else:
                print('{0: >2}'.format(str(dscore[0])), end='')
        print('')

        pscore = getFinalScore(phand)
        print('You have:   ' + '{0: >2}'.format(str(pscore[0])))
    # For the player's turn
    else:
        print('You have:   ', end='')
        pscore = getScore(phand)
        print('{0: >2}'.format(str(pscore[0])), end='')
        # Show soft value if applicable
        if pscore[1] and pscore[0] <= 11:
            print(' (Soft ' + '{0: >2}'.format(str(pscore[0] + 10)) + ')', end='')
        print('')
    return

"""
printTable - Print the hands of both hands in a presentable way.
"""
def printTable(dhand, phand, hideDealer=False):
    # Print dealer's hand.
    print('Dealer Hand: ', end='')
    # Hide first card if it is player's turn (hideDealer is checked).
    if hideDealer:
        printHand(dhand, True)
    else:
        printHand(dhand)
    print('')

    # Print player's hand.
    print('Player Hand: ', end='')
    printHand(phand)
    print('')
    return

"""
printWinner - Print the final scores and print who the winner is.
"""
def printWinner(dhand, phand):
    # Calculate final scores.
    dscore = getFinalScore(dhand)
    pscore = getFinalScore(phand)

    # Determine winner.
    if pscore[0] > dscore[0]:
        print("Your score is higher than the dealer. You win!")
    elif pscore[0] == dscore[0]:
        print("Your score is the same as the dealer. You lose.")
    elif pscore[0] < dscore[0]:
        print("Your score is lower than the dealer. You lose.")
    else:
        print("Error determining winner.")

    return

"""
startGame(deck) - Draw a card for each player as "hand", a list of cards.
Returns the deck along with the player's and dealer's hands.
"""
def startGame(deck):
    # Draw a card for the player, then dealer, then player, then dealer.
    deck, card = drawCard(deck)
    phand = [card]
    deck, card = drawCard(deck)
    dhand = [card]
    deck, card = drawCard(deck)
    phand.append(card)
    deck, card = drawCard(deck)
    dhand.append(card)
    return deck, phand, dhand

"""
Functions for debugging
"""
# def drawCardDebug1(deck):
#     number = 0
#     suit = 0
#     card = [deck[number][0], deck[number][1][suit]]
#     del deck[number][1][suit]
#     if len(deck[number][1]) < 1:
#         del deck[number]
#     return deck, card
#
# def drawCardDebug2(deck):
#     number = 4
#     suit = 0
#     card = [deck[number][0], deck[number][1][suit]]
#     del deck[number][1][suit]
#     if len(deck[number][1]) < 1:
#         del deck[number]
#     return deck, card
#
# def startGameDebug(deck):
#     deck, card = drawCardDebug1(deck)
#     phand = [card]
#     deck, card = drawCardDebug1(deck)
#     dhand = [card]
#     deck, card = drawCardDebug2(deck)
#     phand.append(card)
#     deck, card = drawCardDebug2(deck)
#     dhand.append(card)
#     return deck, phand, dhand

"""
#####
# Main statement
#####
"""
def main():
    # Welcome message.
    print('Welcome to Blackjack.')

    # Main loop for the game. If this loop is broken the program ends.
    while 1==1:
        # Prompt user to start game or end program.
        choice = 0
        print('1) Start a game.')
        print('2) Exit Program.')
        choice = input('Enter the number corresponding to your choice: ')
        print('')

        # Continue on to the next block if user picks 1.
        if choice == '1':
            pass
        # Exit if user picks 2.
        elif choice == '2':
            exit()
        # Error for all else.
        else:
            inputErrorMessage()
            continue

        # Game initialization.
        deck = createDeck()
        deck, phand, dhand = startGame(deck)
        # deck, phand, dhand = startGameDebug(deck)     # For debugging
        printTable(dhand, phand, True)
        printStatus(dhand, phand, hideDealer=True)

        # Check for Blackjacks, which ends the game.
        if isBJ(dhand):
            print('Dealer has Blackjack!')
            printHand(dhand)
            print('')
            print('You lose.')
            print('Would you like to play again?')
            continue
        elif isBJ(phand):
            print('You have Blackjack! You win!')
            print('Would you like to play again?')
            continue

        # This will be used to skip the next block if player busts.
        pbust = False

        # Player's turn.
        while 1==1:
            # Prompt user to hit or stand.
            choice = 0
            print('What would you like to do?')
            print('1) Hit')
            print('2) Stand')
            choice = input('Enter the number corresponding to your choice: ')
            print('')

            # Give the player a card if they pick 1.
            if choice == '1':
                deck, phand = hit(deck, phand)
                pscore = getScore(phand)
                printTable(dhand, phand, True)
                printStatus(dhand, phand, hideDealer=True)

                # Automatically end player's turn if they have 21.
                if pscore[0] == 21:
                    print('You have 21!')
                    pauseForEnter()
                    break
                # Toggle pbust if player busts and print losing message.
                elif pscore[0] > 21:
                    pbust = True
                    print('Bust! You lose.')
                    pauseForEnter()
                    break
            # Leave the player's turn loop normally if they pick 2.
            elif choice == '2':
                break
            else:
                inputErrorMessage()
                pauseForEnter()
                printTable(dhand, phand, True)
                printStatus(dhand, phand, hideDealer=True)

        # Continue only if player is not bust.
        if not pbust:
            # This will be used to skip the next block if dealer busts.
            dbust = False
            printTable(dhand, phand)
            printStatus(dhand, phand)

            # Dealer's turn.
            while 1==1:
                # Determine if the dealer should hit.
                dealerHits = getDealerChoice(dhand)

                # If dealer hits, give dealer a card.
                if dealerHits:
                    print('Dealer has less than 17. Dealer hits.')
                    pauseForEnter()
                    deck, dhand = hit(deck, dhand)
                    dscore = getScore(dhand)
                    printTable(dhand, phand)
                    printStatus(dhand, phand)
                    # Automatically end dealer's turn if they have 21.
                    if dscore[0] == 21:
                        print('Dealer has 21!')
                        pauseForEnter()
                        break
                    # Toggle pbust if dealer busts and print winning message.
                    elif dscore[0] > 21:
                        dbust = True
                        print('Dealer Busts! You win!')
                        pauseForEnter()
                        break
                # If dealer hits, give dealer a card.
                elif not dealerHits:
                    print('Dealer stands.')
                    pauseForEnter()
                    break
                # Error message
                else:
                    print('Error: Something happened with the dealer.')
                    pauseForEnter()
                    break

            # Final Showdown.
            if not dbust:
                print('Final Scores:')
                printStatus(dhand, phand, final=True)
                printWinner(dhand, phand)
                pauseForEnter()

        # Give a message different from the welcome message before returning
        # to the beginning where they will be prompted to start a new game
        # or exit the program.
        print('Would you like to play again?')

if __name__ == '__main__':
    main()
