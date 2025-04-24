import pygame
from math import pi
import physics_engine

# Classe qui représente une planche (Slab), qui peut être horizontale ou verticale
class Slab:
    def __init__(self, x, y, w, h, color=(255, 255, 255)):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.image = pygame.image.load("Images/wall_horizontal.png") if self.w > self.h else pygame.image.load("Images/wall_vertical.png")
        self.image = pygame.transform.scale(self.image, (self.w, self.h))
        self.color = color

    def draw(self, display):
        display.blit(self.image, (self.x, self.y))

    # Gestion des collisions entre la balle et la planche
    def collision_manager(self, ball, type="BALL"):
        if type == "BALL":
            if (ball.y + ball.r > self.y) and (ball.y < self.y + self.h):
                if (ball.x < self.x + self.w) and (ball.x + ball.r > self.x + self.w):
                    ball.x = 2*(self.x + self.w) - ball.x
                    ball.velocity.angle = - ball.velocity.angle
                    ball.velocity.magnitude *= physics_engine.elasticity
                elif ball.x + ball.r > self.x and (ball.x < self.x):
                    ball.x = 2*(self.x - ball.r) - ball.x
                    ball.velocity.angle = - ball.velocity.angle
                    ball.velocity.magnitude *= physics_engine.elasticity

            if (ball.x + ball.r > self.x) and (ball.x < self.x + self.w):
                if ball.y + ball.r > self.y and ball.y < self.y:
                    ball.y = 2*(self.y - ball.r) - ball.y
                    ball.velocity.angle = pi - ball.velocity.angle
                    ball.velocity.magnitude *= physics_engine.elasticity
                elif (ball.y < self.y + self.h) and (ball.y + ball.r > self.y + self.h):
                    ball.y = 2*(self.y + self.h) - ball.y
                    ball.velocity.angle = pi - ball.velocity.angle
                    ball.velocity.magnitude *= physics_engine.elasticity
        return ball