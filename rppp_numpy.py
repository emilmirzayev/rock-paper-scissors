import random
import numpy as np

RESULTS = {"RR": 0, "SS": 0, "PP":0, "RS": 1, "RP":-1, "SR": -1, "SP": 1, "PR": 1, "PS": -1}
CHOICES = ["R", "P", "S"]
# HISTORY_LENGTH = 10

class AI:

    """Simple AI class which uses Markov chaing and probability to guess the next move of the user"""

    def __init__(self):

        self.gamesPlayed = 0
        self.lastUserMove = ""
        self.lastGameResult = ""
        self.prediction = ""
        self.move = ""
        self.history = []                      # Generating some values to fill the transition matrix. Non-relevant
        self.M = np.array([[1/3, 1/3, 1/3],                              # Initial transition matrix. All outcomes are equally probable
                  [1/3, 1/3, 1/3],
                  [1/3, 1/3, 1/3]])
        self.move_dict = {"R": 0, "P": 1, "S": 2}               # Used for mapping purposes
        self.reverse_move_dict = {0 : "R", 1: "P", 2: "S"}      # Used for mapping purposes
        self.winCount = 0
        self.lostCount = 0
        self.tieCount = 0
    
    def process_move(self, userMove):

        # Remember past user moves
        move_as_int = self.move_dict[userMove]
        self.history.append(move_as_int)


    def update_transition_matrix(self):               # Update the transition matrix based on user move history
            
            transitions = self.history

            tempM = np.zeros((3,3))

            for (i,j) in zip(transitions,transitions[1:]):
               tempM[i, j] += 1

            # now convert to probabilities:
            self.M = tempM / tempM.sum(axis = 1)
            print(self.M)
            return self.M

    def predict(self):                                           # Predicting the users next move based on users last move
        if self.lastUserMove == "R":
            self.prediction = self.reverse_move_dict[self.M[0].argmax()]
        elif self.lastUserMove == "P":
            self.prediction = self.reverse_move_dict[self.M[1].argmax()]
        elif self.lastUserMove == "S":
            self.prediction = self.reverse_move_dict[self.M[2].argmax()]
        else:
            self.prediction = random.choice(CHOICES)
    
    
    def make_move(self):                                         # Making a move based on prediction
        if self.prediction == "R":
            self.move = "P"
        elif self.prediction == "P":
            self.move = "S"
        else:
            self.move = "R"


class User:
    
    """
    Simple user agent does mostly nothing except moves
    """

    def __init__(self, name):
        self.name = name
        print("Hi, {}".format(self.name))
    
    def make_move(self):
        move = input("Plase, make a move selecting one of: R, P, S >>> ").upper()
        self.move = move




ai = AI()

# Testing the algorithm on dummy user which has biased decision making. AI will soon adapt itself to playstyle
def main():
    for i in range(2):
        user_move = np.random.choice(CHOICES, p = [0.03, 0.28, 0.69])
        
        ai.predict()
        ai.make_move()
        ai_move = ai.move
        result = user_move + ai_move
        if RESULTS[result] == 0:
            print("Game is tie")
            ai.tieCount += 1
        elif RESULTS[result] == 1:
            print("User won")
            ai.lostCount += 1
        else:
            print("AI won")
            ai.winCount += 1
        ai.gamesPlayed += 1
        ai.process_move(user_move)
        ai.update_transition_matrix()                   # Adding this manually so that, we can have a custom game :)
        ai.lastUserMove = user_move

    print("Games played", ai.gamesPlayed, " Games won", ai.winCount)
    print("Transition matrix \n")
    for row in ai.M: print(' '.join('{0:.2f}'.format(x) for x in row))


if __name__ == "__main__":
    main()
