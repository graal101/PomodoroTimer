import numpy as np
import time
import pygame as pg

class Sound():
    """Бип для звукового сигнала"""
    def __init__(self, duration = 300, frequence = 1000):
        self.duration = duration
        self.frequence = frequence
        self.sampleRate = 44100
        
    def play_sound(self):
        pg.mixer.init(44100,-16,2,512)
        arr = np.array([4096 * np.sin(2.0 * np.pi * self.frequence * x / self.sampleRate) for x in range(0, self.sampleRate)]).astype(np.int16)
        arr2 = np.c_[arr,arr]
        sound = pg.sndarray.make_sound(arr2)
        sound.play(-1)
        pg.time.delay(self.duration)
        sound.stop()
        
