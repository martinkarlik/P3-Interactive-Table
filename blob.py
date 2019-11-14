class Blob:

    def __init__(self, pixels):
        self.pixels = pixels
        self.area = len(pixels)
        self.compactness = 0
        self.circular = 0
        self.marker = False
        self.beer = False
        self.coloured = False
        self.bounding_box = self.findBoundingBox()
        self.center = self.findCenter()

    def calcCompactness(self, area):
        return area / ((self.max_x - self.min_x + 1) * (self.max_y - self.min_y + 1))

    def isBeer(self, threshold):
        return self.circular > threshold

    def isMarker(self, threshold):
        return self.compactness >= threshold

    def findBoundingBox(self):
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

    def findCenter(self):
        return [int((self.bounding_box[0] + self.bounding_box[2]) / 2), int((self.bounding_box[1] + self.bounding_box[3]) / 2)]

    @staticmethod
    def iAmStatic():
        print("no you aint ya bitch")





