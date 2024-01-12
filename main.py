import turtle
from random import randint

shoeDeck = []   # playing card deck
cardsFace = ["2", "3", "4", "5", "6",
             "7", "8", "9", "10",
             "J", "Q", "K", "A"]
scr_dct = {"J": 10, "Q": 10, "K": 10, "A": 11}
suits = {"SPADE": "♠", "CLUB": "♣", "HEART": "♥", "DIAMOND": "♦"}


def create_deck(decks=1):
    """Adds cards to playing deck
    :parameter: number of decks to add"""
    for j in range(decks):
        for i in range(13):
            shoeDeck.append(cardsFace[i]+" SPADE")
            shoeDeck.append(cardsFace[i]+" CLUB")
            shoeDeck.append(cardsFace[i]+" HEART")
            shoeDeck.append(cardsFace[i]+" DIAMOND")


def deal_card(person_cards):
    """Uses a random index within 0-number of cards in playing deck
    :parameter: person's list of cards"""
    card = shoeDeck[randint(0, len(shoeDeck)-1)]
    person_cards.append(card)
    shoeDeck.remove(card)   # remove card from playing deck to avoid repeats


def add_to_score(person_cards, person_score):
    """Uses index 0 of card string to convert face value and adds to the list of card values
    :parameter: person's list of card, the list of card values"""
    card = person_cards[-1]
    face = card.split(" ")
    try:
        person_score.append(int(face[0]))   # uses the face value of the card 1-10
    except ValueError:                      # since J-A are not integer, value error results
        person_score.append(int(scr_dct[face[0]]))  # use face value dictionary for J-A


def decision(person, person_cards, person_score, xaxis, yaxis, checked_ace=False):
    """User inputs if they want to hit, or stand
    This function is called again within itself if user has an ace and exceeds 21
    :parameter: person, list of person's cards, list of person's score,
                display on x-axis, display on y-axis, always false when called outside scope of function"""
    if not checked_ace:  # the function has not checked for ace in player deck
        change_x = 75    # for displaying purposes (avoids new card blocking another card)
    else:                # the function has checked ace
        change_x = (len(person_cards)-1)*75
    while sum(person_score) < 21:  # continues to prompt user until stand or bust
        choice = turtle.textinput('Decision', f'{person} Hit(h) or Stand(s):')
        if choice == 'h':
            pen.color("green")
            pen.goto(xaxis, yaxis)
            pen.write(f'{person_cards} : {sum(person_score)}')
            deal_card(person_cards)
            add_to_score(person_cards, person_score)
            pen.color("black")
            pen.write(f'{person_cards} : {sum(person_score)}')
            change_x += 75
            display_face_up(xaxis+change_x, yaxis - 175, person_cards[-1])
        elif choice == 's':
            return choice
        else:
            print("Invalid Input")
            continue

    if not checked_ace:  # the function checks for ace if score exceeds 21
        ace_redemption(person_cards, person_score, xaxis, yaxis)
        decision(person, person_cards, person_score, xaxis, yaxis, True)


def dealer_logic(dlr_cards, dlr_score):
    """Dealer draws until score meets minimum or bust
    :parameter: list of dealer's cards, list of dealer's score"""
    change_x = 0    # for displaying purposes (avoids new card blocking another card)
    while sum(dlr_score) < 17:
        change_x += 75
        pen.color("green")
        pen.goto(-325, 150)
        pen.write(f'{dlr_cards} : {sum(dlr_score)}')
        deal_card(dlr_cards)
        add_to_score(dlr_cards, dlr_score)
        pen.color("black")
        pen.write(f'{dlr_cards} : {sum(dlr_score)}')
        display_face_up(-250+change_x, 25, dlr_cards[-1])


def ace_redemption(person_cards, person_score, xaxis, yaxis):
    """When person exceeds 21, this function checks for an ace in deck and changes the first ace's value
    :parameter: list of person's cards, list of person's score
                display on x-axis, display on y-axis"""
    if sum(person_score) > 21:
        for i in range(len(person_cards)):
            if 'A' in person_cards[i][0]:
                pen.color("green")
                pen.goto(xaxis, yaxis)
                pen.write(f'{person_cards} : {sum(person_score)}')
                person_score[i] = 1
                pen.color("black")
                pen.write(f'{person_cards} : {sum(person_score)}')
                break


