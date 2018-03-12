#cards.py
from random import *
from copy import *
from itertools import combinations
from test import predict_batch
import numpy as np
import sys

class CardsAgainstHumanity:
	def __init__(self):
		self.whiteDeck = None
		self.blackDeck = None
		self.currentDeck = None
		self.chosenBlack = None
		self.options = None
		self.prepare_game()

	def set_current_deck(self, currentDeck):
		self.currentDeck = currentDeck

	def get_current_deck(self):
		return self.currentDeck

	def get_black_deck(self):
		return self.blackDeck

	def get_white_deck(self):
		return self.whiteDeck

	def set_chosen_black(self, chosenBlack):
		self.chosenBlack = chosenBlack

	def get_chosen_black(self):
		return self.chosenBlack

	def set_options(self, options):
		self.options = options

	def append_options(self, item):
		self.options.append(item)

	def get_options(self):
		return self.options

	def prepare_game(self):
		questions = open('against-humanity/questions.txt').readlines()
		answers = open('against-humanity/answers.txt').readlines()
		self.blackDeck = [question[:-1] for question in questions]
		self.whiteDeck = [answer[:-1] for answer in answers]

	def play_round(self):
		numOptions = self.getOptions()
		going = True

		while going == True:
			going = self.runTurn(numOptions)

	def get_black_card(self):
		self.set_chosen_black(self.blackDeck[randrange(0, len(self.blackDeck))])
		#print("Black card:", self.get_chosen_black())
		#print("")

	def get_white_cards(self, hand):
		for i in range(len(hand)):
			print("Option " + str(i + 1) + ": " + hand[i])

	def getChoice(self, hand, priorChoices, choice):
		invalid = True
		while invalid == True:
			if choice == "-1":
				exit()
			try:
				check = int(choice)
			except ValueError:
				print("Please input an integer between 1 and " + str(len(hand)) + ".")
				choice = input("Which number card would you like to play?\n")
				return self.getChoice(hand, priorChoices, choice)
			choice = int(choice)
			if choice - 1 not in range(len(hand)):
				print("Please input an integer between 1 and " + str(len(hand)) + ".")
				choice = input("Which number card would you like to play?\n")

				return self.getChoice(hand, priorChoices, choice)

			elif choice in priorChoices:
				print("You cannot select the same card twice.")
				choice = int(input("Which number card would you like to play?\n"))

				return self.getChoice(hand, priorChoices, choice)
			else:
				invalid = False
			return int(choice)

	def get_num_options(self):
		try:
			numOptions = 7 if len(sys.argv) == 1 else \
			min(max(int(sys.argv[1]), 7), len(self.get_white_deck()))
		except ValueError:
			numOptions = len(self.get_white_deck()) if sys.argv[1] == "ALL" else 7
		return numOptions

	def fill_in_blanks(self, blanks, player):
		places = ["first", "second", "third", "fourth"]
		hand = player.getHand()
		if blanks == 0:
			choiceInput = input("Which number card would you like to play?\n")
			choice = self.getChoice(hand, [], choiceInput)
			insertion = hand.pop(choice - 1).upper()
			result = self.get_chosen_black() + ' ' + insertion
		else:
			result = self.get_chosen_black()
			priorChoices = []
			for i in range(blanks):
				if (blanks == 1):
					choice = input("Which number card would you like to play?\n")
				else:
					choice = input("Which number card would you like to play for the " + places[i] + " blank?\n")
				choice = self.getChoice(hand, priorChoices, choice)
				priorChoices.append(choice)

				blank = result.find('_')
				goodPhrase = hand[choice - 1].upper()
				insertion = goodPhrase[:-1] if goodPhrase[-1] == "." and blank >= 0 \
					else goodPhrase
				result = result[:blank] + insertion + result[blank + 1:]
			toRemove = [hand[choice-1] for choice in priorChoices]
			player.setHand([card for card in hand if card not in toRemove])
		return result

	def insert_whites(self, blanks, hand, combos):
		if blanks == 0:
			insertion = hand[combos-1].upper()
			result = self.get_chosen_black() + ' ' + insertion

		else:
			result = self.get_chosen_black()
			if blanks == 1:
				length = 1
			else:
				length = len(combos)

			for i in range(length):
				if blanks == 1:
					choice = combos
				else:
					choice = combos[i]
				blank = result.find('_')
				goodPhrase = hand[choice - 1].upper()
				insertion = goodPhrase[:-1] if goodPhrase[-1] == "." and blank >= 0 \
					else goodPhrase
				result = result[:blank] + insertion + result[blank + 1:]
		return result


	def runTurn(self, player):
		self.set_current_deck(deepcopy(self.get_white_deck()))
		deck = self.get_current_deck()

		print("Which option best completes the phrase?")
		print("Black card:", self.get_chosen_black())
		hand = player.getHand()
		self.get_white_cards(hand)

		blanks = self.get_chosen_black().count('_')

		result = self.fill_in_blanks(blanks, player)
		if not blanks: 
			player.drawCard(deck)
		for i in range(blanks):
			player.drawCard(deck)
		if result[-1] not in "?!.":
			result += "."
		print(result)
		return(result)
		

	def run_AI_turn(self, hand):
		self.set_current_deck(deepcopy(self.get_white_deck()))

		#self.get_black_card()

		print("Which option best completes the phrase?")
		print("Black card:", self.get_chosen_black())
		self.get_white_cards(hand)

		return self.get_chosen_black().count('_')

