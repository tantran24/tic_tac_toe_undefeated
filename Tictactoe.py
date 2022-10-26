from random import randint
import pygame, sys
from array import array
from tabnanny import check

class Tictactoe:
    def __init__(self):   
        self.array = [[' ',' ',' ']
                ,[' ',' ',' ']
                ,[' ',' ',' ']]

    def checkwinner(self):
        if self.numMoves < 5:
            return 'null'
        a, b = self.current
        #check column
        if self.array[0][b] == self.array[1][b] == self.array[2][b]:
            return self.array[a][b]
        #check row
        if self.array[a][0] == self.array[a][1] == self.array[a][2]:
            return self.array[a][b]
        #check diagonal
        if self.array[0][0] == self.array[1][1] == self.array[2][2] and self.array[1][1] != ' ':
            return self.array[1][1]
        if self.array[2][0] == self.array[1][1] == self.array[0][2] and self.array[1][1] != ' ':
            return self.array[1][1]
        #check tie
        if self.numMoves == 9:
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
                    self.numMoves = self.numMoves + 1
                    self.current = i, j
                    Score, depth = self.minimax(False, 0)
                    self.array[i][j] = ' '
                    self.numMoves = self.numMoves - 1
                    if (Score > pointEva) or (Score == pointEva and depth < mindepth):
                        pointEva = Score
                        mindepth = depth
                        move = (i,j)
        return move

    Rule = {'tie' : 0, 'o' : -1, 'x' : 1}
    current = 0, 0
    numMoves = 0

    def minimax(self, isMaxPlayer, depth):
        if self.checkwinner() != 'null':
            return self.Rule[self.checkwinner()], depth
        if isMaxPlayer:
            pointEva = -10
            for i in range(3):
                for j in range(3):
                    if self.array[i][j] == ' ':
                        self.array[i][j] = 'x'
                        self.numMoves = self.numMoves + 1
                        self.current = i, j
                        Score, depth = self.minimax(False, depth + 1)
                        self.array[i][j] = ' '
                        self.numMoves = self.numMoves - 1
                        pointEva = max(Score, pointEva)
            return pointEva, depth
        else:
            pointEva = 10
            for i in range(3):
                for j in range(3):
                    if self.array[i][j] == ' ':
                        self.array[i][j] = 'o'
                        self.numMoves = self.numMoves + 1
                        self.current = i, j
                        Score, depth = self.minimax(True, depth + 1)
                        self.array[i][j] = ' '
                        self.numMoves = self.numMoves - 1
                        pointEva = min(Score, pointEva)
            return pointEva, depth
    

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
        self.X = pygame.transform.scale(self.X, (self.h/5, self.h/5))
        self.O = pygame.image.load('images/O.png')
        self.O = pygame.transform.scale(self.O, (self.h/5, self.h/5))
        self.LOSE = pygame.image.load('images/LOSE.jpg')
        self.LOSE = pygame.transform.scale(self.LOSE, (self.w/1.7, self.h/1.7))
        self.TIE = pygame.image.load('images/TIE.jpg')
        self.TIE = pygame.transform.scale(self.TIE, (self.w/1.7, self.h/1.7))
        self.tic_tac_toe = Tictactoe() 
        self.turn = ' '

    WHITE = (255, 255, 255)
    ORIGIN_board = vec2(w/16.7, h/5.5)
    CELL_SIZE = h*2/3

    def draw_objects(self):
        for i, row  in enumerate (self.tic_tac_toe.array):
            for j, obj in enumerate (row):
                if obj != ' ':
                    x, y = map(int,self.ORIGIN_board + vec2(j*self.w/8, i*self.w/8))
                    if self.tic_tac_toe.array[i][j] == 'x':                 
                        self.screen.blit(self.X, (x, y))
                    elif self.tic_tac_toe.array[i][j] == 'o':
                        self.screen.blit(self.O, (x, y))

                    
    def draw(self):
        self.screen.blit(self.bg, (0,0))
        self.draw_objects()


    def check_events(self):
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
    stop = ' '
    def game_core(self):
        current_cell = (vec2(pygame.mouse.get_pos()) - self.ORIGIN_board) // (self.CELL_SIZE//3)
        col, row = map(int, current_cell)
        left_click = pygame.mouse.get_pressed()[0]
        
        if col >= 0 and col <=2 and row >= 0 and row <=2:
            if left_click and self.tic_tac_toe.array[row][col] == ' ' and self.turn == 'o':
                self.tic_tac_toe.array[row][col] = 'o'      
                self.turn = 'x' 
                self.tic_tac_toe.numMoves = self.tic_tac_toe.numMoves + 1
                self.tic_tac_toe.current = row, col
                if self.tic_tac_toe.checkwinner() != 'null':
                    self.stop = self.tic_tac_toe.checkwinner()
            
            if self.turn  == 'x':
                a, b = self.tic_tac_toe.bestMove()
                self.tic_tac_toe.array[a][b] = 'x'
                self.turn = 'o'
                self.tic_tac_toe.numMoves = self.tic_tac_toe.numMoves + 1
                self.tic_tac_toe.current = a, b
                if self.tic_tac_toe.checkwinner() != 'null':
                    self.stop = self.tic_tac_toe.checkwinner()
    game_mode = 2
    option = 0
    def run(self):
        alpha = 0
        self.check = 0
        if self.game_mode == 2:
            a, b = randint(0,2), randint(0,2)
            self.tic_tac_toe.array[a][b] = 'x'
            self.tic_tac_toe.numMoves = self.tic_tac_toe.numMoves + 1 
        self.turn = 'o'
        print(self.stop)
        while True:
            self.check_events()
            self.draw()
            x, y = pygame.mouse.get_pos()
            left_click = pygame.mouse.get_pressed()[0]            
            if self.stop == ' ':
                self.game_core() 
            else:
                self.bg.fill((200, 200, 200, alpha), None, pygame.BLEND_RGBA_MULT)
                if self.stop == 'tie':
                    self.screen.blit(self.TIE, (self.w/2.2, self.h/5))
                elif self.stop == 'x':               
                    self.screen.blit(self.LOSE, (self.w/2.2, self.h/5))                   
                if left_click and (x >= 560 and x <= 630) and (y >= 320 and y <=380):
                    self.option = 1
                elif left_click and (x >= 800 and x <= 870) and (y >= 320 and y <=380):
                    self.option = 2
                if self.option == 1:
                    self.playNewGame()
                elif self.option == 2:
                    return

            pygame.display.flip()
            self.clock.tick(60)

    def playNewGame(self):
        self = Game()
        self.run()
        
B = Game()
B.run()

pygame.quit()