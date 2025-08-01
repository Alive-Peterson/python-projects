import math
import random

class Player:
    def __init__(self,letter):
        # letter can be x or o
        self.letter=letter

    def get_move(self,game):
        pass

class RandomComputerPlayer(Player):
    def __init__(self, letter):
        super().__init__(letter)

    def get_move(self, game):
        square=random.choice(game.available_moves())
        return square

class HumanPlayer(Player):
    def __init__(self, letter):
        super().__init__(letter)

    def get_move(self, game):
        valid_square=False
        val=None
        while not valid_square:
            square=input(self.letter + '\'s turn. Input move (0-8):')
            # we are going to check that it's a correct value by trying to cast it as an integer
            # and if it's not its invalid and if that spot is not available on the board we also say it's invalid
            try:
                val=int(square)
                if val not in game.available_moves():
                    raise ValueError
                valid_square=True #if these are successfull, then good
            except ValueError:
                print('Invalid square, Try again')
            
        return val
    
class GeniusComputerPlayer(Player):
    def __init__(self,letter):
        super().__init__(letter)

    def get_move(self,game):
        if len(game.available_moves())==9:
            square=random.choice(game.available_moves()) #it chooses a square randomly
        else:
            #gets the square based on minimax algorithm 
            square=self.minimax(game,self.letter)['position']
        return square
    
    def minimax(self,state,player):
        max_player=self.letter #the human player - us
        other_player='o' if player =='x' else 'x' #other player

        #we want to check if the previous move is a winner

        if state.current_winner==other_player:
        # we should return position and score to keep track of the stats of the players
        # for minimax to work
            return {'position':None,
                    'score':1*(state.num_empty_squares() + 1) if other_player == max_player else -1 * (
                        state.num_empty_squares() + 1)
                    }
        elif not state.empty_squares(): #no empty scores
            return {'position':None,'score':0}
        
        if player==max_player:
            best= {'position':None,'score':-math.inf} #each score should be larger (maximize)
        else:
            best= {'position':None,'score':math.inf} #each score should minimize

        for possible_move in state.available_moves():
            #step1: make a move, try that spot
            state.make_move(possible_move,player)

            #step2: recurse using minimax, to stimulate a game after making a move
            sim_score=self.minimax(state,other_player)

            #step3:undo the move
            state.board[possible_move]=' '
            state.current_winner=None
            sim_score['position']=possible_move

            #step4:update the dictionaries if necessary
            if player==max_player:  #we are trying to maximize the max_player
                if sim_score['score']>best['score']:
                    best=sim_score #replace best
            else:
                if sim_score['score']<best['score']:
                    best=sim_score #replace best
        return best
        
