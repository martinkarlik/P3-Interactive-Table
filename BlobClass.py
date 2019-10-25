import cv2
import numpy as np

class Blob:

    def __init__(self):
        self.pixels = []
        self.area = 0
        self.compactness = 0
        self.circular = 0
        self.marker = False
        self.beer = False
        self.coloured = False
        self.minX = 0
        self.maxX = 0
        self.minY = 0
        self.maxY = 0

    def calcCompactness(self, area):
        return area / ((self.maxX - self.minX + 1) * (self.maxY - self.minY + 1))

    def is_beer(self, threshold):
        return self.circularity > threshold

    def is_marker(self, threshold):
        return self.compactness >= threshold
