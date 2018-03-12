from cards import CardsAgainstHumanity
from cards import Player
from test import predict_batch
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
    numHumans = 1 if len(sys.argv) == 1 else min(4, int(sys.argv[1]))
    numAIs = 1
    numOptions = game.get_num_options()
    whiteDeck = game.get_white_deck()
    players = []
    for i in range(numHumans):
        players.append(Player(i, numOptions, False))
    for i in range(numAIs):
        players.append(Player(i+numHumans, numOptions, True))
    for player in players:
        player.makeHand(numOptions, whiteDeck)
    return players

def main():
    game = CardsAgainstHumanity()
    #we cap the number of human players at 4
    players = makePlayers(game)
    going = True
    playerTurn = 0
    playerNames = ["Player " + str(i + 1) for i in range(len(players))]
    choices = []
    while going == True:
        print("---------- " + playerNames[playerTurn] + " should choose a card. ----------")
        player = players[playerTurn]
        choice = ai_game(game, player) if player.isAI() else game.runTurn(player)
        playerTurn = (playerTurn+1) % len(players)
        persist = input("Play again? (y/n)\n")
        going = True if persist == "y" else False
    #ai_game(game)


if __name__ == '__main__':
    main()