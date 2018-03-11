from itertools import combinations

from cards import CardsAgainstHumanity
from cards import Player
from test import predict_batch
import sys
import numpy as np

class AIPlayer:
    def get_combos(self, black_card, blanks, numOptions, white_cards):
        variables = []

        for i in range(numOptions):
            variables.append(i+1)

        if (blanks > 1):
            return list(combinations(variables, blanks))
        else:
            return variables



    def make_funny(self, sentences, combos):
        humor_prediction = predict_batch(sentences)
        print("")
        for i in range(len(sentences)):
            print(sentences[i] + " -> " + str(humor_prediction[i]))
        print("")

        funniest_sentence = np.argmax(humor_prediction)

        if (type(combos[funniest_sentence]) == type(1)):
            length = 1
        else:
            length = len(combos[funniest_sentence])

        if (length <= 1):
            chosen = "The agent chose card "
        else:
            chosen = "The agent chose cards "

        chosen += str(combos[funniest_sentence])

        print(chosen + ". This resulted in the following:")


        print(sentences[funniest_sentence])
        print("")

def ai_game(game):
    player = AIPlayer()
    numOptions = game.get_num_options()
    going = True

    # while going == True:
    sentences = []
    blanks = game.run_AI_turn(numOptions)

    combos = player.get_combos(game.get_chosen_black(), blanks, numOptions, game.get_options())

    print("COMBOS: ", combos)
    print("")
    for i in range(len(combos)):
        sentence = game.insert_whites(blanks, combos[i])
        sentences.append(sentence)

    # for i in range(len(sentences)):
    #     print(sentences[i])
    #     print("")
    player.make_funny(sentences, combos)

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
    while going == True:
        print("---------- " + playerNames[playerTurn] + " should choose a card. ----------")
        going = game.runTurn(players[playerTurn])
        playerTurn = (playerTurn+1) % len(players)
    #ai_game(game)


if __name__ == '__main__':
    main()