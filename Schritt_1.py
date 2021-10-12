import pygame
import sys
import os
from pygame.locals import *
pygame.display.set_caption("Space Invaders")


class Game():
    laser_list = []

    def __init__(self):
        pygame.init()
        self.width = 800
        self.height = 600
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.clock = pygame.time.Clock()
        self.bg = pygame.transform.scale(pygame.image.load(os.path.join(r"images/bg_1.png")), (self.width, self.height))
        self.position = (0, 0)  # Position für das Hintergrundbild
        self.pause = True

        self.image = pygame.transform.scale(pygame.image.load(r"images/mk_ship.png"),(50, 50))
        colorkey = self.image.get_at((0, 0))
        self.image.set_colorkey(colorkey, RLEACCEL)

        go = True
        Ship_position = Ship(self, self.width / 2, self.height - 100) # Ship position Anfang Spiel
        #enemie_pos

        while go:

            pressed = pygame.key.get_pressed()
            if pressed[pygame.K_LEFT]:             # Taste Links
                Ship_position.x -= 2 if Ship_position.x > 10 else 0  # linke Bereichsgrenze (2 Schritte nach Links / 10 px Begranzung)
            elif pressed[pygame.K_RIGHT]:           # Taste Recht
                Ship_position.x += 2 if Ship_position.x < self.width - 30 else 0  # rechte Bereichsgrenze linke Bereichsgrenze (2 Schritte nach Rechts / - 30 px Begranzung)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    go = True

                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    self.laser_list.append(Laser(self, Ship_position.x + 24, Ship_position.y)) # Wenn Leertaste gedrückt wird, soll das Spiel Laser in "Position Ship schießen"
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                    self.pause = not self.pause
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            if self.pause:              # Das ist für die Pause
                pygame.display.flip()
                self.clock.tick(80)                      # Geschwindigkeit der Ship von Recht zu Links
                self.screen.blit(self.bg, self.position) # Hier wird Hintergrundbild gezeigt
                self.r = pygame.Rect((Ship_position.x, Ship_position.y), (30, 30))
                self.screen.blit(self.image,self.r)


                for rocket in self.laser_list:
                    rocket.draw()

                Ship_position.draw()



class Enemies():
   pass
    #def __init__(self, surface, x, y):
        #self.x = x
        #self.y = y
        #self.surface = surface



    #def draw(self):
        #pygame.draw.rect(self.surface.screen,(210, 250, 251),
         #                pygame.Rect(self.x, self.y, 30, 30))






class Settings():
        pass


class Ship():
    def __init__(self, surface, x, y):
        self.x = x
        self.y = y
        self.surface = surface



    def draw(self):
        #pygame.draw.rect(self.surface.screen,(210, 250, 251),
                         #pygame.Rect(self.x, self.y, 30, 30))
        pass





class Laser():
    def __init__(self, surface, x, y):
        self.x = x
        self.y = y
        self.surface = surface

    def draw(self):         # Laser zeichnen
        pygame.draw.rect(self.surface.screen, (0, 255, 0),
                         pygame.Rect(self.x, self.y, 2, 8))
        self.y -= 2         # Geschwindigkeit von Laser



def main ():
    Game()
main()