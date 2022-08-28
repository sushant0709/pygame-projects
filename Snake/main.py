from pickle import FALSE
import pygame as pg
from pygame.locals import *
import time
import random

SIZE = 40
INITIAL_X = 50
INITIAL_Y = 50
SCREEN_X = 1600
SCREEN_Y = 1000

class Apple:
    def __init__(self,present_screen) -> None:
        self.screen = present_screen
        self.image = pg.image.load('resources/apple.jpg').convert()
        self.x = random.randint(0,SCREEN_X/SIZE-2)*SIZE
        self.y = random.randint(0,SCREEN_Y/SIZE-2)*SIZE


    def draw(self) -> None:
        print(f"Apple_x = {self.x} Apple_y = {self.y}")
        self.screen.blit(self.image,(self.x,self.y))
        # pg.display.update()
    
    def move(self) -> None:
        self.x = random.randint(0,SCREEN_X/SIZE-2)*SIZE
        self.y = random.randint(0,SCREEN_Y/SIZE-2)*SIZE
        self.draw()

class Snake:
    def __init__(self,present_screen,length) -> None:
        self.screen = present_screen
        self.block = pg.image.load('resources/block.jpg').convert()
        self.x = [INITIAL_X]*length
        self.y = [INITIAL_Y]*length
        self.direction = 'down'
        self.length = length

    def draw(self) -> None:
        # 66, 245, 206
        self.screen.fill((66, 245, 206))
        print(f"Length = {self.length}")
        for i in range(self.length):
            print(f"x = {self.x} y = {self.y}")
            self.screen.blit(self.block,(self.x[i],self.y[i]))
        # pg.display.flip()
    
    def move_up(self) -> None:
        self.direction = 'up'

    def move_down(self) -> None:
        self.direction = 'down'
    
    def move_left(self) -> None:
        self.direction = 'left'
    
    def move_right(self) -> None:
        self.direction = 'right'
    
    def walk(self) -> None:
        for i in range(self.length-1,0,-1):
            self.x[i] = self.x[i-1]
            self.y[i] = self.y[i-1]
        if(self.direction == 'up'):
            self.y[0] -= SIZE
        elif(self.direction == 'down'):
            self.y[0] += SIZE
        elif(self.direction == 'left'):
            self.x[0] -= SIZE
        elif(self.direction == 'right'):
            self.x[0] += SIZE
        
        self.draw()
        
class Game:
    def __init__(self) -> None:
        pg.init()
        self.surface = pg.display.set_mode((SCREEN_X,SCREEN_Y))
        self.snake = Snake(self.surface,1)
        self.snake.walk()
        self.apple = Apple(self.surface)
        self.apple.draw()
        pg.display.flip()


    def isCollision(self,apple_x,apple_y,snake_x,snake_y) -> bool:
        if(snake_x>apple_x and snake_x<apple_x+SIZE) or (snake_x+SIZE>apple_x and snake_x+SIZE<apple_x+SIZE):
            if(snake_y>apple_y and snake_y<apple_y+SIZE) or (snake_y+SIZE>apple_y and snake_y+SIZE<apple_y+SIZE):
                
                return True
        return False

    def play(self) -> None:
        self.snake.walk()
        self.apple.draw()
        pg.display.flip()
        if(self.isCollision(self.apple.x,self.apple.y,self.snake.x[0],self.snake.y[0])):
            self.apple.move()
            self.snake.x.append(100)
            self.snake.y.append(100)
            self.snake.length += 1
            self.snake.draw()
            pg.display.flip()

    def run(self) -> None:
        running = True
        while running:
            # self.snake.walk()
            # self.apple.draw()
            for event in pg.event.get():
                if event.type == QUIT:   
                    running = False
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False
                    elif event.key == K_UP:
                        self.snake.move_up()
                    elif event.key == K_DOWN:
                        self.snake.move_down()
                    elif event.key == K_LEFT:
                        self.snake.move_left()
                    elif event.key == K_RIGHT:
                        self.snake.move_right()

            self.play()
            time.sleep(0.2)
                

if __name__ == '__main__':
    game = Game()
    game.run()
