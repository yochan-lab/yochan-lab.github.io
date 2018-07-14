#!/usr/bin/env bash

'''
------
Auto-compile video page for Yochan
------
Author :: Tathagata Chakraborti
Date   :: 04/29/2018
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
def cache(filename = 'data.xlsx'):

	global data

	wb = xl.load_workbook(filename)

	for sheet_name in wb.sheetnames:

		dict_entry = {'short': {}, 'long': {}}

		idx = 0
		for row in wb[sheet_name]:

			if idx == 0: keys = [str(item.value).strip() for item in row]
			else:

				entry = [str(item.value).strip() for item in row]

				new_entry = {}
				for ent in entry:
					new_entry[keys[entry.index(ent)]] = ent

				dict_entry['long'][idx] = new_entry

				if not bool(int(new_entry['Collapsed'])):
					dict_entry['short'][idx] = new_entry

			idx += 1

		data[str(sheet_name)] = dict_entry


'''
method :: write index.html
'''
def write_file():

	# write individual sections

	def write_section(header, length):

		new_entry = ''

		for key in sorted(data[header][length].keys()):

			blob  = entry_blob
			paper = data[header][length][key]

			blob  = blob.replace('[ID]','collapse-{}-{}-{}'.format(key,header,length))
			blob  = blob.replace('[parent-ID]','accordion-{}-{}'.format(key,header,length))

			if paper['Paper'] == 'None':
				blob = blob.replace('[Paper]', 'disabled')
			else:
				blob = blob.replace('[Paper]', 'href="[Paper]" target="_blank"')

			for paper_keys in paper.keys():
				blob = blob.replace('[{}]'.format(paper_keys), paper[paper_keys])

			new_entry += blob

		return new_entry


	# cache data
	print 'Reading data...'
	cache()

	# write problem file
	print 'Compiling index.html ...'

	temp_content = ''

	for key in data.keys():

		name = ' '.join(key.split('-')[1:])

		print 'Writing section {} ...'.format(name)

		new_section   = section_blob

		short_section = write_section(key, 'short')
		long_section  = write_section(key, 'long')

		new_section   = new_section.replace('[Name]', name).replace('[ID]', key)

		new_section   = new_section.replace('[short]', '{}-{}'.format(key, 'short'))
		new_section   = new_section.replace('[long]', '{}-{}'.format(key, 'long'))

		new_section   = new_section.replace('[CONTENT-short]', short_section).replace('[CONTENT-long]', long_section)

		temp_content += new_section 

	with open('index_template.html', 'r') as index_template_file:
		index_template = index_template_file.read()

	index_template = index_template.replace('[CONTENT]', temp_content)
	index_template = index_template.replace('[DATE]', str(datetime.datetime.now()).split(' ')[0].strip())

	# write to output
	print 'Writing to file (../temp.html) ...'

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
	   
