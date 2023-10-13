import os
import re


all_files = os.listdir() # find all files in the current dir.
data_files = [file for file in all_files if '_pawley_' in file.lower() and os.path.splitext(file)[-1] == '.txt'] # find all files with the '_pawley_' substring. CRITICAL!!!


data_dict = {}

for file in data_files:
	sep = re.search(r'_pawley_\d+_',file).group()
	name, typ = file.split(sep)
	typ = os.path.splitext(typ)[0]

	if name not in data_dict.keys(): data_dict[name] = {}

	data_dict[name][typ] = file

print(data_dict)


	




# filesdict = {part[0]:{} for part in parts}

# input_files_batch = [(name+'_pawley_'+) for name in names] # AAAAAAAAAAAAAAAAAAAA