#!/usr/bin/env python

'''
+ script to pull all emojis from slackmojis.com
+ emojis are saved in images/ 
+ upload to slack using Bulk Emoji Uploader extension for Slack on Chrome
'''

import re, requests
import os, errno

valid_emoji_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.ico', '.txt', '.svg', '.bmp']

def download_emojis():

    with open('slackmojis.html', 'wb') as handle:
        response = requests.get('https://slackmojis.com/', stream=True)

        if not response.ok:
            print response

        for block in response.iter_content(1024):
            if not block:
                break

            handle.write(block)

    with open('slackmojis.html', 'r') as temp:
        slackmojis_page_html = temp.read()

    url_re = re.findall(r'<a href=[\'"]?([^\'" >]+)', slackmojis_page_html)

    url_list = set()
    for url_string in url_re:
        if any(ext in url_string for ext in valid_emoji_extensions):
            url_list.add(url_string)

    total_count = len(url_list)
    current_count = 0

    for url in url_list:

            image_name = url[url.rfind("/")+1:url.rfind("?")]

            current_count += 1
            print 'processing {}/{} ... image: {}'.format(current_count, total_count, image_name)

            filename = 'images/' + image_name 

            if not os.path.exists(os.path.dirname(filename)):
                try:
                    os.makedirs(os.path.dirname(filename))
                except OSError as exc: # guard against race condition
                    if exc.errno != errno.EEXIST:
                        raise

            with open(filename, 'wb') as handle:
                response = requests.get(url, stream=True)

                if not response.ok:
                    print 'FAILED', image_name, response

                for block in response.iter_content(1024):
                    if not block:
                        print 'FAILED', image_name, response
                        break

                    handle.write(block)


if __name__ == '__main__':
    download_emojis()
