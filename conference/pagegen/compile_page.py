#!/usr/bin/env bash

'''
------
Auto-compile conference page for Yochan
------
Author :: Tathagata Chakraborti
Date   :: 07/12/2018
------
'''


'''
packages
'''

import openpyxl as xl
import argparse, sys, os
import datetime

'''
global variables 
'''

data = {} 
conference_header = None

'''
html blobs 
'''

with open('section_blob.html', 'r') as section_blob_file:
    section_blob = section_blob_file.read()

with open('entry_blob.html', 'r') as entry_blob_file:
    entry_blob = entry_blob_file.read()

with open('news_blob.html', 'r') as news_blob_file:
    news_blob = news_blob_file.read()

'''
method :: cache data from xlxs file
'''
def cache(filename):

    global data, conference_header

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

                if new_entry['Title'] != 'None':
                    dict_entry[idx] = new_entry

            idx += 1

        data[str(sheet_name)] = dict_entry
        conference_header = sheet_name

        break


'''
method :: write index.html
'''
def write_file(filename: str = None, conference_name: str = None):

    # write individual sections

    def write_section(header):

        new_entry = ''

        for key in sorted(data[header].keys()):

            blob  = entry_blob
            paper = data[header][key]

            blob  = blob.replace('[ID]','collapse-{}-{}'.format(key, header.replace(' ','-')))
            blob  = blob.replace('[parent-ID]','accordion-{}'.format(header.replace(' ','-')))

            blob = blob.replace('[Paper]', 'href="[Paper]" target="_blank"')
            for paper_key in paper.keys():
                if paper_key != "News":
                    blob = blob.replace('[{}]'.format(paper_key), paper[paper_key])

            temp = ""
            if "News" in paper:
                if paper["News"].strip() != "None":
       
                    news_data = paper["News"].split('[DELIM]')

                    for news in news_data:
                        news_header = news.split('[HEADER]')[0].strip()
                        news_link = news.split('[HEADER]')[1].strip()

                        temp += news_blob.replace('[Link]', news_link).replace('[Header]', news_header)

            blob = blob.replace('[News]', temp)                
            new_entry += blob

        return new_entry

    # cache data
    print( 'Reading data...' )
    cache( filename )

    # write problem filea
    print( 'Compiling index.html ...' )

    temp_content = ''

    for key in data.keys():

        print( 'Writing section {} ...'.format(key) )

        section       = write_section(key)

        new_section   = section_blob
        new_section   = new_section.replace('[Name]', key).replace('[ID]', key.replace(' ','-'))
        new_section   = new_section.replace('[CONTENT-ID]', key.replace(' ','-'))
        new_section   = new_section.replace('[CONTENT]', section)

        temp_content += new_section 

    with open('index_template.html', 'r') as index_template_file:
        index_template = index_template_file.read()

    index_template = index_template.replace('[HEADER]', conference_header)

    index_template = index_template.replace('[CONTENT]', temp_content)
    index_template = index_template.replace('[DATE]', str(datetime.datetime.now()).split(' ')[0].strip())

    # write to output
    print( 'Writing to file (../{}.html) ...'.format(conference_name) )

    try:    os.mkdir( '../'+ conference_name )
    except: pass

    with open('../{}/index.html'.format(conference_name), 'w') as output_file:
        output_file.write(index_template)

    print( 'Done.' )


'''
method :: main
'''
def main():

    parser = argparse.ArgumentParser(description='''Auto-compile conference page for Yochan.''', epilog='''Usage >> python3 compile_page.py''')

    parser.add_argument('-f', '--filename', type=str, help='path to data file')
    parser.add_argument('-c', '--name', type=str, help='name of conference to be used in url')

    args = parser.parse_args()

    if '-h' in sys.argv[1:]:
        print( parser.print_help() )
        sys.exit(1)
    else:
        write_file(filename = args.filename, conference_name = args.name)

if __name__ == "__main__":
    main()
       
