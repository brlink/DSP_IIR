import numpy as np
from matplotlib import pyplot as plt

data = np.loadtxt('./data/data_collection.txt')
fft_data = np.fft.fft(data)
db = 20* np.log(fft_data)
xaxis = np.linspace(1, 100, len(data))
plt.plot(xaxis, db)
plt.show()