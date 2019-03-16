import random
import numpy as np

from itertools import combinations, product, tee
import time



class AI:

    """Simple AI class which uses Markov chaing and probability to guess the next move of the user"""

    def __init__(self):

        self.gamesPlayed = 0
        self.lastUserMove = ""
        self.lastGameResult = ""
        self.prediction = ""
        self.move = ""
        self.history = []                      

        self.moveDict = {"R": 0, "P": 1, "S": 2}               # Used for mapping purposes
        self.reverseMoveDict = {0 : "R", 1: "P", 2: "S"}      # Used for mapping purposes
        self.winCount = 0
        self.lostCount = 0
        self.tieCount = 0
        self.difficulty = int(input("""Please, choose the game difficulty via typing the corresponding digit: \n
- 1 for Easy mode \n
- 2 for Normal mode \n
- 3 for Hard mode \n 
-> """))
        if self.difficulty == 2:
            self.M = [[1/3, 1/3, 1/3],                              
                  [1/3, 1/3, 1/3],
                  [1/3, 1/3, 1/3]]
        elif self.difficulty == 3:
            self.M = np.zeros((9, 3), dtype = float)
    
    def _process_move(self, userMove):

        # Remember past user moves
        move_as_int = self.moveDict[userMove]
        self.history.append(move_as_int)
        self.lastUserMove = userMove
        self._update_transition_matrix()
        
    def _update_transition_matrix(self):
        """Update the transition matrix based on the game difficulty.
        
        Based on game difficulty two type of matrices can be calculated:
            1. For difficulty 1, Easy, initial matrix will not be changed and will be left as it is
            1. For difficulty 2, Normal, first order transition matrix will be calculated
            2. For difficulty 3, Hard, second order transition matrix will be calculated
        For calculating the second order transition matrix, move history should be greater than 2
        """
        if self.difficulty == 1:
            pass
        elif self.difficulty == 2:
            self._transition_matrix_first_order()
        elif self.difficulty == 3 and len(self.history) >= 3:
            self._transition_matrix_sec_order()
        


    def _transition_matrix_first_order(self):
            
            sequence = self.history

            self.M = [[0] * 3 for _ in range(3)]

            for (i,j) in zip(sequence, sequence[1:]):
                self.M[i][j] += 1

            # now convert to probabilities:
            for row in self.M:
                s = sum(row)
                if s > 0:
                    row[:] = [f/s for f in row]
            return self.M

   
    def _transition_matrix_sec_order(self):
        
        sequence = self.history
        M = np.zeros((len(sequence)**2, len(sequence)))
        permutations = list(product(sequence, repeat=2))

        def triplewise(iterable):
            a, b, c = tee(iterable, 3)
            next(b)
            next(c); next(c)
            return zip(a, b, c)
    

        for a, b, c in triplewise(sequence):
            prev_two = (a, b)
            M[permutations.index(prev_two)][c] += 1

        M = np.nan_to_num(M / M.sum(axis = 1, keepdims= True))

        return M


    def _predict(self):
        if self.difficulty == 2:
            self._prediction_first_order
        elif self.difficulty == 3:
            self._prediction_second_order
            
            
    def _prediction_first_order(self):
        # Predicting the users next move based on users last move
        if self.lastUserMove == "R":
            self.prediction = self.reverseMoveDict[self.M[0].index(max(self.M[0]))]
        elif self.lastUserMove == "P":
            self.prediction = self.reverseMoveDict[self.M[1].index(max(self.M[1]))]
        elif self.lastUserMove == "S":
            self.prediction = self.reverseMoveDict[self.M[2].index(max(self.M[2]))]
        else:
            self.prediction = random.choice(Game.CHOICES)

    def _prediction_second_order(self):
        indexList = list(map(lambda a: str(a[0] + a[1]), list(product("RPS", repeat = 2))))
        self.prediction = self.reverseMoveDict[self.M[indexList.index(self.lastUserMove)].argmax()]

    # TODO add functionality for keeping history of 2 moves
   

    
    
    def _make_move(self):
        """Makes move based on predicted user move. If game difficulty is 1, then it will randomly make a move
        based on move choices
        """
        if self.difficulty == 1:
            self.move = random.choice(Game.CHOICES)                                         # Making a move based on prediction
        elif self.prediction == "R":
            self.move = "P"
        elif self.prediction == "P":
            self.move = "S"
        else:
            self.move = "R"

