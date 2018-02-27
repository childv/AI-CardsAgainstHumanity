#cards.py
from random import *
from copy import *
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
		print("Black card:", self.get_chosen_black())
		print("")

	def get_white_cards(self, numOptions):
		self.set_options([])


		for i in range(numOptions):
			numCards = len(self.whiteDeck)
			if numCards == 0:
				print("The deck is empty.")
				break

			else:
				index = randrange(0, len(self.whiteDeck) - i)
				self.append_options(self.currentDeck.pop(index))

		for i in range(len(self.options)):
			print("Option " + str(i + 1) + ": " + self.options[i])

	def getChoice(self, numOptions, priorChoices, choice):
		invalid = True
		while invalid == True:
			if choice == "n" or choice == "q":
				exit()
			try:
				check = int(choice)
			except ValueError:
				print("Please input an integer between 1 and " + str(numOptions) + ".")
				choice = input("Which number card would you like to play?\n")

				return self.getChoice(numOptions, priorChoices, choice)

			if int(choice) - 1 not in range(numOptions):
				print("Invalid choice.")
				choice = input("Which number card would you like to play?\n")

				return self.getChoice(numOptions, priorChoices, choice)

			elif choice in priorChoices:
				print("You cannot select the same card twice.")
				choice = input("Which number card would you like to play?\n")

				return self.getChoice(numOptions, priorChoices, choice)
			else:
				invalid = False
			return choice

	def get_num_options(self):
		try:
			numOptions = 7 if len(sys.argv) == 1 else \
			min(max(int(sys.argv[1]), 7), len(self.get_white_deck()))
		except ValueError:
			numOptions = len(self.get_white_deck()) if sys.argv[1] == "ALL" else 7
		return numOptions

	def fill_in_blanks(self, blanks, numOptions):
		places = ["first", "second", "third", "fourth"]

		if blanks == 0:
			choice = input("Which number card would you like to play?\n")
			choice = self.getChoice(numOptions, [], choice)
			insertion = self.get_options()[int(choice) - 1].upper()
			result = self.get_chosen_black() + ' ' + insertion
		else:
			result = self.get_chosen_black()
			priorChoices = []
			for i in range(blanks):
				if (blanks == 1):
					choice = input("Which number card would you like to play?\n")
				else:
					choice = input("Which number card would you like to play for the " + places[i] + " blank?\n")

				choice = self.getChoice(numOptions, priorChoices, choice)
				priorChoices.append(choice)

				blank = result.find('_')
				goodPhrase = self.get_options()[int(choice) - 1].upper()

				insertion = goodPhrase[:-1] if goodPhrase[-1] == "." and blank >= 0 \
					else goodPhrase
				result = result[:blank] + insertion + result[blank + 1:]

		return result

	def insert_whites(self, blanks, combos):
		if blanks == 0:
			result = self.get_chosen_black() + ' ' + self.get_options()[combos-1]

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
				goodPhrase = self.get_options()[int(choice) - 1].upper()

				insertion = goodPhrase[:-1] if goodPhrase[-1] == "." and blank >= 0 \
					else goodPhrase
				result = result[:blank] + insertion + result[blank + 1:]

		return result


	def runTurn(self, numOptions):
		self.set_current_deck(deepcopy(self.get_white_deck()))

		self.get_black_card()

		print("Which option best completes the phrase?")
		self.get_white_cards(numOptions)

		blanks = self.get_chosen_black().count('_')

		result = self.fill_in_blanks(blanks, numOptions)


		if result[-1] not in "?!.":
			result += "."

		print(result)

		persist = input("Play again? (y/n)\n")
		going = True if persist == "y" else False

		return going

	def run_AI_turn(self, numOptions):
		self.set_current_deck(deepcopy(self.get_white_deck()))

		self.get_black_card()

		print("Which option best completes the phrase?")
		self.get_white_cards(numOptions)

		return self.get_chosen_black().count('_')

def main():
	game = CardsAgainstHumanity()

	numOptions = game.get_num_options()

	going = True
	while going == True:
		going = game.runTurn(numOptions)

if __name__ == '__main__':
	main()