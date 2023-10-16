import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

fig = plt.figure(figsize=(6, 4), constrained_layout=False) # set this to true
gs = gridspec.GridSpec(3, 1, height_ratios=[1,1,1])

ax1 = plt.subplot(gs[0])
ax2 = plt.subplot(gs[1])
ax3 = plt.subplot(gs[2])

ax1.plot([1, 2, 3], [3, 2, 1], label='Subplot 1')
ax2.plot([1, 2, 3], [1, 2, 3], label='Subplot 2')
ax3.plot([1, 2, 3], [2, 1, 2], label='Subplot 3')


print("Original height ratios:", gs.get_height_ratios())

new_height_ratios = [5, 1, 1]
gs.set_height_ratios(new_height_ratios)

print("Updated height ratios:", gs.get_height_ratios())

# plt.tight_layout() # uncomment this

plt.show()