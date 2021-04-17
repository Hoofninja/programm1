import matplotlib.pyplot as plt
import os
import pygame
import sys


class Field(pygame.sprite.Sprite):

    # Init variables, X and Y lists
    def __init__(self, x, y, file_name):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.file_name = file_name

    # Plot X Y graphic
    def graph(self):
        plt.plot(self.x, self.y)
        plt.title(self.file_name)
        plt.show()

    # Detects the presence of a peak
    def peak(self, left_x, right_x, min_max) -> bool:
        x_temp = []
        y_temp = []
        for i in range(len(self.x)):
            if left_x < self.x[i] < right_x:
                x_temp.append(self.x[i])
                y_temp.append(self.y[i])
        multiplier = min_max[0]
        min_max = float(min_max.replace(min_max[0], ""))
        if multiplier == "*":
            peak_value = min(y_temp) * min_max
        if multiplier == "+":
            peak_value = min(y_temp) + min_max
        if multiplier == "-":
            peak_value = min(y_temp) - min_max
        if multiplier == "/":
            peak_value = min(y_temp) / min_max

        tg = False
        if max(y_temp) != (y_temp[0] or y_temp[-1]):
            tg = True

        if (max(y_temp) >= peak_value) and (tg is True):
            return True
        else:
            return False
