import pandas as pd
import matplotlib.pyplot as plt
from kalman import Kalman

data = pd.read_csv("./output.csv").to_numpy()[:, 2]

while True:
    kf = Kalman(float(input("Q=")), float(input("R=")), 3) #1 1.3 3

    estimates = []

    for i in data:
        estimates.append(kf.estimate(i))

    x = range(len(data))
    plt.plot(x, data, label = "data")
    plt.plot(x, estimates, label = "estimate")
    plt.legend()
    plt.show()
    print("")