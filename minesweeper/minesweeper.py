import random
import re

class Board:
    def __init__(self, dim_size, num_bombs):
        self.dim_size = dim_size
        self.num_bombs = num_bombs

        self.board = self.make_new_board()
        self.assign_values_to_board()
        
        self.dug=set()

    def make_new_board(self):
       board=[[None for _ in range(self.dim_size)] for _ in range(self.dim_size)]
       bombs_planted=0
       while bombs_planted<self.num_bombs:
           loc = random.randint(0,self.dim_size**2-1) # returns a random N integer such that N>=a, N>=b
           row = loc // self.dim_size
           col = loc % self.dim_size

           if board[row][col] == '*':
               continue
           
           board[row][col] = '*'
           bombs_planted += 1
       return board
       
    def assign_values_to_board(self):

        for r in range(self.dim_size):
            for c in range(self.dim_size):
                if self.board[r][c] =='*':
                    continue
                self.board[r][c] = self.get_num_neighbouring_bombs(r,c)

    def get_num_neighbouring_bombs(self, row,col):
        num_neighbouring_bombs = 0
        for r in range(max(0, row-1), min(self.dim_size-1, row+1)+1):
            for c in range(max(0, col-1), min(self.dim_size-1, col+1)+1):
                if r == row and c == col:
                    continue
                if self.board[r][c] == '*':
                    num_neighbouring_bombs += 1
        return num_neighbouring_bombs

    def dig(self, row, col): #digging at a location based on row and column

        self.dug.add((row,col))

        if self.board[row][col] == '*':
            return False
        elif self.board[row][col] > 0:
            return True
        
        for r in range(max(0, row-1), min(self.dim_size-1, row+1)+1):
                for c in range(max(0, col-1), min(self.dim_size-1, col+1)+1):
                    if (r, c) in self.dug:
                        continue
                    self.dig(r, c)
        return True
        
        


    def __str__(self):
        visible_board=[[None for _ in range(self.dim_size)] for _ in range(self.dim_size)]
        for row in range(self.dim_size):
            for col in range(self.dim_size):
                if (row,col) in self.dug:
                    visible_board[row][col] = str(self.board[row][col])
                else:
                    visible_board[row][col] = ' '

        # put this together in a string
        string_rep = ''
        # get max column widths for printing
        widths = []
        for idx in range(self.dim_size):
            columns = map(lambda x: x[idx], visible_board)
            widths.append(
                len(
                    max(columns, key = len)
                )
            )

        # print the csv strings
        indices = [i for i in range(self.dim_size)]
        indices_row = '   '
        cells = []
        for idx, col in enumerate(indices):
            format = '%-' + str(widths[idx]) + "s"
            cells.append(format % (col))
        indices_row += '  '.join(cells)
        indices_row += '  \n'
        
        for i in range(len(visible_board)):
            row = visible_board[i]
            string_rep += f'{i} |'
            cells = []
            for idx, col in enumerate(row):
                format = '%-' + str(widths[idx]) + "s"
                cells.append(format % (col))
            string_rep += ' |'.join(cells)
            string_rep += ' |\n'

        str_len = int(len(string_rep) / self.dim_size)
        string_rep = indices_row + '-'*str_len + '\n' + string_rep + '-'*str_len

        return string_rep


def play(dim_size = 10, num_bombs = 10):
    board=Board(dim_size, num_bombs)

    safe=True

    while len(board.dug) < board.dim_size**2 - num_bombs:
        print(board)
        #can handle 0, 0 or 0,0 or 0,   0. It splits the space and the characters
        user_input = re.split(',(\\s)*', input("Choose a location to dig? (Input as row,col format):"))
        row, col = int(user_input[0]), int(user_input[-1])
        if row < 0 or row >= board.dim_size or col >= board.dim_size:
            print ("Invalid Location, try again!") 
            continue

        #if it's valid, we dig
        safe = board.dig(row, col)
        if not safe: #dug a bomb
            break #gameover
    
    #there two ways the game gonna end up, either you dig all squares safely or you dig a bomb
    if safe:
        print ("CONGRATULATIONS, YOU WON !!")
    else:
        print ("SORRY, YOU LOST..")
        board.dug=[(r,c) for r in range(board.dim_size) for c in range(board.dim_size)]
        print (board)

if __name__ == '__main__':
    play()