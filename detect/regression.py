class LinearRegression:
    m = 0.0
    b = 0.0

    def __init__(self, y):
        self.y = y
        self.x = [i for i in range(len(y))]

    def runLeastSquares(self):
        n = len(self.x)
        xySum = 0
        for i in range(len(self.x)):
            xySum += self.x[i] * self.y[i]
        m1 = n * xySum - sum(self.x) * sum(self.y)
        x_squaredSum = 0
        for v in self.x:
            x_squaredSum += v ** 2
        m2 = n * x_squaredSum - sum(self.x) ** 2
        self.m = m1 / m2
        self.b = sum(self.y) - self.m * sum(self.x)
        self.b /= n
    
    def predictNextValue(self):
        return len(self.x) * self.m + self.b