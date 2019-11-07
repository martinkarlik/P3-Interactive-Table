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
        self.centerX = 0
        self.centerY = 0

    def calcCompactness(self, area):
        return area / ((self.maxX - self.minX + 1) * (self.maxY - self.minY + 1))

    def isBeer(self, threshold):
        return self.circular > threshold

    def isMarker(self, threshold):
        return self.compactness >= threshold

    @staticmethod
    def iAmStatic():
        print("static")