class Player:
	def __init__(self, num, numCards, ai):
		self.num = num
		self.hand = []
		self.wonCards = []
		self.numCards = numCards
		self.ai = ai
		self.score = 0

	def getNum(self):
		return self.num

	def playCard(self, num):
		return self.hand.pop(num)

	def drawCard(self, deck):
		if not deck:
			print("There are no more cards!")
			finish()
		self.hand.append(deck.pop(randrange(len(deck))))

	def makeHand(self, numCards, deck):
		for i in range(numCards):
			self.drawCard(deck)

	def getHand(self):
		return self.hand

	def setHand(self, hand):
		self.hand = hand

	def isAI(self):
		return self.ai

	def raiseScore(self, blackCard):
		self.score += 1
		self.wonCards.append(blackCard)
		print("Player " + str(self.num) + "'s score has been updated.")

	def getScore(self):
		return self.score

	def getWonCards(self):
		return self.wonCards

	#ai players only
	def get_combos(self, black_card, blanks, numOptions, white_cards):
		variables = []

		for i in range(numOptions):
			variables.append(i+1)

		if (blanks > 1):
			return list(combinations(variables, blanks))
		else:
			return variables

	#ai players only
	def make_funny(self, sentences, combos, player, deck):
		hand = player.getHand()
		humor_prediction = predict_batch(sentences)
		print("")
		for i in range(len(sentences)):
			print(sentences[i] + " -> " + str(humor_prediction[i]))
		print("")
		funniest_sentence = np.argmax(humor_prediction)
		if (type(combos[funniest_sentence]) == type(1)):
			length = 1
			hand.pop(combos[funniest_sentence]-1)
			self.drawCard(deck)
		else:
			length = len(combos[funniest_sentence])
			toRemove = [hand[combo-1] for combo in combos[funniest_sentence]]
			player.setHand([card for card in hand if card not in toRemove])
			for i in range(length):
				self.drawCard(deck)

		if (length <= 1):
			chosen = "The agent chose card "
		else:
			chosen = "The agent chose cards "
		print("FUNNIEST SENTENCE", funniest_sentence)
		chosen += str(combos[funniest_sentence])
		print(chosen + ". This resulted in the following:")

		best = sentences[funniest_sentence]
		print(best)
		print("")
		return best

	def finish():
		print("The game is done")
		
def main():
	game = CardsAgainstHumanity()
	numOptions = game.get_num_options()
	going = True
	while going == True:
		going = game.runTurn(numOptions)

if __name__ == '__main__':
	main()