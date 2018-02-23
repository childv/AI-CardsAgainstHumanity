#cards.py
from random import *
from copy import *
import sys

def main():
	questions = open('against-humanity/questions.txt').readlines()
	answers = open('against-humanity/answers.txt').readlines()
	blackDeck = [question[:-1] for question in questions]
	whiteDeck = [answer[:-1] for answer in answers]
	going = True
	while going == True:
		chosenBlack = blackDeck[randrange(0, len(blackDeck))]
		numOptions = 5 if len(sys.argv) == 1 else int(sys.argv[1])
		currentDeck = deepcopy(whiteDeck)
		options = []
		print("Black card:", chosenBlack)
		print("Which option best completes the blank?")
		for i in range(numOptions):
			numCards = len(whiteDeck)
			if numCards == 0:
				print("The deck is empty.")
				break
			else:
				index = randrange(0, len(whiteDeck))
				options.append(currentDeck.pop(index))
		for i in range(len(options)):
			print("Option " + str(i+1) + ": " + options[i])
		invalid = True
		while invalid == True:
			choice = input("Which number card would you like to play?\n")
			if int(choice) - 1 in range(numOptions):
				invalid = False
			else:
				print("Invalid choice.") 
		blank = chosenBlack.find('_')
		goodPhrase = options[int(choice) - 1].upper()
		insertion = goodPhrase[:-1] if goodPhrase[-1] == "." and blank >= 0 \
		 else goodPhrase
		if blank == -1:
			result = chosenBlack + ' ' + insertion
		else:
			result = chosenBlack[:blank] + insertion + chosenBlack[blank + 1:]
		print(result)
		persist = input("Play again? (y/n)\n")
		going = True if persist == "y" else False



if __name__ == '__main__':
	main()