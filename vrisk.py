def fmp_historical(stock):
    key = ''
    return f'https://financialmodelingprep.com/stable/historical-price-eod/light?symbol={stock}&apikey={key}'

# Value At Risk with Geometric Brownian Motion
# x = alpha, y = time, z = VaR

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt 
from mpl_toolkits.mplot3d import Axes3D
import ctypes
import requests

quant = ctypes.CDLL("./vrisk.so")
quant.VaR.argtypes = [
    ctypes.c_double,
    ctypes.c_double,
    ctypes.c_double,
    ctypes.c_double,
    ctypes.c_int
]
quant.VaR.restype = ctypes.POINTER(ctypes.c_double)

quant.free_memory.argtypes = [ctypes.POINTER(ctypes.c_double)]

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

stock = 'TSLA'
prices = pd.DataFrame(requests.get(fmp_historical(stock)).json())['price'][::-1].values
returns = prices[1:]/prices[:-1] - 1.0
N = 200
M = 40

S0 = prices[-1]
drift = np.mean(returns)
volt = np.std(returns)

t = 10 / 365.0

T = np.linspace(1, 100, M)
A = np.linspace(0.01, 0.1, M)

XT, YT = np.meshgrid(A, T)
Z = np.zeros((M, M))

for i in range(M):
    for j in range(M):
        print(i, j)
        alpha = XT[i, j]
        t = YT[i, j] / 252.0
        I = int(alpha*N)
        result = quant.VaR(S0, drift, volt, t, N)
        VaR = [result[i] for i in range(N)]
        VaR = list(sorted(VaR))
        val_at_risk = VaR[I]
        Z[i, j] = val_at_risk

        quant.free_memory(result)

ax.set_title(f"Value At Risk Simulation for {stock}")
ax.plot_surface(XT, YT, Z, cmap='jet_r')
ax.set_xlabel('Alpha')
ax.set_ylabel('Time')
ax.set_zlabel('Value At Risk')
plt.show()