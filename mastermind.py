# goal: code mastermind the game based on text input
# secondary goal: code an autosolver for mastermind

import random 
import copy
from typing import Sized

class Mastermind():
    def __init__(self, size, guesses, colors):
        self.size = size
        self.colors = range(1,colors+1)
        self.solution = self.makeSolution()
        self.guesses = guesses
        self.board = [[0 for i in range(self.size)] for j in range(self.guesses)]
        self.playing = True
        self.all_bagels = [[0 for i in range(self.size)] for j in range(self.guesses)]

    def makeSolution(self):
        soln = [0 for i in range(self.size)]
        for i in range(len(soln)):
            soln[i] = random.choice(self.colors)
        return soln
    
    def makeGuess(self, guess):
        self.guesses -= 1
        # evaluate guess
        bagel = self.evaluate(guess)
        # add evaluation to the board
        self.addEval(bagel)
        # add guess to the board
        self.addGuess(guess)
        # check for endgame
        self.checkEndgame(guess)
        # show the board to the player
        self.showBoard()
    
    def addGuess(self, guess): # adds guess to the board
        row = len(self.board) - self.guesses - 1
        for i in range(len(guess)):
            self.board[row][i] = guess[i]
    
    def addEval(self, bagel):
        row = len(self.all_bagels) - self.guesses - 1
        self.all_bagels[row] = bagel

    def evaluate(self, guess): # evaluates the accuracy of the guess
        # TODO REPEATS DO NOT ALWAYS WORK
        bagel = [0 for i in range(len(guess))]
        loc = 0
        color = 0
        
        see_soln = copy.deepcopy(self.solution)
        guess_check = copy.deepcopy(guess)
        for i in range(len(guess)):
            if guess[i] == self.solution[i]:
                loc += 1
                see_soln[i] = 0
                guess_check[i] = 0
        #print("frst see", see_soln)

        for i in range(len(guess)):
            if guess_check[i] != 0 and guess[i] in see_soln: 
                #print(i, guess[i], see_soln)
                color += 1
                see_soln[see_soln.index(guess[i])] = 0
                #print(i, guess[i], see_soln, color)
            #print("i = ", i, see_soln)
       

        for i in range(len(bagel)):
            if loc > 0:
                bagel[i] = 2
                loc -= 1
            elif color > 0:
                bagel[i] = 1
                color -= 1

        return bagel
    
    def showBoard(self):
        for_print = ""
        for row in range(len(self.board)):
            for i in range(len(self.board[row])):
                for_print += str(self.board[row][i]) + " "
            for_print += "  ||  "
            for i in range(len(self.all_bagels[row])):
                if self.all_bagels[row][i] != 0: for_print += str(self.all_bagels[row][i]) + " "
            #print(self.board[row], self.all_bagels[row])
            for_print += "\n"
        print(for_print)

    def checkEndgame(self, guess):
        if guess == self.solution:
            print("You solved the puzzle!")
            self.playing = False
        elif self.guesses == 0:
            print("You ran out of guesses.")
            print("The solution was ", self.solution)
            self.playing = False


class playGame():
    def __init__(self, size=4, guesses=10, colors=8):
        print("Welcome to Mastermind")
        self.size = size
        self.game = Mastermind(size, guesses, colors)
        self.makeMoves()
    
    def makeMoves(self):
        while self.game.playing == True:
            raw_guess = input("Make a new guess: ").split(" ")
            guess = list()
            allowed = True
            for i in range(len(raw_guess)):
                if int(raw_guess[i]) < 1 or int(raw_guess[i]) > len(self.game.colors): allowed = False
                if len(raw_guess[i]) > 0:
                    guess += [int(raw_guess[i])]
            if len(guess) != self.size: allowed = False
            if allowed:
                self.game.makeGuess(guess)

def play(mode="guess"):
    play = input("Would you like to play Mastermind? ")
    if mode == "guess":
        while play == "Yes" or play == "Y" or play == "y" or play == "yes":
            size = int(input("How big should each guess be? "))
            guesses = int(input("How many guesses would you like to have? "))
            colors = int(input("How many colors would you like to play with? "))
            playGame(size, guesses, colors)
            play = input("Would you like to play again? ")

    print("Thank you for playing Mastermind. Come back again soon!")

play()
