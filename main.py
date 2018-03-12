from cards import CardsAgainstHumanity
from cards import Player
from test import predict_batch
from random import shuffle
import sys
import numpy as np

def ai_game(game, player):
    numOptions = game.get_num_options()
    sentences = []
    deck = game.get_current_deck()
    hand = player.getHand()
    blanks = game.run_AI_turn(hand)
    combos = player.get_combos(game.get_chosen_black(), blanks, numOptions, game.get_options())
    for i in range(len(combos)):
        sentence = game.insert_whites(blanks, hand, combos[i])
        sentences.append(sentence)
    return player.make_funny(sentences, combos, player, deck)

def makePlayers(game): 
    numHumans = 2 if len(sys.argv) == 1 else max(2, min(5, int(sys.argv[1])))
    numAIs = 1
    numOptions = game.get_num_options()
    whiteDeck = game.get_white_deck()
    players = []
    for i in range(numHumans):
        players.append(Player(i+1, numOptions, False))
    for i in range(numAIs):
        players.append(Player(i+numHumans+1, numOptions, True))
    for player in players:
        player.makeHand(numOptions, whiteDeck)
    return players

def chooseBest(playerWithBlack, choices):
    shuffle(choices)
    print("The results are in! In no particular order: ")
    for i in range(len(choices)):
        print ("Option " + str(i+1) + ": " + choices[i][1])
    choice = input("Player " + str(playerWithBlack.getNum()) + ", what is the funniest option?\n")
    try:
        check = int(choice)
    except ValueError:
        print("Please input an integer between 1 and " + str(len(choices)) + ".")
        return chooseBest(playerWithBlack, choices)
    choice = int(choice)
    if choice - 1 not in range(len(choices)):
        print("Please input an integer between 1 and " + str(len(choices)) + ".")
        return self.getChoice(hand, priorChoices, choice)
    return choices[choice-1][0]

def showScores(players):
    for player in players:
        playerName = "Player " + str(player.getNum())
        if player.isAI():
            playerName += " (AI)"
        print(playerName + ":", player.getScore(), "points.")
        print(playerName, "won cards:", player.getWonCards())
    print("Thanks for playing!")

def runRound(game, players, playerTurn):
    playerWithBlack = players[playerTurn]
    playersWhoChoose = [p for p in players if p is not playerWithBlack]
    game.get_black_card()
    print("\n\n\n\n\n---------- NEW ROUND ----------")
    blackPlayerNum = str(playerWithBlack.getNum())
    input("Player " + blackPlayerNum + ", press return to draw a black card.")
    print("Player " + blackPlayerNum + " drew this card:")
    print(game.get_chosen_black())
    choices = []
    for player in playersWhoChoose:
        playerNum = str(player.getNum())
        AI = player.isAI()
        print("\n---------- Player " + playerNum + " should choose a card. ----------")
        if not AI:
            input("Player " + playerNum + ", press return when you're ready.")
        choice = ai_game(game, player) if AI else game.runTurn(player)
        choices.append((player.getNum(), choice))
        print("\n\n\n\n")
    playerWhoWins = chooseBest(playerWithBlack, choices)
    print("The card " + game.get_chosen_black() + " goes to player " + str(playerWhoWins) + "!")
    players[playerWhoWins-1].raiseScore(game.get_chosen_black())

def main():
    game = CardsAgainstHumanity()
    #we cap the number of human players at 4
    players = makePlayers(game)
    going = True
    playerTurn = 0
    while going == True:
        runRound(game, players, playerTurn)
        playerTurn = (playerTurn+1) % len(players)
        if playerTurn == 0:
            print("Now would be a fair time to stop.")
        persist = input("Play again? (y/n)\n")
        going = True if persist == "y" else False
    showScores(players)
    #ai_game(game)


if __name__ == '__main__':
    main()