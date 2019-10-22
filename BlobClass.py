import cv2
import numpy as np


class Blob:
    pixels = []
    area = 0
    compactness = 0
    circular = 0
    marker = False
    beer = False
    coloured = False
    minX = 0
    maxX = 0
    minY = 0
    maxY = 0

    def __init__(self):
        self.pixels = []

    def calcCompactness(self, area):
        return (area / ((self.maxX - self.minX + 1) * (self.maxY - self.minY + 1)))

    def isBeer(self, threshold):
        return self.circular > threshold

    def isMarker(self, threshold):
        return self.compactness >= threshold
