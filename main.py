from itertools import combinations

from cards import CardsAgainstHumanity
from test import predict_batch
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


def main():
    game = CardsAgainstHumanity()

    ai_game(game)


if __name__ == '__main__':
    main()