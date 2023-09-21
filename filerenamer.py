# Python3 code to rename multiple
# files in a directory or folder
import glob
import os
import logging
import configparser
import pandas as pd
import re


def rename(path, old, new):
	for f in os.listdir(path):
		os.rename(os.path.join(path, f), os.path.join(path, f.replace(old, new)))


def main():
	# Read config
	config = configparser.ConfigParser()
	config.read('config.ini')
	source_file = config["FILE"]["SOURCE_FILE"]
	log_file = config["LOGGING"]["LOG_FILE"]
	log_level = logging.getLevelName(config["LOGGING"]["LOG_LEVEL"])
	regex = re.compile(config["FILE"]["REGEX"])
	# regex = re.compile(r"(.*-.*-.*-)(.*?-.\d*)(.*)")

	# logger
	logger = logging.getLogger('filefinder')
	logger.setLevel(log_level)
	fh = logging.FileHandler(log_file, mode="w", encoding="UTF-8")
	fh.setLevel(log_level)
	ch = logging.StreamHandler()
	ch.setLevel(log_level)
	formatter = logging.Formatter('%(levelname)s - %(asctime)s - %(message)s')
	fh.setFormatter(formatter)
	ch.setFormatter(formatter)
	logger.addHandler(fh)
	logger.addHandler(ch)

	dtype_dic = {'subject_id': str, 'subject_number': 'float'}
	data = pd.read_excel(source_file, dtype=object)

	files = [glob.glob(e) for e in ['*.jpg', '*.tif']]
	for imagetype in files:
		for f in imagetype:
			for row in data.itertuples():
				# logger.debug(f)
				# logger.debug(row.ImageTitleOld)
				if f == row.ImageTitleOld:
					match = re.search(regex, f)
					newname = (
						str(match[1])
						+ str(row.AccessionNumber).replace('SMNS_DIP_', '')
						+ str(match[3])
					)
					os.rename(f, newname)
					logger.info('Renamed ' + f + ' to ' + newname)


if __name__ == '__main__':
	main()
