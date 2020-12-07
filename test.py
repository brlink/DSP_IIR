import numpy as np
from matplotlib import pyplot as plt
import pickle

data = open('./data/data_orignal_storage.dat', 'rb')
d = pickle.load(data)
data.close()
fft_data = np.fft.fft(d)
db = 20* np.log(fft_data)
xaxis = np.linspace(1, 100, len(d))
plt.plot(xaxis, db)
#plt.plot(data)
plt.show()