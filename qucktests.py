import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.ticker import AutoMinorLocator,MultipleLocator


class PlotPawleyFit: # Should I use a parent class?

	def __init__(self): # needs the data sets to plot a single graph.

		l = np.linspace(0,50,1000)
 
		self.data = {'exp':(l,np.sin(l)),'cal':(l,np.sin(l)),'dif':(l,np.sin(l)),'pos':(l,np.sin(l))}



	def plot(self): # need to decide on args for this method.

		'''Make the default plot according to directly passable commandline args.'''

		def plot_style(ax1,ax2,ax3,lims):

			'''Define the style of the plot. A bit weird, but this way it's all in one place.'''

			for ax in (ax1,ax2,ax3):
				ax.set_yticks(()) # remove yticks
				ax.set_xlim(0,0.00001) # set x axis limits 
			

			ax1.set_xticks(())


		fig = plt.figure()  # create canvas.
		gs = gridspec.GridSpec(3, 1, height_ratios=[8, 1, 2]) # make stacked multiplot for exp+cal // pos // dif

		# attribute subplots to variables.
		ax1 = plt.subplot(gs[0]) # exp+cal
		ax2 = plt.subplot(gs[1]) # pos
		ax3 = plt.subplot(gs[2]) # dif

		plt.subplots_adjust(hspace=0.0) # reduce space between subplots to zero

		# plot the different data values.
		exp = ax1.plot(self.data['exp'][0], self.data['exp'][1], ls='' ,marker='x', color='k', label='Observed')
		cal = ax1.plot(self.data['cal'][0], self.data['cal'][1], ls='-' ,marker='', color='r', label='Calculated')
		pos = ax2.plot(self.data['pos'][0], np.zeros(len(self.data['pos'][0])), ls='' ,marker='|', ms=5, color='b', label='Reflections')
		dif = ax3.plot(self.data['dif'][0], self.data['dif'][1], ls='-' ,marker='', color='g', label='Difference')

		lims = min(self.data['exp'][0]), max(self.data['exp'][0])
		plot_style(ax1,ax2,ax3,lims) # set plot style

		plt.show()



f = PlotPawleyFit()
f.plot()