from regression import LinearRegression

class Kalman:
    K = 0
    P = 1

    def __init__(self, Q, R, N):
        self.Q = Q
        self.R = R
        self.N = N
        self.x = 0
        self.estimates = [0] * N
        self.regression = LinearRegression(self.estimates)
        self.findK()

    def setX(self, x):
        self.x = x

    def getX(self):
        return self.x

    def push(self, x):
        while len(self.estimates) >= self.N:
            self.estimates = self.estimates[1:]
        self.estimates.append(x)

    def estimate(self, measurement):
        self.regression.runLeastSquares()
        self.x += self.regression.predictNextValue() - self.estimates[len(self.estimates) - 1];
        self.x += self.K * (measurement - self.x)
        self.push(self.x)
        self.regression = LinearRegression(self.estimates)
        return self.x

    def findK(self):
        for _ in range(2000): self.solveDARE()

    def solveDARE(self):
        self.P = self.P + self.Q
        self.K = self.P / (self.P + self.R)
        self.P = (1 - self.K) * self.P