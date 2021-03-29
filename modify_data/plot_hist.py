import matplotlib.pyplot as plt
import numpy as np

values  = []
with open('all.txt') as f:
	values = [x.strip() for x in f.readlines()]
values = np.array(values).astype(np.float)
n_bins = 500

print(np.mean(values), np.std(values))

plt.title('Histogram of frequencies with bins = '+str(n_bins))
plt.xlabel('Fatness values')
plt.ylabel('Frequency')
plt.hist(values, bins=n_bins)
plt.show()