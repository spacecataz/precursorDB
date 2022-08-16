import matplotlib.pyplot as plt

plt.ylabel("Y-axis ")
plt.xlabel("X-axis ")

plt.plot([9, 5], [2, 5], [4, 7, 8])

plt.legend(["blue", "orange", "test"], frameon=True)

plt.show()