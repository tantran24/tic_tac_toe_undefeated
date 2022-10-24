
import random
import pygame, sys
from array import array
from tabnanny import check




class Tictactoe:
    
    
    array = [[' ',' ',' ']
                ,[' ',' ',' ']
                ,[' ',' ',' ']]


    def draw(self):
        print("___________________")
        for i in range (3):
            print("|", end = '')
            for j in range (3):
                print(" ", self.array[i][j], end='  |')
            print()
            print("___________________")


    def checkwinner(self):
        if self.__numMoves < 5:
            return 'null'
        a, b = self.current
        # print("CHECK ",a, b)
        #check column
        if self.array[0][b] == self.array[1][b] == self.array[2][b]:
            return self.array[a][b]
        #check row
        if self.array[a][0] == self.array[a][1] == self.array[a][2]:
            return self.array[a][b]
 
        # #check row
        # for i in range (3):
        #     if self.array[i][0] == self.array[i][1] == self.array[i][2] and self.array[i][1] != ' ':
        #         return self.array[i][0]
        # #check column
        # for i in range (3):
        #     if self.array[0][i] == self.array[1][i] == self.array[2][i] and self.array[0][i] != ' ':
        #         return self.array[0][i]
        #check diagonal
        if self.array[0][0] == self.array[1][1] == self.array[2][2] and self.array[1][1] != ' ':
            return self.array[1][1]
        if self.array[2][0] == self.array[1][1] == self.array[0][2] and self.array[1][1] != ' ':
            return self.array[1][1]
        #check tie
        # for i in range (3):
        #     for j in range(3):
        #         if self.array[i][j] == ' ':
        #             return 'null'
        # return 'tie' 
        if self.__numMoves == 9:
            return 'tie'
        return 'null'

    Score, depth = 0, 0
    move = (0, 0)

    def bestMove(self):
        #AI turn
        pointEva = -10
        mindepth = 100
        for i in range(3):
            for j in range(3):
                if self.array[i][j] == ' ':
                    self.array[i][j] = 'x'
                    self.__numMoves = self.__numMoves + 1
                    self.current = i, j
                    Score, depth = self.minimax(False, 0)
                    self.array[i][j] = ' '
                    self.__numMoves = self.__numMoves - 1
                    if (Score > pointEva) or (Score == pointEva and depth < mindepth):
                        pointEva = Score
                        mindepth = depth
                        move = (i,j)
        return move

    Rule = {'tie' : 0, 'o' : -1, 'x' : 1}
    current = 0, 0
    __numMoves = 0

    def minimax(self, isMaxPlayer, depth):
        if self.checkwinner() != 'null':
            return self.Rule[self.checkwinner()], depth
        if isMaxPlayer:
            pointEva = -10
            for i in range(3):
                for j in range(3):
                    if self.array[i][j] == ' ':
                        self.array[i][j] = 'x'
                        self.__numMoves = self.__numMoves + 1
                        self.current = i, j
                        Score, depth = self.minimax(False, depth + 1)
                        self.array[i][j] = ' '
                        self.__numMoves = self.__numMoves - 1
                        pointEva = max(Score, pointEva)
            return pointEva, depth
        else:
            pointEva = 10
            for i in range(3):
                for j in range(3):
                    if self.array[i][j] == ' ':
                        self.array[i][j] = 'o'
                        self.__numMoves = self.__numMoves + 1
                        self.current = i, j
                        Score, depth = self.minimax(True, depth + 1)
                        self.array[i][j] = ' '
                        self.__numMoves = self.__numMoves - 1
                        pointEva = min(Score, pointEva)
            return pointEva, depth


    def game(self):
        print("# Choose your turn : ")
        print("- FIRST : 1")
        print("- THEN  : 2")
        t = int(input())
        if t == 2:
            x = 1
            y = 1
            self.array[x][y] = 'x'
            self.__numMoves = self.__numMoves + 1
            self.current = x, y
            self.draw()
            while self.checkwinner() == 'null':          
                while True:
                    print("Input your desired position: ")
                    a, b = list(map(int, input().split()))
                    if self.array[a][b] == ' ':
                        break
                self.array[a][b] = 'o'
                self.__numMoves = self.__numMoves + 1
                self.current = a, b
                if self.checkwinner() != 'null':
                    break
                move = self.bestMove()
                self.array[move[0]][move[1]] = 'x' 
                self.__numMoves = self.__numMoves + 1
                self.current = move
                self.draw()
                print(self.current, self.__numMoves)
        else:
            while True:     
                self.draw()       
                while True:
                    print("Input your desired position: ")
                    a, b = list(map(int, input().split()))
                    if self.array[a][b] == ' ':
                        break
                self.array[a][b] = 'o'
                self.__numMoves = self.__numMoves + 1
                self.current = a, b
                if self.checkwinner() != 'null':
                    break
                move = self.bestMove()
                self.draw()
                self.array[move[0]][move[1]] = 'x'
                self.__numMoves = self.__numMoves + 1
                self.current = move
                if self.checkwinner() != 'null':
                    break
            self.draw()  
        self.Report()
        
    def Report(self):
        winner = self.checkwinner()
        print(winner, end = '')
        if winner != 'tie':
            print(' is the winner! \(^o^)/')
        else:
            print("!")

    
