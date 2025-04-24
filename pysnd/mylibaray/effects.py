# pysnd/effects.py
import pygame
import os


class SoundEffects:
    def __init__(self):
        pygame.mixer.init()
        self.effects = {}

    def load(self, name, path):
        self.effects[name] = pygame.mixer.Sound(path)

    def play(self, name):
        if name in self.effects:
            self.effects[name].play()

    def stop(self, name):
        if name in self.effects:
            self.effects[name].stop()

    def set_volume(self, name, volume):
        if name in self.effects:
            self.effects[name].set_volume(volume)
