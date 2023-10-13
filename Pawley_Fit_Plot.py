import re
import os
import argparse
from glob import glob
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.ticker import AutoMinorLocator,MultipleLocator

# Notes:
	# important code parts are highlighted with "CRITICAL!!!"

# DONE: 
	# Adapt args names.
	# File-finder has been revamped. Should work a lot better now.
	# data reader is finished. 

# TODO:
	# check behavior for legend_columns: Crashes on ncol > nvals?
	# implement class for plotting a single file first


sinfo = 'Plots the result of a TOPAS Pawley fit using the following output files: X_Yobs, X_Ycalc, X_Difference, 2Th_Ip.'
sname = os.path.basename(__file__)

defaults = {'input':'AUTOBATCH', # Specify the input for the script to plot.
			'silent':True, # run in silent mode.
			'multi_range':(0,0,1), # multiply 2theta angle range by a certain factor (START,END,FAC).
			'color_exp':'k', # color for experimental values.
			'color_cal':'r', # color for theoretical values.
			'color_pos':'b', # color for predicted reflection position values.
			'color_dif':'g', # color for experimental/theoretical values difference.
			'marker_exp_size':6, # size of black X-markers of the experimental data.
			'marker_pos_size':50, # size of the blue dashes for predicted reflection position values.
			'plot_size':(6,4), # set the size of the plot.
			'dots_per_inch':600, 
			'extension':'svg', # default output type in silent mode is svg.
			'legend_text_exp':'Observed', # set the legend text for the experimental values. 
			'legend_text_cal':'Calculated', # set the legend text for the theoretical values. 
			'legend_text_pos':'Reflections', # set the legend text for the predicted reflection position values. 
			'legend_text_dif':'Difference', # set the legend text for experimental/theoretical values difference.
			'legend_columns':1, # number of columns in the legend. 
			'size_axis_labels':12, # size of x/y-axis labels.
			'size_legend_labels':12, # size of the legend labels.
			'size_tick_labels':12, # size of axis tick labels.
			'size_multiply_label':12, # size of the multiplication number.
			'x_label_text':r'2\theta \quad / \quad°', # label for the x axis.
			'y_label_text':r'\mathrm{Intensity} \quad / \quad \mathrm{arb. units}', # label for the y axis.
			'x_step_width':10, # step size of the x axis (2theta angles)
			'x_axis_tolerance':0, # specify the tolerance of the x axis in angles.
			'vline_style':'-', # vertical multiply line style.
			'vline_strength':0.6 # strength of the vertical multiply line.
			}

