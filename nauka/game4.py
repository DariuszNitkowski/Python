import time
import pygame, sys
from pygame.locals import *
import math
import os
import shutil





shutil.copyfile("game.bmp", "game1.bmp") # start from copying to keep source untouched
class Coordinates():
    pygame.init()
    window_width = 800
    window_height = 600
    size = (window_width, window_height)
    screen = pygame.display.set_mode(size)
    WHITE = (255, 255, 255)
    BLUE = (0, 0, 255)
    RED = (255, 0, 0) # i move them here to be able to use them from class methods
    def __init__(self,start,stop,pixel):
        self.start=start.copy()
        self.stop=stop.copy()
        self.pixel=pixel

    def draw(self):
        screen=self.screen
        WHITE=self.WHITE
        BLUE=self.BLUE
        RED=self.RED
        start=self.start
        stop=self.stop
        pixel=self.pixel
        size=self.size
        count=max(abs(start[0]-self.stop[0]), abs(start[1]-self.stop[1])) # peek up the highest diffrence
        if start[0] < stop[0]: #moves right
            sign_x = 1
        elif start[0]==stop[0]: # moves straigh up or down
            sign_x = 0
        elif start[0] > stop[0]: # moves lef
            sign_x = -1

        if start[1]<stop[1]: # i moves down
            sign_y=1
        elif start[1]==stop[1]: # moves sideways
            sign_y=0
        elif start[1]>stop[1]: #moves up
            sign_y=-1
        moves=int(round((count / pixel),0)) # how many repetitions
        x = int(sign_x* abs(start[0] - stop[0]) / moves) # how long would be single move
        y = int(sign_y*abs(start[1] - stop[1]) / moves)# and for y

        if (abs(start[0]-stop[0])/moves).is_integer():
            fraction_x=0
        else:
            fraction_x=(abs(start[0]-stop[0])/moves)-(int(abs(start[0]-stop[0])/moves))
        if (abs(start[1]-stop[1])/moves).is_integer():
            fraction_y=0
        else:
            fraction_y=(abs(start[1]-stop[1])/moves)-(int(abs(start[1]-stop[1])/moves))


         # resolution for window
        player = pygame.image.load("game1.bmp") # tutaj ładuje background
        player = pygame.transform.scale(player,size) # adjusting background
        screen.blit(player, [0, 0])
        pygame.display.update()


        pygame.draw.circle(screen, BLUE, start, 5,0)
        pygame.display.update()


        pixel_count_x=0
        pixel_count_y=0
        fraction_x_count=0
        fraction_y_count=0
        for i in range(moves):
            fraction_x_count = fraction_x_count + fraction_x
            fraction_y_count = fraction_y_count + fraction_y
            if fraction_x_count - pixel_count_x > pixel:
                pixel_count_x+= 1
            if fraction_y_count - pixel_count_y > pixel:
                pixel_count_y += 1
            pygame.draw.circle(screen, BLUE,((start[0] + x+(sign_x*pixel_count_x)), (start[1] + y+(sign_y*pixel_count_y))), 5)
            pygame.display.update()
            time.sleep(0.05)
            start[0]=start[0]+x
            start[1]=start[1]+y


        pygame.image.save(screen,"d:/python/nauka/game1.bmp")

        pygame.display.update()


    @staticmethod
    def stop_program():
        while True:
            for event in pygame.event.get():
                if event.type==MOUSEBUTTONDOWN:
                    pygame.quit()
                    print("Program closed")
                    sys.exit()
            pygame.display.update()
    @classmethod
    def stop_draw(cls):
        pygame.draw.circle(Coordinates.screen, Coordinates.RED, (450, 350), 5)
        pygame.display.update()



first=Coordinates([50,100],[300,50],5)
second=Coordinates([300,50],[350,300],5)
third=Coordinates([350,300],[400,50],5)
fourth=Coordinates([400,50],[50,400],5)

first.draw()
second.draw()
third.draw()
fourth.draw()
Coordinates.stop_draw()
Coordinates.stop_program()