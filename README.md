# blackjack
For Assignment 2
-----------------

This was created for the Introduction to Python course.

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