# Game = Tictactoe()
# Game.game()        
# 
vec2 = pygame.math.Vector2
class Game:
    w, h = 960, 540
    def __init__(self):
        pygame.init()     
        self.screen = pygame.display.set_mode((self.w, self.h))
        self.clock = pygame.time.Clock()
        self.bg = pygame.image.load('images/back-ground.jpg')
        self.bg = pygame.transform.scale(self.bg, (self.w, self.h))
        self.X = pygame.image.load('images/X.png')
        self.X = pygame.transform.scale(self.X, (self.h/4, self.h/4))
        self.O = pygame.image.load('images/O.png')
        self.O = pygame.transform.scale(self.O, (self.h/4, self.h/4))
        self.tic_tac_toe = Tictactoe()
        self.board = [[' ',' ',' ']
                     ,[' ',' ',' ']
                     ,[' ',' ',' ']]
        self.turn = 'x'

    WHITE = (255, 255, 255)
    ORIGIN_board = vec2(48, 80)
    CELL_SIZE = h*2/3

    def draw_objects(self):
        for i, row  in enumerate (self.board):
            for j, obj in enumerate (row):
                if obj != ' ':
                    x, y = map(int,self.ORIGIN_board + vec2(i*self.w/8, j*self.w/8))
                    print("(x,y) = ",x,y)
                    print("(i,j) =",i,j)
                    if self.board[i][j] == 'x':                 
                        self.screen.blit(self.X, (x, y))
                    elif self.board[i][j] == 'o':
                        self.screen.blit(self.O, (x, y))

                    
    def draw(self):
        self.screen.blit(self.bg, (0,0))
        self.draw_objects()


    def check_events(self):
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    def game_core(self):
        current_cell = (vec2(pygame.mouse.get_pos()) - self.ORIGIN_board) // (self.CELL_SIZE//3)
        col, row = map(int, current_cell)
        print(row, col)
        left_click = pygame.mouse.get_pressed()[0]

        if left_click and self.board[row][col] == ' ':
            self.board[row][col] = self.turn
            if self.turn == 'o':
                self.turn = 'x' 
            elif self.turn == 'x':
                self.turn = 'o'

    def run(self):
        while True:
            self.check_events()
            self.draw()
            self.game_core() 
            
            left_click = pygame.mouse.get_pressed()[0]
            current_cell = vec2(pygame.mouse.get_pos())
            print("QQQQ",current_cell)

            pygame.display.flip()
            self.clock.tick(45)
            #print(self.board)


A = Game()
A.run()

pygame.quit()
