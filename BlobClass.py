import cv2
import numpy as np

class Blob:

    def __init__(self):
        self.pixels = []
        self.area = 0
        self.compactness = 0
        self.circularity = 0
        self.marker = False
        self.beer = False
        self.coloured = False
        self.min_x = 0
        self.max_x = 0
        self.min_y = 0
        self.max_y = 0

    def calc_compactness(self, area):
        return area / ((self.max_x - self.min_x + 1) * (self.max_y - self.min_y + 1))

    def is_beer(self, threshold):
        return self.circularity > threshold

    def is_marker(self, threshold):
        return self.compactness >= threshold
