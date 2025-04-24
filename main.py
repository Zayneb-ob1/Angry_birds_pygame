import pygame
import sys
from math import *
from mylibrary import SoundEffects
import physics_engine
import objects
import maps
import interface

# Initialisation de Pygame
pygame.init()

WIDTH, HEIGHT = 1100, 500
# couleurs utilisées dans l'interface
FONT_COLOR = (236, 240, 241)
BUTTON_YELLOW = (244, 208, 63)
BUTTON_YELLOW_HOVER = (247, 220, 111)
BUTTON_RED = (241, 148, 138)
BUTTON_RED_HOVER = (245, 183, 177)

# Setup display
display = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Angry Birds')
clock = pygame.time.Clock()

def close():
    pygame.quit()
    sys.exit()

backgrounds = pygame.image.load("assets/image.jpg")
backgrounds = pygame.transform.scale(backgrounds, (WIDTH, HEIGHT))
background_game = pygame.image.load("assets/game.jpg")
background_game = pygame.transform.scale(background_game, (WIDTH, HEIGHT))

def start_game(map):
    try:
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    close()

            display.blit(background_game, (0, 0))
            map.draw_map()

            pygame.display.update()
            clock.tick(60)
    except Exception as e:
        print(f"Error starting game: {e}")
        close()

def menu_loop(map, start, quit_btn):
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                close()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if quit_btn.isActive():
                    quit_btn.action()
                if start.isActive():
                    start.action()
                    return
        display.blit(backgrounds, (0, 0))
        start.draw()
        quit_btn.draw()
        
        pygame.display.update()
        clock.tick(60)
def GAME():
    physics_engine.init(display)
    interface.init(display)
    maps.init(display)

    map = maps.Maps()
    start = interface.Button(WIDTH//2 - 250, 380, 200, 75, lambda: start_game(map), BUTTON_YELLOW, BUTTON_YELLOW_HOVER)
    start.add_text("START GAME", 40, "Fonts/arfmoochikncheez.ttf", (0, 0, 0))

    quit_btn = interface.Button(WIDTH//2 + 50, 380, 200, 75, close, BUTTON_RED, BUTTON_RED_HOVER)
    quit_btn.add_text("QUIT", 40, "Fonts/arfmoochikncheez.ttf", (0, 0, 0))
    menu_loop(map, start, quit_btn)

    display.blit(background_game, (0, 0))
    pygame.display.update()
    map.draw_map()
        
se = SoundEffects()
se.load("click", r"C:\Users\HP\Documents\Angry_birds\pysnd\sounds\nom_du_fichier.ogg")
se.play("click")

if __name__ == "__main__":
    GAME()