# command line arguments.
parser = argparse.ArgumentParser(description=sinfo)
parser.add_argument('-i','--input', type=str, nargs='+',default=defaults['input'], help='Specify your input file.')
parser.add_argument('-s','--silent', action='store_true', default=False, help='Run in silent mode. This way only pictures are generated without opening a window.')
parser.add_argument('-m','--multi_range', type=float, nargs='+',default=(-100.,-100.,1), help='Multiply the intensities of the experimental and calculated dataset by a number. The given range of diffraction angles will be EXCLUDED from the multiplication. Specify: \"[START] [END] [FACTOR]\"')
parser.add_argument('-cexp','--color_exp', type=str, default=defaults['color_exp'], help='Set the color for experimental values: (_pawley_01_X_Yobs).')
parser.add_argument('-ccal','--color_cal', type=str, default=defaults['color_cal'], help='Set the color for calculated values: (_pawley_01_Out_X_Ycalc)')
parser.add_argument('-cpos','--color_pos', type=str, default=defaults['color_pos'], help='Set the color for X position values: (_pawley_01_2Th_Ip)')
parser.add_argument('-cdif','--color_dif', type=str, default=defaults['color_dif'], help='Set the color for difference values: (_pawley_01_X_Difference)')
parser.add_argument('-xs','--marker_exp_size', type=int, default=defaults['marker_exp_size'], help='Set the marker size of the experimental data (X markers).')
parser.add_argument('-ds','--marker_pos_size', type=int, default=defaults['marker_pos_size'], help='Set the marker size of the positional data (| markers).')
parser.add_argument('-size','--plot_size', type=float, default=defaults['plot_size'], nargs=2, help='Specify the plot size with a tuple \"[HEIGHT] [WIDTH]\" in inches.')
parser.add_argument('-dpi','--dots_per_inch',type=int, default=defaults['dots_per_inch'], help='Provide the image resolution in dots per inch.')
parser.add_argument('-ext','--extension',type=str,default=defaults['extension'],help='Specify the file type for your plot. Default is eps. To see which formats are supported, run the script and check the options under the save disc icon')
parser.add_argument('-lexp','--legend_text_exp', type=str, default=defaults['legend_text_exp'], help='Specify the legend text for the experimental intensities.')
parser.add_argument('-lcal','--legend_text_cal', type=str, default=defaults['legend_text_cal'], help='Specify the legend text for the calculated intensities.')
parser.add_argument('-lpos','--legend_text_pos', type=str, default=defaults['legend_text_pos'], help='Specify the legend text for the expected diffraction angles.')
parser.add_argument('-ldif','--legend_text_dif', type=str, default=defaults['legend_text_dif'], help='Specify the legend text for the intensity differences.')
parser.add_argument('-lcol','--legend_columns',type=int, default=defaults['legend_columns'], help='Specify the number of columns in the legend.')
parser.add_argument('-slab','--size_axis_labels', type=int, default=defaults['size_axis_labels'], help='Specify the size of the axis labels.')
parser.add_argument('-sleg','--size_legend_labels', type=int, default=defaults['size_legend_labels'], help='Specify the size of the legend labels.')
parser.add_argument('-stic','--size_tick_labels', type=int, default=defaults['size_tick_labels'], help='Specify the size of the tick labels.')
parser.add_argument('-smul','--size_multiply_label', type=int, default=defaults['size_multiply_label'], help='Specify the size of the multiplicator_text.')
parser.add_argument('-xlab','--x_label_text', type=str, default=defaults['x_label_text'], help='Specify the x label. This option evaluates LaTeX code so that Greek letters can be specified as well (e.g. \\Delta). Most basic math mode codes should be recognized, but not all. ALWAYS surround LaTeX code with Quotes (\").')
parser.add_argument('-ylab','--y_label_text', type=str, default=defaults['y_label_text'], help='Specify the y label. This option evaluates LaTex code so that Greek letters can be specified as well (e.g. \\Delta). Most basic math mode codes should be recognized, but not all. ALWAYS surround LaTeX code with Quotes (\").')
parser.add_argument('-xstep','--x_step_width', type=int, default=defaults['x_step_width'], help='Specify the step width of the x axis.')
parser.add_argument('-xtol','--x_axis_tolerance', type=float, default=defaults['x_axis_tolerance'], help='Specify the tolerance of the x-axis in degrees (absolute values).')
parser.add_argument('-vsty','--vline_style', type=str, default=defaults['vline_style'], help='Specify the line style of the vertical multiplication lines. Options: do = dotted, da = dashed.')
parser.add_argument('-vstr','--vline_strength', type=float, default=defaults['vline_strength'], help='Specify the thickness of vertical multiplication lines.')
args = parser.parse_args()


# 1. find input files
def get_input_files(inps='AUTOBATCH'):

	'''Finds the relevant input files based on input string.'''

	def add_files_to_files_dict(data_files, dirpath, files_dict):
