import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

clusters = pd.read_csv("../data/community_counts/community_counts_0.90_dropFalse.csv")

fig, ax1 = plt.subplots()

# color = 'tab:red'
ax1.set_xlabel('Year')
ax1.set_ylabel('Number of Detected Communities')
ax1.plot(clusters.Year, clusters.Communities, label='Communities')
# ax1.tick_params(axis='y', labelcolor=color)
# ax1.legend()

ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

# color = 'tab:blue'
color = 'tab:red'
ax2.set_ylabel('Number of Detected Communities with More than 10 Members')  # we already handled the x-label with ax1
ax2.plot(clusters.Year, clusters.More_than_10, color=color, label='Large Communities')
ax2.tick_params(axis='y')
ax2.set_ylim(3.5, 40)
fig.legend(loc="upper left", bbox_to_anchor=(0,1), bbox_transform=ax2.transAxes)

fig.tight_layout()  # otherwise the right y-label is slightly clipped
plt.show()
