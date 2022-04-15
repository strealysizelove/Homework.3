# -*- coding: utf-8 -*-
"""
Created on Sun Apr 10 21:40:17 2022

@author: Strealy Sizelove
"""

# STK LULU
# Import requests to retrive Web Urls example HTML. TXT 
import requests

# Import BeautifulSoup
from bs4 import BeautifulSoup

# import re module for REGEXes
import re

# import pandas
import pandas as pd

# Get the HTML data from the 2018 10-K from Apple
r = requests.get('https://www.sec.gov/Archives/edgar/data/0001397187/000139718718000013/lulu-20180128x10k.txt')
raw_10k = r.text

print(raw_10k[0:1300])

# Regex to find <DOCUMENT> tags
doc_start_pattern = re.compile(r'<DOCUMENT>')
doc_end_pattern = re.compile(r'</DOCUMENT>')
# Regex to find <TYPE> tag prceeding any characters, terminating at new line
type_pattern = re.compile(r'<TYPE>[^\n]+')

# Create 3 lists with the span indices for each regex

doc_start_is = [x.end() for x in doc_start_pattern.finditer(raw_10k)]
doc_end_is = [x.start() for x in doc_end_pattern.finditer(raw_10k)]

doc_types = [x[len('<TYPE>'):] for x in type_pattern.findall(raw_10k)]

document = {}

# Create a loop to go through each section type and save only the 10-K section in the dictionary
for doc_type, doc_start, doc_end in zip(doc_types, doc_start_is, doc_end_is):
    if doc_type == '10-K':
        document[doc_type] = raw_10k[doc_start:doc_end]
        
# display excerpt the document
document['10-K'][0:500]

# Write the regex
regex = re.compile(r'(>Item(\s|&#160;|&nbsp;)(1A|1B|7A|7|8)\.{0,1})|(ITEM\s(1A|1B|7A|7|8))')

# Use finditer to math the regex
matches = regex.finditer(document['10-K'])

# Write a for loop to print the matches
for match in matches:
    print(match)
    
    # Matches
matches = regex.finditer(document['10-K'])

# Create the dataframe
test_df = pd.DataFrame([(x.group(), x.start(), x.end()) for x in matches])

test_df.columns = ['item', 'start', 'end']
test_df['item'] = test_df.item.str.lower()

# Display the dataframe
test_df.head()

# Get rid of unnesesary charcters from the dataframe
test_df.replace('&#160;',' ',regex=True,inplace=True)
test_df.replace('&nbsp;',' ',regex=True,inplace=True)
test_df.replace(' ','',regex=True,inplace=True)
test_df.replace('\.','',regex=True,inplace=True)
test_df.replace('>','',regex=True,inplace=True)

# display the dataframe
test_df.head()

# Drop duplicates
pos_dat = test_df.sort_values('start', ascending=True).drop_duplicates(subset=['item'], keep='last')

# Display the dataframe
pos_dat

# Get Item 1a
item_1a_raw = document['10-K'][pos_dat['start'].loc['item1a']:pos_dat['start'].loc['item1b']]

# Get Item 7
item_7_raw = document['10-K'][pos_dat['start'].loc['item7']:pos_dat['start'].loc['item7a']]

# Get Item 7a
item_7a_raw = document['10-K'][pos_dat['start'].loc['item7a']:pos_dat['start'].loc['item8']]

item_1a_raw[0:1000]

item_1a_content = BeautifulSoup(item_1a_raw, 'lxml')

print(item_1a_content.prettify()[0:1000])

print(item_1a_content.get_text("\n\n"))
