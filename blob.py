import numpy as np

class Blob:

    def __init__(self, pixels):
        self.pixels = pixels
        self.area = len(pixels)

        self.bounding_box = self.find_bounding_box()
        self.center = self.find_center()
        self.mean = self.find_mean()

        self.is_beer = self.is_beer()
        self.is_marker = self.is_marker()



    def find_bounding_box(self):
        min_y = self.pixels[0][0]
        min_x = self.pixels[0][1]
        max_y = self.pixels[0][0]
        max_x = self.pixels[0][1]

        for pixel in self.pixels:

            if pixel[0] < min_y:
                min_y = pixel[0]
            if pixel[0] > max_y:
                max_y = pixel[0]
            if pixel[1] < min_x:
                min_x = pixel[1]
            if pixel[1] > max_x:
                max_x = pixel[1]

        return [min_y, min_x, max_y, max_x]

    def find_center(self):
        return [int((self.bounding_box[0] + self.bounding_box[2]) / 2), int((self.bounding_box[1] + self.bounding_box[3]) / 2)]

    def find_mean(self):
        sum_x = 0
        sum_y = 0
        for p in self.pixels:
            sum_x += p[1]
            sum_y += p[0]

        return [int(sum_y / self.area), int(sum_x / self.area)]

    def get_compactness(self):
        return self.area / (self.bounding_box[3] - self.bounding_box[1] + 1) * (self.bounding_box[2] - self.bounding_box[0] + 1)

    def get_circularity(self):
        return 1

    def is_beer(self):
        return self.area > 10 and self.get_circularity() > 0.7

    def is_marker(self):
        return self.area > 100 and self.get_compactness() > 0.7