def filter_scores(pl1_score, pl2_score, dlr_score):
    """Organizes scores into a list, for single player script: player 2's list will be empty
                                    if a player bust (>21) their respective list will be empty
    :parameter: list of player's score, list of player 2's score, list of dealer's score"""
    scores = [sum(pl1_score), sum(pl2_score), sum(dlr_score)]
    filtered = [[], [], []]
    for i in range(len(scores)):
        if scores[i] <= 21:
            filtered[i].append(scores[i])
    return filtered


def interpret_outcome(person, person_final_score, dlr_score, outcome):
    """Compares each player's score, with dealer's
    :parameter: player, list of player's score using filter_scores return
                list of dealer's score using filter_scores return, list of outcome"""
    if bool(person_final_score):
        if sum(person_final_score) == sum(dlr_score):
            outcome.append(person + " draws")
        elif sum(person_final_score) > sum(dlr_score):
            outcome.append(person + " wins")
        else:
            outcome.append(person + " lost")
    else:
        outcome.append(person + " busted")


def deal_hand(person_cards, person_score):
    """For repetition purposes: comprised of deal_card(), add_to_score functions
   :parameter:list of person's cards, list of person's score """
    deal_card(person_cards)
    add_to_score(person_cards, person_score)


def player_choice(player, player_cards, player_score, xaxis, yaxis):
    """For repetition purposes: comprised of decision() function, other displaying
    :parameter: player, list of player's cards, list of player's score
                display on x-axis, display on y-axis"""
    print("\n" + player + "'s turn")
    print(player_cards, ":", sum(player_score))
    decision(player, player_cards, player_score, xaxis, yaxis)


def dealer_behavior(dlr_cards, dlr_score):
    """For repetition purposes: comprised of conditions and dealer_logic() function
    :parameter: list of dealer's cards, list of dealer's score"""
    if sum(dlr_score) < 17:
        dealer_logic(dlr_cards, dlr_score)
    if sum(dlr_score) > 21:
        ace_redemption(dlr_cards, dlr_score, -325, 150)
        dealer_logic(dlr_cards, dlr_score)


def get_bet(player, player_pocket):
    """Prompts user to input bet
    :parameter: player, list of player's money"""
    player_bet = ""
    while player_bet == "":
        try:  # accepts only integer values
            player_bet = int(turtle.textinput("Player 1 Bet", player + " Enter bet (integer value only): "))
            if player_bet > player_pocket:
                print(f'You do not have enough money to bet {player_bet}')
                player_bet = ''
        except ValueError:
            print("Invalid input!")
    return player_bet


def player_earnings(player_outcome, player_bet, player_pocket):
    """Adds or subtracts money according to outcome
    :parameter: player's list of outcome, player's bet, player's money"""
    if (player_outcome.split(" "))[-1] == "wins":
        player_pocket += player_bet
    elif (player_outcome.split(" "))[-1] == "draws":
        player_pocket = player_pocket
    else:
        player_pocket -= player_bet
    return player_pocket


def count_win(player_outcome):
    return bool((player_outcome.split(" "))[-1] == "wins")


def display_hand(person, person_cards, person_score, xaxis, yaxis):
    """For displaying purposes
    :parameter: person, list of person's cards, list of person's score
                display on x-axis, display on y-axis"""
    pen.goto(xaxis, yaxis)
    pen.write(person + "'s cards", font=("", 9, "bold"))
    pen.goto(xaxis, yaxis-25)
    pen.write(f'{person_cards} : {sum(person_score)}')


def display_dealer_initial_card(dealer_cards):
    """For displaying purposes: displays dealer's initial card
    :parameter: dealer's cards"""
    pen.goto(-325, 175)
    pen.write("Dealer initial card:", font=("", 9, "bold"))
    pen.goto(-325, 150)
    pen.write(f'{dealer_cards[0]}')


def sinplay_write_stats(pl1_wins, pl1_pocket):
    """For displaying purposes: displays player(s) standings
    :parameter: player's wins, player's money"""
    pen.penup()
    pen.goto(175, 300)
    pen.write("PLAYER".ljust(0) + "WINS".center(20) + "MONEY".rjust(1), font=("", 9, "bold"))
    pen.goto(175, 275)
    pen.write(player1.ljust(0) + str(pl1_wins).center(20) + str(pl1_pocket).rjust(3), font=("", 9, ""))


