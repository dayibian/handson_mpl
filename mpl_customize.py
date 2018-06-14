import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np

mpl.rcParams['lines.color'] = 'r'

data = np.random.randn(50)

plt.plot(data)
plt.show()