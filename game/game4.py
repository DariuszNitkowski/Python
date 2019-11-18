import time
import pygame, sys
from pygame.locals import *
import math
import os
import shutil


shutil.copyfile("game.bmp", "game1.bmp") # zaczynam od zabepieczenia źródłowego pliku zeby nastepne uruchomienie było z czystą kartka
class Krzywa():
    pygame.init()
    window_width = 800
    window_height = 600
    size = (window_width, window_height)
    screen = pygame.display.set_mode(size)
    WHITE = (255, 255, 255)
    BLUE = (0, 0, 255)
    RED = (255, 0, 0) # te atrybuty zmienne przeniosłem tutaj żeby móc je wywoływać przez definicje statyczne, niezwiązane z rysowaniem
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
        count=max(abs(start[0]-self.stop[0]), abs(start[1]-self.stop[1])) # wybieram większa różnice żeby obliczyc ilość skoków
        if start[0] < stop[0]: #idzie w prawo
            znak_x = 1
        elif start[0]==stop[0]: # idzie do góry lub dołu
            znak_x = 0
        elif start[0] > stop[0]: # idzie w lewo
            znak_x = -1

        if start[1]<stop[1]: # idzie w dół
            znak_y=1
        elif start[1]==stop[1]: # idzie bok
            znak_y=0
        elif start[1]>stop[1]: #idie do góry
            znak_y=-1
        skok=int(round((count / pixel),0)) # tutaj jest ilość skoków
        x = int(znak_x* abs(start[0] - stop[0]) / skok) #obliczam długoś skoku dla x
        y = int(znak_y*abs(start[1] - stop[1]) / skok)# i dla y

        if (abs(start[0]-stop[0])/skok).is_integer():
            ulamek_x=0
        else:
            ulamek_x=(abs(start[0]-stop[0])/skok)-(int(abs(start[0]-stop[0])/skok))
        if (abs(start[1]-stop[1])/skok).is_integer():
            ulamek_y=0
        else:
            ulamek_y=(abs(start[1]-stop[1])/skok)-(int(abs(start[1]-stop[1])/skok))


         # tuatj ustalam rozdzielczosc samego okienka
        player = pygame.image.load("game1.bmp") # tutaj ładuje background
        player = pygame.transform.scale(player,size) # tutaj dopasowuje background do okienka
        screen.blit(player, [0, 0]) # tutaj ładuje obrazek na screena
        pygame.display.update()


        pygame.draw.circle(screen, BLUE, start, 5,0) # ale zeby wyswietlic kropke to juz screen jako pierwszy argument! chbya dlatego że player został
            # zmieniaony na screena a raczej screen wziął cechy playera przez screen.blit!
        pygame.display.update()


        pixel_count_x=0
        pixel_count_y=0
        ulamek_x_count=0
        ulamek_y_count=0
        for i in range(skok):
            ulamek_x_count = ulamek_x_count + ulamek_x# tutaj powiększam ułamki
            ulamek_y_count = ulamek_y_count + ulamek_y
            if ulamek_x_count - pixel_count_x > pixel: # tutaj będę dodawał pixele jeśli ułamek bieżacy dodawany będzie wiekszy od pixela
                pixel_count_x+= 1
            if ulamek_y_count - pixel_count_y > pixel:
                pixel_count_y += 1
            pygame.draw.circle(screen, BLUE,((start[0] + x+(znak_x*pixel_count_x)), (start[1] + y+(znak_y*pixel_count_y))), 5)
            pygame.display.update()
            time.sleep(0.05)
            start[0]=start[0]+x
            start[1]=start[1]+y


        pygame.image.save(screen,"d:/python/nauka/game1.bmp") # ten tutaj zapisuje screen zeby nie kasowac tego co juz zrobił

        pygame.display.update()

    # uzycie metody klasy:Zwykła metoda zmusza cię do wywoływania na rzecz konkretnego obiektu a to nie zawsze ma sens
    @staticmethod
    def stop_program():
        while True:
            for event in pygame.event.get():
                if event.type==MOUSEBUTTONDOWN:
                    pygame.quit()
                    print("Program zamknięty poprawnie")
                    sys.exit()
            pygame.display.update()
    @classmethod
    def stop_draw(cls):
        pygame.draw.circle(Krzywa.screen, Krzywa.RED, (450, 350), 5)
        pygame.display.update()

"""
pierwsza=Krzywa([100,100],[100,200],5)
druga=Krzywa([100,200],[200,200],5)
trzecia=Krzywa([200,200],[200,100],5)
czwarta=Krzywa([200,100],[100,100],5)"""

pierwsza=Krzywa([50,100],[300,50],5)
druga=Krzywa([300,50],[350,300],5)
trzecia=Krzywa([350,300],[400,50],5)
czwarta=Krzywa([400,50],[50,400],5)

pierwsza.draw()
druga.draw()
trzecia.draw()
czwarta.draw()
Krzywa.stop_draw()
Krzywa.stop_program()
