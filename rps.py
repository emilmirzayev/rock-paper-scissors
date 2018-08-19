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
        self.history = [0,1,2,0,1,2,0,1,2]                      # Generating some values to fill the transition matrix. Non-relevant
        self.M = [[1/3, 1/3, 1/3],                              # Initial transition matrix. All outcomes are equally probable
                  [1/3, 1/3, 1/3],
                  [1/3, 1/3, 1/3]]
        self.move_dict = {"R": 0, "P": 1, "S": 2}               # Used for mapping purposes
        self.reverse_move_dict = {0 : "R", 1: "P", 2: "S"}      # Used for mapping purposes
        self.winCount = 0
        self.lostCount = 0
        self.tieCount = 0
    
    def process_move(self, userMove):

        # Remember past user moves
        move_as_int = self.move_dict[userMove]
        self.history.append(move_as_int)


    def update_transition_matrix(self, n_states):               # Update the transition matrix based on user move history
            
            transitions = self.history

            self.M = [[0]*n_states for _ in range(n_states)]

            for (i,j) in zip(transitions,transitions[1:]):
                self.M[i][j] += 1

            # now convert to probabilities:
            for row in self.M:
                s = sum(row)
                if s > 0:
                    row[:] = [f/s for f in row]
            return self.M

    def predict(self):                                           # Predicting the users next move based on users last move
        if self.lastUserMove == "R":
            self.prediction = self.reverse_move_dict[self.M[0].index(max(self.M[0]))]
        elif self.lastUserMove == "P":
            self.prediction = self.reverse_move_dict[self.M[1].index(max(self.M[1]))]
        elif self.lastUserMove == "S":
            self.prediction = self.reverse_move_dict[self.M[2].index(max(self.M[2]))]
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

for i in range(1000):
    user_move = np.random.choice(CHOICES, p = [0.05, 0.05, 0.9])            # Dummy user will mostly play Paper
    
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
    
    ai.update_transition_matrix(n_states = 3)
    ai.process_move(user_move)
    ai.lastUserMove = user_move

print("Games played", ai.gamesPlayed, " Games won", ai.winCount)
print("Transition matrix \n")
for row in ai.M: print(' '.join('{0:.2f}'.format(x) for x in row))