class User:
    
    """
    Simple user agent does mostly nothing except moves
    """

    def __init__(self, ):
        self.name = input("Please, tell me your name: --> ")
        print("Hi, {}!".format(self.name))
    
    def _make_move(self):
        move = input("Plase, make a move selecting one of: R, P, S >>> ").upper()
        self.move = move


class Game:
    """
    Game class object. Has the information about the state of the game.
    Attributes are:
        - difficulty
        - rounds played
        - rounds won by user
        - rounds won by computer
        ...
    """
    # class variables
    
    user = User()
    ai = AI()

    RESULTS = {"RR": 0, "SS": 0, "PP":0, "RS": 1, "RP":-1, "SR": -1, "SP": 1, "PR": 1, "PS": -1}
    CHOICES = ["R", "P", "S"]

    gameContinue = True


    def __init__(self):
        self.roundsPlayed = 0
        self.userWon = 0
        self.aiWon = 0
        self.winPercentage = {"aiWinRate": 0, "userWinRate": 0}
        self.finalMove = ""
        self.lastGameResult = 0


    def _update_win_percentage(self):
        """Updates the win percentage of AI and User based on results and rounds played.
        
        Calculates the new values and updates `winPercentage` 
        """

        if self.roundsPlayed >= 1:
            _compWinRate = (self.aiWon / self.roundsPlayed) * 100
            _userWinRate = (self.userWon / self.roundsPlayed) * 100
            self.winPercentage["aiWinRate"], self.winPercentage["userWinRate"] = _compWinRate, _userWinRate
    
    def _update_game_process(self, verbose = False):
        """General method for updating the game state
        
        Order of the processes:
            1. Asks user to make a move
            2. AI makes a move
            3. AI processes the user's move ex-post
            4. Creating the final move
            5. Gets the result (who won)
            6. Result announcment
            7. Updates the win percentage statistics
        """
        self.user._make_move()
        self.ai._predict()
        self.ai._make_move()
        print("AI chose {}". format(self.ai.move.upper()))
        self.ai._process_move(self.user.move)
        self._make_result()
        self._get_result()
        self._announce_round_results()
        self._update_win_percentage()
        if self.roundsPlayed % 10 == 0:
            self._ask_for_continuation()

    def _make_result(self):
        """Generate a final move from the moves of the user and AI
        
        Does not return anything
        """
        self.finalMove = self.user.move + self.ai.move
    
    def _get_result(self):
        """Gets the result from the result dictionary based on the final move
        
        Does not return anything
        """
        self.lastGameResult = self.RESULTS[self.finalMove]

    
    def _announce_round_results(self):
        """Announces the result on command line and makes subsequent changes to game state
        
        1. Increments the number of rounds played
        2. Increments the win counts

        Does not return anything
        """
        self.roundsPlayed += 1
        if self.lastGameResult == 0:
            print("Game is tie. No one wins")
        elif self.lastGameResult == 1:
            print("User won the game! Congrats!")
            self.userWon += 1
        else:
            print("AI won *insert T900 gif here*")
            self.aiWon += 1
    
    def _announce_game_results(self):
        print()
        print("Game has ended! It either happened because you decided so,\n or it is enough playing and time to get back to reality!")
        print("-" * 20)
        print("From {} games played, {} won {} times and AI won {} times!".format(self.roundsPlayed, self.user.name, self.userWon, self.aiWon))
        print("Your win percentage is {}".format(self.winPercentage["userWinRate"]))
        print("AI win percentage is {}".format(self.winPercentage["aiWinRate"]))

    
    def _ask_for_continuation(self):
        to_continue = input("Do you want to play another 10 rounds? Answer y for Yes and n for No --> (y/n) ")
        if to_continue == "n":
            self.gameContinue = False
        elif to_continue == "y":
            self.gameContinue = True
        else:
            raise Exception("You had one job! \nTo select either 'y' for Yes and 'n' for No")



oyun = Game()

for i in range(20):
    oyun._update_game_process()
print(oyun.ai.M)