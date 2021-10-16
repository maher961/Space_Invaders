import pygame
import sys
import os
from pygame.locals import *

pygame.display.set_caption("Space Invaders")

class Settings():
    def __init__(self):
        pass


class Bullet():
    def __init__(self):
        pass


class Score():
    def __init__(self):
        pass


class Highscore():
    def __init__(self):
        pass


class Ship():
    """
    Author: Maher Koulak, Mohammad Farhat
    :return:
    """
    def __init__(self, surface, x, y):
        self.x = x
        self.y = y
        self.surface = surface


class Laser():
    """
    Author: Maher Koulak, Mohammad Farhat
    :return:
    """
    def __init__(self, surface, x, y):
        self.x = x
        self.y = y
        self.surface = surface

    def draw(self):
        pygame.draw.rect(self.surface.screen, (0, 255, 0),
                         pygame.Rect(self.x, self.y, 2, 8))
        self.y -= 2


class Alien():
    """
    Author: Maher Koulak, Mohammad Farhat
    :return:
    """
    def __init__(self, surface, x, y):
        self.x = x
        self.y = y
        self.size = 30
        self.hoehe = 10
        self.breit = 5
        self.mitte_breit = 6
        self.surface = surface

    def draw(self):
        pygame.draw.rect(self.surface.screen, (200, 0, 0),
                         pygame.Rect(self.x, self.y, self.size, self.hoehe))
        pygame.draw.rect(self.surface.screen, (200, 0, 0),
                         pygame.Rect(self.x + 12, self.y, self.mitte_breit, self.size))
        pygame.draw.rect(self.surface.screen, (200, 0, 0),
                         pygame.Rect(self.x, self.y + 10, self.breit, self.hoehe))
        pygame.draw.rect(self.surface.screen, (200, 0, 0),
                         pygame.Rect(self.x + 25, self.y + 10, self.breit, self.hoehe))
        self.y += 0.20

    def kill_aliens(self, surface):
        for laser in surface.laser_list:
            if (laser.x < self.x + self.size and
                    laser.x > self.x - 6 and
                    laser.y < self.y + self.size and
                    laser.y > self.y ):
                surface.laser_list.remove(laser)
                surface.aliens.remove(self)


class AlienFeld():
    """
    Author: Maher Koulak, Mohammad Farhat
    :return:
    """
    def __init__(self, surface):
        margin = 30
        zwischen_breit = 50
        for x in range(margin, surface.width - margin, zwischen_breit):
            for y in range(margin, int(surface.height / 2), zwischen_breit):
                surface.aliens.append(Alien(surface, x, y))


class Shield():
    """
    Author: Maher Koulak, Mohammad Farhat
    :return:
    """
    def __init__(self, surface, x, y):
        self.x = x
        self.y = y
        self.size = 50
        self.size_y = 2
        self.surface = surface

    def draw(self):
        pygame.draw.rect(self.surface.screen, (255, 255, 0),
                         pygame.Rect(self.x, self.y, 50, 5))

    def kill_schield(self, surface):
        for laser_1 in surface.laser_list:
            if (laser_1.x < self.x + self.size and
                    laser_1.x > self.x - 6 and
                    laser_1.y < self.y + self.size_y and
                    laser_1.y > self.y ):
                surface.laser_list.remove(laser_1)
                surface.steine.remove(self)

        for m in surface.aliens:
            if (m.y < self.y + self.size and
                    m.y > self.y - 29 and
                    m.x - 10 < self.x - self.size_y and
                    m.x > self.x):
                surface.aliens.remove(m)
                surface.steine.remove(self)


class ShieldFeld():
    """
    Author: Maher Koulak, Mohammad Farhat
    :return:
    """
    def __init__(self, surface):
        margin = 75
        zwischen_breit = 100
        m = 10
        for x in range(margin, surface.width - margin, zwischen_breit):
            for y in range(margin, int(surface.height / 5), m):
                surface.steine.append(Shield(surface, x, y + 340))


class Game():
    """
    Author: Maher Koulak, Mohammad Farhat
    :return:
    """
    steine = []
    laser_list = []
    alien_laser = []
    aliens = []
    lost = False

    def __init__(self):
        pygame.init()
        self.width = 800
        self.height = 600
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.clock = pygame.time.Clock()
        self.pause = True
        self.bg = pygame.transform.scale(pygame.image.load(os.path.join(r"images/bg_1.png")), (self.width, self.height))
        self.position = (0, 0)
        self.image = pygame.transform.scale(pygame.image.load(r"images/mk_ship.png"), (50, 50))
        colorkey = self.image.get_at((0, 0))
        self.image.set_colorkey(colorkey, RLEACCEL)

        go = True
        Ship_position = Ship(self, self.width / 2, self.height - 100)
        AlienFeld(self)
        ShieldFeld(self)
        while go:
            if len(self.aliens) == 0:
                self.displayText("Gewonnen!!!")

            pressed = pygame.key.get_pressed()
            if pressed[pygame.K_LEFT]:
                Ship_position.x -= 2 if Ship_position.x > 0 else 0
            elif pressed[pygame.K_RIGHT]:
                Ship_position.x += 2 if Ship_position.x < self.width - 50 else 0

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    self.laser_list.append(Laser(self, Ship_position.x + 24, Ship_position.y))
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                    self.pause = not self.pause
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE or event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            if self.pause:
                pygame.display.flip()
                self.clock.tick(80)
                self.screen.blit(self.bg, self.position)
                self.r = pygame.Rect((Ship_position.x, Ship_position.y), (30, 30))
                self.screen.blit(self.image,self.r)
                for shield in self.steine:
                    shield.draw()
                    shield.kill_schield(self)

                for alien in self.aliens:
                    alien.draw()
                    alien.kill_aliens(self)
                    if (alien.y > Ship_position.y):
                        self.lost = True
                        self.displayText("Verloren!!!")

                for laser_2 in self.laser_list:
                    laser_2.draw()

    def displayText(self, text):
        pygame.font.init()
        font = pygame.font.SysFont('Arial', 50)
        textsurface = font.render(text, False, (0, 255, 0))
        self.screen.blit(textsurface, (300, 200))

def main ():
    Game()
main()
