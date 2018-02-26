#cards.py
from random import *
from copy import *
import sys

def main():
	questions = open('against-humanity/questions.txt').readlines()
	answers = open('against-humanity/answers.txt').readlines()
	blackDeck = [question[:-1] for question in questions]
	whiteDeck = [answer[:-1] for answer in answers]
	numOptions = getOptions(blackDeck, whiteDeck)
	going = True
	while going == True:
		going = runTurn(numOptions, blackDeck, whiteDeck)

def runTurn(numOptions, blackDeck, whiteDeck):
	currentDeck = deepcopy(whiteDeck)
	options = []
	chosenBlack = blackDeck[randrange(0, len(blackDeck))]
	print("Black card:", chosenBlack)
	print("Which option best completes the blank?")
	for i in range(numOptions):
		numCards = len(whiteDeck)
		if numCards == 0:
			print("The deck is empty.")
			break
		else:
			index = randrange(0, len(whiteDeck) - i)
			options.append(currentDeck.pop(index))
	for i in range(len(options)):
		print("Option " + str(i+1) + ": " + options[i])
	blanks = chosenBlack.count('_')
	if blanks == 0:
		choice = getChoice(numOptions, [])
		insertion = options[int(choice) - 1].upper()
		result = chosenBlack + ' ' + insertion
	else:
		result = chosenBlack
		priorChoices = []
		for i in range(blanks):
			choice = getChoice(numOptions, priorChoices)
			priorChoices.append(choice)
			blank = result.find('_')
			goodPhrase = options[int(choice) - 1].upper()
			insertion = goodPhrase[:-1] if goodPhrase[-1] == "." and blank >= 0 \
			 else goodPhrase
			result = result[:blank] + insertion + result[blank + 1:]
	if result[-1] not in "?!.":
		result += "."
	print(result)
	persist = input("Play again? (y/n)\n")
	going = True if persist == "y" else False
	return going

def getChoice(numOptions, priorChoices):
	invalid = True
	while invalid == True:
		choice = input("Which number card would you like to play?\n")
		if choice == "n" or choice == "q":
			exit()
		try:
   			check = int(choice)
		except ValueError:
   			print("Please input an integer between 1 and " + str(numOptions) + ".")
   			return getChoice(numOptions, priorChoices)
		if int(choice) - 1 not in range(numOptions):
			print("Invalid choice.") 
			return getChoice(numOptions, priorChoices)
		elif choice in priorChoices:
			print("You cannot select the same card twice.")
			return getChoice(numOptions, priorChoices)
		else:
			invalid = False
		return choice

def getOptions(blackDeck, whiteDeck):
	try:
		numOptions = 7 if len(sys.argv) == 1 else \
		min(max(int(sys.argv[1]), 7), len(whiteDeck))
	except ValueError:
		numOptions = len(whiteDeck) if sys.argv[1] == "ALL" else 7
	return numOptions

if __name__ == '__main__':
	main()