def twoplay_write_stats(pl1_wins, pl1_pocket, pl2_wins, pl2_pocket):
    """For displaying purposes: displays player(s) standings
    :parameter: player's wins, player's money"""
    pen.penup()
    pen.goto(175, 300)
    pen.write("PLAYER".ljust(0) + "WINS".center(20) + "MONEY".rjust(1), font=("", 9, "bold"))
    pen.goto(175, 275)
    pen.write(player1.ljust(0) + str(pl1_wins).center(20) + str(pl1_pocket).rjust(3), font=("", 9, ""))
    pen.goto(175, 250)
    pen.write(player2.ljust(0) + str(pl2_wins).center(20) + str(pl2_pocket).rjust(3), font=("", 9, ""))


def get_character(card):
    """For displaying purposes: gets symbols to print for face up card
    :parameter: specific card"""
    card_val = card.split(" ")
    face = card_val[0]
    suit = suits[card_val[-1]]
    return suit, face


def display_face_down(x, y):
    """For displaying purposes: displays a face down card
    :parameter: display on x-axis, display on y-axis"""
    t.goto(x, y)
    t.down()
    t.fillcolor("indian red")
    t.begin_fill()
    for i in range(2):  # creates a rectangle
        t.forward(wi)
        t.left(90)
        t.forward(le)
        t.left(90)
    t.end_fill()
    t.up()


def display_face_up(x, y, card):
    """For displaying purposes: displays a face up card with symbols
    :parameter: display on x-axis, display on y-axis"""
    suit, face = get_character(card)
    t.goto(x, y)
    t.down()
    t.fillcolor("ivory")
    t.begin_fill()
    for i in range(2):  # creates a rectangle
        t.forward(wi)
        t.left(90)
        t.forward(le)
        t.left(90)
    t.end_fill()
    t.up()
    # writes symbols on card
    t.goto(x+8, y)
    t.write(face, font=("", 14, ""))
    t.goto(x+wi-18, y+le-20)
    t.write(face, font=("", 14, ""))
    t.goto(x+wi-11-wi/3-2, y+le-20-le/2+8)
    t.write(suit, font=("", 14, ""))


def two_player_script():
    """Algorithm to follow if there is two users"""
    outcome = []
    terminate = ''
    create_deck(4)
    pl1_pocket = 1000
    pl1_wins = 0
    pl2_pocket = 1000
    pl2_wins = 0
    while terminate != 'q':
        twoplay_write_stats(pl1_wins, pl1_pocket, pl2_wins, pl2_pocket)
        pl1_bet = get_bet(player1, pl1_pocket)
        pl2_bet = get_bet(player2, pl2_pocket)
        dlr_cards = []
        dlr_score = []
        pl1_cards = []
        pl1_score = []
        pl2_cards = []
        pl2_score = []

        # deals first two cards to each person
        for i in range(2):
            deal_hand(pl1_cards, pl1_score)
            deal_hand(pl2_cards, pl2_score)
            deal_hand(dlr_cards, dlr_score)

        # Display and run game
        display_hand(player1, pl1_cards, pl1_score, -325, -50)
        display_face_up(-325, -250, pl1_cards[0])
        display_face_up(-250, -250, pl1_cards[-1])
        display_hand(player2, pl2_cards, pl2_score, -5, 5)
        display_face_up(-5, -195, pl2_cards[0])
        display_face_up(70, -195, pl2_cards[-1])
        display_dealer_initial_card(dlr_cards)
        display_face_up(-325, 25, dlr_cards[0])
        display_face_down(-250, 25)
        player_choice(player1, pl1_cards, pl1_score, -325, -75)
        player_choice(player2, pl2_cards, pl2_score, -5, -20)
        pen.color("green")
        display_dealer_initial_card(dlr_cards)
        pen.color("black")
        display_hand("Dealer", dlr_cards, dlr_score, -325, 175)
        display_face_up(-250, 25, dlr_cards[-1])
        dealer_behavior(dlr_cards, dlr_score)

        # result after game
        final_score = filter_scores(pl1_score, pl2_score, dlr_score)
        interpret_outcome(player1, final_score[0], final_score[-1], outcome)
        interpret_outcome(player2, final_score[1], final_score[-1], outcome)
        pl1_pocket = player_earnings(outcome[-2], pl1_bet, pl1_pocket)
        pl1_wins += count_win(outcome[-2])
        pl2_pocket = player_earnings(outcome[-1], pl2_bet, pl2_pocket)
        pl2_wins += count_win(outcome[-1])

        # adds cards to playing deck
        if len(shoeDeck) < 104:
            create_deck(2)
        pen.goto(125, 200)
        pen.write(outcome[-2:], font=("", 9, "bold"))  # displays outcome
        # if one of the user runs out of money game ends
        if pl1_pocket <= 0 or pl2_pocket <= 0:
            turtle.textinput("GAME OVER", "Enter any key to view results")
            pen.clear()
            t.clear()
            break
        terminate = turtle.textinput("Quit", "Enter q to quit // Enter any key to continue")
        pen.clear()
        t.clear()
    twoplay_write_stats(pl1_wins, pl1_pocket, pl2_wins, pl2_pocket)  # displays final standings


