import pygame

class Sound:
    def __init__(self, sound_file):
        self.sound_file = sound_file
        self.sound = pygame.mixer.Sound(sound_file)

    def play(self):
        self.sound.play()