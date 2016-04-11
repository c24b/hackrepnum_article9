import numpy as np
import matplotlib.pyplot as plt

np.random.seed(101)
a = np.random.normal(size=1000)
b = np.random.normal(size=1000)
c = np.random.normal(size=1000)

common_params = dict(bins=20, 
                     range=(-5, 5), 
                     normed=True)

plt.subplots_adjust(hspace=.4)
plt.subplot(311)
plt.title('Default')
plt.hist(a, **common_params)
plt.hist(b, **common_params)
plt.hist(c, **common_params)
plt.subplot(312)
plt.title('Skinny shift - 3 at a time')
plt.hist((a, b, c), **common_params)
plt.subplot(313)
common_params['histtype'] = 'step'
plt.title('With steps')
plt.hist(a, **common_params)
plt.hist(b, **common_params)
plt.hist(c, **common_params)

plt.savefig('3hist.png')
plt.show()
