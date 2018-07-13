#!/usr/bin/env bash

'''
------
Auto-compile video page for Yochan
------
Author :: Tathagata Chakraborti
Date   :: 07/12/2018
------
'''


'''
packages
'''

import openpyxl as xl
import argparse, sys, random
import datetime

reload(sys)
sys.setdefaultencoding('utf-8')

'''
global variables 
'''

data = {} 

'''
html blobs 
'''

with open('section_blob.html', 'r') as section_blob_file:
	section_blob = section_blob_file.read()

with open('entry_blob.html', 'r') as entry_blob_file:
	entry_blob = entry_blob_file.read()


'''
method :: cache data from xlxs file
'''
def cache(filename = 'data/faim-18.xlsx'):

	global data

	wb = xl.load_workbook(filename)

	for sheet_name in wb.sheetnames:

		dict_entry = {}

		idx = 0
		for row in wb[sheet_name]:

			if idx == 0: keys = [str(item.value).strip() for item in row]
			else:

				entry = [str(item.value).strip() for item in row]

				new_entry = {}
				for ent in entry:
					new_entry[keys[entry.index(ent)]] = ent

				dict_entry[idx] = new_entry

			idx += 1

		data[str(sheet_name)] = dict_entry


'''
method :: write index.html
'''
def write_file():

	# write individual sections

	def write_section(header):

		new_entry = ''

		for key in sorted(data[header].keys()):

			blob  = entry_blob
			paper = data[header][key]

			blob  = blob.replace('[ID]','collapse-{}-{}'.format(key, header.replace(' ','-')))
			blob  = blob.replace('[parent-ID]','accordion-{}-{}'.format(key,header.replace(' ','-')))

			for paper_key in paper.keys():
				blob = blob.replace('[{}]'.format(paper_key), paper[paper_key])

			new_entry += blob

		return new_entry

	# cache data
	print 'Reading data...'
	cache()

	# write problem file
	print 'Compiling index.html ...'

	temp_content = ''

	for key in data.keys():

		print 'Writing section {} ...'.format(key)

		section       = write_section(key)

		new_section   = section_blob
		new_section   = new_section.replace('[Name]', key).replace('[ID]', key.replace(' ','-'))
		new_section   = new_section.replace('[CONTENT-ID]', key)
		new_section   = new_section.replace('[CONTENT]', section)

		temp_content += new_section 

	with open('index_template.html', 'r') as index_template_file:
		index_template = index_template_file.read()

	index_template = index_template.replace('[CONTENT]', temp_content)
	index_template = index_template.replace('[DATE]', str(datetime.datetime.now()).split(' ')[0].strip())

	# write to output
	print 'Writing to file (../index.html) ...'

	with open('../index.html', 'w') as output_file:
		output_file.write(index_template)

	print 'Done.'


'''
method :: main
'''
def main():

    parser = argparse.ArgumentParser(description='''Auto-compile video page for Yochan.''', epilog='''Usage >> python compile_page.py''')

    args = parser.parse_args()

    if '-h' in sys.argv[1:]:
        print parser.print_help()
        sys.exit(1)
    else:
		write_file()

if __name__ == "__main__":
	main()
	   
