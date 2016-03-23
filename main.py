import training
import pickle
import json
import io
import sys

def split_data_in_file(data_filename, flag_print_split):
	data=''
	num_obj=0
	with io.open(data_filename,'r', encoding='utf8') as f:
		fwrite=[io.open('data/compression_data_%d.json'%i,'a') for i in range(5)]
		for line in f:
			if line in ['\n','\n\r']:
				data+=line
				fwrite[num_obj%5].write(data)
				num_obj+=1
				data=''
				if flag_print_split=='1':
					print('Done %d object'%num_obj)
			else:
				data+=line
		fwrite[0].write(data)
		print('Done')

def training_5fold(list_filename):
	list_name
	for i in range(5):
		

if __name__=='__main__':
	flag_print_split = sys.argv[1]
	split_data_in_file('data/compression-data.json', flag_print_split)
