#!/usr/bin/python

"""
A script to download stock prices from Yahoo
ie. from a url like http://finance.yahoo.com/q?s=GOOG
"""

import http.cookiejar
import urllib.request, urllib.parse, urllib.error
import urllib.request, urllib.error, urllib.parse
from bs4 import BeautifulSoup

import csv
import os
import sys
import time

def get_stock_html(ticker_name):
    opener = urllib.request.build_opener(
            urllib.request.HTTPRedirectHandler(),
            urllib.request.HTTPHandler(debuglevel=0),
        )
    opener.addheaders = [
        ('User-agent', 
         "Mozilla/4.0 (compatible; MSIE 7.0; "
         "Windows NT 5.1; .NET CLR 2.0.50727; "
         ".NET CLR 3.0.4506.2152; .NET CLR 3.5.30729)")
    ]
    url = "http://finance.yahoo.com/q?s=" + ticker_name
    response = opener.open(url)
    return b''.join(response.readlines()).decode('utf-8')

def find_quote_section(html):
    soup = BeautifulSoup(html, "html.parser")
    quote = soup.find('div', attrs={'class': 'yfi_quote_summary'})
    return quote
    
def parse_stock_html(html):
    quote = find_quote_section(html)
    result = {}
    
    # <h2>Google Inc.</h2>
    result['stock_name'] = quote.find('h2').contents[0]
    
    ### After hours values
    # <span id="yfs_l91_goog">329.94</span>
    result['ah_price'] = quote.find('span', attrs={'id': 'yfs_l91_goog'}).string
    
    # <span id="yfs_z08_goog">
    # ... <span class="yfi-price-change-down">0.22</span>
    print(quote.find(attrs={'id': 'yfs_z08_goog'}))
    print(quote.find(attrs={'id': 'yfs_z08_goog'}).contents)
    result['ah_change'] = (quote.find(attrs={'id': 'yfs_z08_goog'}).contents[-1])
        #).
        #find(attrs={'class': ['yfi-price-change-up', 'yfi-price-change-down']}).contents)
    
    ### Current values
    # <span id="yfs_l10_goog">330.16</span>
    result['last_trade'] = quote.find('span', attrs={'id': 'yfs_l10_goog'}).string
    
    # <span id="yfs_c10_goog" class="yfi_quote_price">
    # ... <span class="yfi-price-change-down">1.06</span>
    def is_price_change(value):
        return (value is not None and
            value.strip().lower()
                 .startswith('yfi-price-change'))
            
    result['change'] = (quote.
        find(attrs={'id': 'yfs_c10_goog'}).
        find(attrs={'class': is_price_change}).string)
    
    return result


fields = {'date' : "Date",
          'last_trade' : 'Last Trade',
          'change' : 'Change',
          'ah_price' : 'After Hours Price',
          'ah_change' : 'After Hours Change'}

def write_row(ticker_name, row):
    file_name = "stocktracker-" + ticker_name + ".csv"
    if os.access(file_name, os.F_OK):
        file_mode = 'ab'
    else:
        file_mode = 'wb'
    
    csv_writer = csv.DictWriter(
        open(file_name, file_mode),
        fieldnames=list(fields.keys()),
        extrasaction='ignore')
        
    if file_mode == 'wb':
        csv_writer.writerow(fields)
    
    csv_writer.writerow(stock_values)
    
    
if len(sys.argv) > 1:
    ticker_name = sys.argv[1]
    ticker_name = ticker_name.upper()
    ticker_name = ''.join(
        [char for char in ticker_name
        if char in "ABCDEFGHIJKLMNOPQRSTUVWXYZ"])
    if len(ticker_name) not in [3, 4]:
        raise ValueError("Invalid ticker name: " + ticker_name)
        
    html = get_stock_html(ticker_name)
    print(find_quote_section(html))
    
    stock_values = parse_stock_html(html)
    stock_values['date'] = time.strftime("%Y-%m-%d %H:%M")
    # del stock_values['stock_name']
    
    write_row(ticker_name, stock_values)
    
    print(stock_values)
    
else:
    html = ''.join(sys.stdin.readlines())
    print(parse_stock_html(html))