# 
		'''Fills the files_dict var with entries for the different input files.'''

		for file in data_files:
			sep = re.search(r'_pawley_\d+_',file).group() # find out separator between name and input file type
			name, typ = file.split(sep) # split filename by separator
			typ = os.path.splitext(typ)[0] # remove extension from type name 

			if name not in files_dict.keys(): files_dict[name] = {} # create new entry if not present.

			files_dict[name][typ] = os.path.join(dirpath,file) # add type files to data dict.



	files_dict = {} # return

	if inps == 'AUTOBATCH':
		all_files = os.listdir() # find all files in the current dir.
		data_files = [file for file in all_files if '_pawley_' in file.lower() and os.path.splitext(file)[-1] == '.txt'] # find all files with the '_pawley_' substring. CRITICAL!!!
		add_files_to_files_dict(data_files,'',files_dict) # add no dirpath, since it will search where the script is.

	else:
		for inp in inps: # manual specification of input files returns a list 
			if not os.path.exists(inp): # quit if the provided input is not a valid file.
				print('The input file %s could not be found.'%inp)
				sys.exit('Exiting ')

			# run this if boolean check didn't call sys.exit(). 
			dirname = os.path.dirname(inp)
			file = os.path.basename(inp)
			filename = os.path.splitext(file)[0]
			data_files = [file for file in os.listdir(dirname) if filename in file and os.path.splitext(file)[-1] == '.txt']
			add_files_to_files_dict(data_files,dirname,files_dict)
	
	return files_dict



# 2. read in input and return data
def get_data(paths_dict):

	'''Reads in data files and returns the appropriate data arrays/dataframes...we'll see.'''

	data = {} # to return
	names_to_sensible = {'x_yobs':'exp', # i hate the names of the data that TOPAS uses...
						 'out_x_ycalc':'cal',
						 'x_difference':'dif',
						 '2th_ip':'pos'} 

	for typ in paths_dict:
		df = pd.read_csv(paths[typ],delim_whitespace=True,header=None,dtype=float)
		df.columns = ('x','y')

		name = names_to_sensible[typ.lower()] # convert the names of TOPAS to better names.

		data[name] = [df['x'],df['y']]

	return data



class PlotPawleyFit: # Should I use a parent class?

	def __init__(self,data): # needs the data sets to plot a single graph.

		self.data = data # receive num data for plotting. 


	def plot(self): # need to decide on args for this method.

		'''Make the default plot according to directly passable commandline args.'''

		fig = plt.figure(figsize=args.plot_size)  # create canvas.
		gs = gridspec.GridSpec(3, 1, height_ratios=[4, 1, 1]) # make stacked multiplot for exp+cal // pos // dif

		# attribute subplots to variables.
		ax1 = plt.subplot(gs[0]) # exp+cal
		ax2 = plt.subplot(gs[1]) # pos
		ax3 = plt.subplot(gs[2]) # dif

		plt.subplots_adjust(hspace=0.0) # reduce space between subplots to zero

		# plot the different data values.
		ax1.plot(self.data['exp'][0], self.data['exp'][1], 'kx',label='Observed')
		ax1.plot(self.data['cal'][0], self.data['cal'][1], label='Calculated')
		ax2.plot(self.data['pos'][0], np.zeros(len(self.data['pos'][0])), label='Reflections')
		ax3.plot(self.data['dif'][0], self.data['dif'][1], label='Difference')

		# Hide horizontal lines between subplots
		ax1.spines['bottom'].set_visible(False)
		ax2.spines['top'].set_visible(False)
		ax2.spines['bottom'].set_visible(False)
		ax3.spines['top'].set_visible(False)

		plt.show()


	def add_style(self): 

		'''Will add formatting options to the produced plot.'''

		pass




# Main loop
files_dict = get_input_files(args.input)

for entry in files_dict:
	paths = files_dict[entry]
	
	if len(paths) != 4: # quit if data file missing. check get_input_files() for mistakes.
		print('ERROR! %s FOUND %s INPUT FILES FOR THE INPUT GROUP %s INSTEAD OF 4!'%(sname,len(paths),entry))
		sys.exit('Exiting %s...'%sname)
	
	data = get_data(paths) # get all the data from the four input files.

	plot_obj = PlotPawleyFit(data) # create plot object.
	plot_obj.plot() # call the plot method.


	
