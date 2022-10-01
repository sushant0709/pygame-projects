from pickle import FALSE
import pygame as pg
from pygame.locals import *
import time
import random

SIZE = 40
INITIAL_X = 50
INITIAL_Y = 50
SCREEN_X = None
SCREEN_Y = None
class Apple:
    def __init__(self,present_screen) -> None:
        self.screen = present_screen
        self.image = pg.image.load('resources/apple.jpg').convert()
        self.x = random.randint(0,SCREEN_X/SIZE-2)*SIZE
        self.y = random.randint(0,SCREEN_Y/SIZE-2)*SIZE


    def draw(self) -> None:
        #print(f"Apple_x = {self.x} Apple_y = {self.y}")
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
        self.screen.fill((0, 0, 0))
        #print(f"Length = {self.length}")
        for i in range(self.length):
            #print(f"x = {self.x} y = {self.y}")
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

    def increase_length(self) -> None:
        self.x.append(100)
        self.y.append(100)
        self.length += 1
        
class Game:
    def __init__(self) -> None:
        pg.init()
        infoObject = pg.display.Info()
        global SCREEN_X
        SCREEN_X = infoObject.current_w
        global SCREEN_Y
        SCREEN_Y = infoObject.current_h
        print(f"Screen X = {SCREEN_X} Screen Y = {SCREEN_Y}")
        self.surface = pg.display.set_mode((SCREEN_X,SCREEN_Y))
        self.snake = Snake(self.surface,1)
        self.snake.walk()
        self.apple = Apple(self.surface)
        self.apple.draw()
        pg.display.flip()

    def reset(self) -> None:
        self.snake = Snake(self.surface,1)
        self.apple = Apple(self.surface)

    def show_game_over(self) -> None:
        self.surface.fill((0, 0, 0))
        font = pg.font.SysFont('arial',30)
        line1 = font.render(f"Game Over !! Your Score is: {self.snake.length}",True,(255,255,255))
        self.surface.blit(line1,(SCREEN_X/2-20,SCREEN_Y/2-20))

    def isCollision(self,apple_x,apple_y,snake_x,snake_y) -> bool:
        if(snake_x>apple_x and snake_x<apple_x+SIZE) or (snake_x+SIZE>apple_x and snake_x+SIZE<apple_x+SIZE):
            if(snake_y>apple_y and snake_y<apple_y+SIZE) or (snake_y+SIZE>apple_y and snake_y+SIZE<apple_y+SIZE):
                return True
        return False

    def display_score(self) -> None:
        font = pg.font.SysFont('arial',30)
        score = font.render(f"Score: {self.snake.length}",True,(255,255,255))
        self.surface.blit(score,(SCREEN_X/2 -10,40))

    def play(self) -> None:
        self.snake.walk()
        self.apple.draw()
        self.display_score()
        pg.display.flip()
        # collision with apple
        if(self.isCollision(self.apple.x,self.apple.y,self.snake.x[0],self.snake.y[0])):
            self.snake.increase_length()
            self.apple.move()

        # collision with itself
        for i in range(2,self.snake.length):
            if(self.isCollision(self.snake.x[0],self.snake.y[0],self.snake.x[i],self.snake.y[i])):
                raise "Collision Occured"


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

            try:
                self.play()
            except Exception as e:
                self.show_game_over()
                self.reset()
            time.sleep(0.15)
                

if __name__ == '__main__':
    game = Game()
    game.run()