def single_player_script():
    """Algorithm to follow if there is only one user"""
    outcome = []
    create_deck(4)
    pl1_pocket = 1000
    pl1_wins = 0
    terminate = ''
    while terminate != 'q':
        sinplay_write_stats(pl1_wins, pl1_pocket)
        pl1_bet = get_bet(player1, pl1_pocket)
        dlr_cards = []
        dlr_score = []
        pl1_cards = []
        pl1_score = []
        pl2_score = []

        # deals first two cards to each person
        for i in range(2):
            deal_hand(pl1_cards, pl1_score)
            deal_hand(dlr_cards, dlr_score)

        # Display and run game
        display_hand(player1, pl1_cards, pl1_score, -325, -50)
        display_face_up(-325, -250, pl1_cards[0])
        display_face_up(-250, -250, pl1_cards[-1])
        display_dealer_initial_card(dlr_cards)
        display_face_up(-325, 25, dlr_cards[0])
        display_face_down(-250, 25)
        player_choice(player1, pl1_cards, pl1_score, -325, -75)
        pen.color("green")
        display_dealer_initial_card(dlr_cards)
        pen.color("black")
        display_hand("Dealer", dlr_cards, dlr_score, -325, 175)
        display_face_up(-250, 25, dlr_cards[-1])
        dealer_behavior(dlr_cards, dlr_score)

        # result after game
        final_score = filter_scores(pl1_score, pl2_score, dlr_score)
        interpret_outcome(player1, final_score[0], final_score[-1], outcome)
        pl1_pocket = player_earnings(outcome[-1], pl1_bet, pl1_pocket)
        pl1_wins += count_win(outcome[-1])

        # adds cards to playing deck
        if len(shoeDeck) < 104:
            create_deck(2)
        pen.goto(125, 200)
        pen.write(outcome[-1:], font=("", 9, "bold"))
        # if user runs out of money
        if pl1_pocket <= 0:
            turtle.textinput("GAME OVER", "Enter any key to view results")
            pen.clear()
            t.clear()
            break
        terminate = turtle.textinput("Quit", "Enter q to quit // Enter any key to continue")
        pen.clear()
        t.clear()
    sinplay_write_stats(pl1_wins, pl1_pocket)


# setting screen
screen = turtle.Screen()
screen.bgcolor("green")
pen = turtle.Turtle()
pen.hideturtle()
t = turtle.Turtle()
t.hideturtle()
t.speed(0)
t.up()

# card's width and length
wi = 62
le = wi*1.618

num_pla = ''
while num_pla == "":
    try:
        num_pla = int(turtle.textinput("Number of Player", "How many players 1(1) or 2(2) : "))
        if num_pla == 1:
            player1 = turtle.textinput("Player 1 Name", "Enter a Name for Player 1: ")
            single_player_script()
            turtle.textinput("Quit", "Enter any key to exit")
            turtle.bye()
        elif num_pla == 2:
            player1 = turtle.textinput("Player 1 Name", "Enter a Name for Player 1: ")
            player2 = turtle.textinput("Player 2 Name", "Enter a Name for Player 2: ")
            two_player_script()
            turtle.textinput("Quit", "Enter any key to exit")
            turtle.bye()
        else:
            print("Invalid Input enter '1' or '2'")
            num_pla = ""
    except ValueError:
        print("Invalid input enter '1' or '2'")