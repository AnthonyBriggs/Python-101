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
import tempfile
import time

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


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
    
def parse_stock_html(html, ticker_name):
    quote = find_quote_section(html)
    result = {}
    tick = ticker_name.lower()
    
    # <h2>Google Inc.</h2>
    result['stock_name'] = quote.find('h2').contents[0]
    
    ### After hours values
    # <span id="yfs_l91_goog">329.94</span>
    print(tick)
    print(quote.find('span', attrs={'id': 'yfs_l91_'+tick}))
    result['ah_price'] = quote.find('span', attrs={'id': 'yfs_l91_'+tick}).string
    
    # <span id="yfs_z08_goog">
    # ... <span class="yfi-price-change-down">0.22</span>
    print(quote.find(attrs={'id': 'yfs_z08_'+tick}))
    print(quote.find(attrs={'id': 'yfs_z08_'+tick}).contents)
    result['ah_change'] = (quote.find(attrs={'id': 'yfs_z08_'+tick}).contents[-1])
    
    ### Current values
    # <span id="yfs_l10_goog">330.16</span>
    result['last_trade'] = quote.find('span', attrs={'id': 'yfs_l10_'+tick}).string
    
    # <span id="yfs_c10_goog" class="yfi_quote_price">
    # ... <span class="yfi-price-change-down">1.06</span>
    def is_price_change(value):
        return (value is not None and
            value.strip().lower()
                 .startswith('yfi-price-change'))
            
    result['change'] = (quote.
        find(attrs={'id': 'yfs_c10_'+tick}).
        find(attrs={'class': is_price_change}).string)
    
    return result


def mail_report(to, ticker_name):
    # Outer wrapper
    msg_outer = MIMEMultipart()
    msg_outer['Subject'] = "Stock report for " + ticker_name
    msg_outer['From'] = "you@example.com"
    msg_outer['To'] = to

    # Internal text container
    msg = MIMEMultipart('alternative')
    text = "Here is the stock report for " + ticker_name
    html = """\
    <html>
      <head></head>
      <body>
        <p>Here is the stock report for <b>""" + ticker_name + """</b>
        </p>
      </body>
    </html>
    """
    part1 = MIMEText(text, 'plain')
    part2 = MIMEText(html, 'html')
    # Attach parts into message container.
    msg.attach(part1)
    msg.attach(part2)
    msg_outer.attach(msg)

    filename = 'stocktracker-GOOG.csv'
    csv_text = ''.join(open(filename).readlines())
    csv_part = MIMEText(csv_text, 'csv')
    csv_part.add_header('Content-Disposition',
        'attachment', filename=filename)
    msg_outer.attach(csv_part)

    #send_message(msg_outer)
    queue_mail(msg_outer)
    
def send_message(message):
    s = smtplib.SMTP('mail.example.com')
    s.sendmail(message['From'], message['To'], message.as_string())
    s.close()

def queue_mail(message):
    if os.access('mail_queue', os.F_OK) != 1:           #1
        os.mkdir('mail_queue')                          #1
    handle, file_name = tempfile.mkstemp(               #2
        prefix='mail',                                  #2
        dir='mail_queue',                               #2
        text=True)                                      #2
    mail_file = open(file_name, 'w')                    #2
    mail_file.write(message['From'] + '\n')             #3
    mail_file.write(message['To'] + '\n')               #3
    mail_file.write(message.as_string() + '\n')         #3
    mail_file.close()
    
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
        print("Invalid ticker name: " + ticker_name)
        sys.exit()
        
    html = get_stock_html(ticker_name)
    print(find_quote_section(html))
    
    stock_values = parse_stock_html(html, ticker_name)
    stock_values['date'] = time.strftime("%Y-%m-%d %H:%M")
    
    write_row(ticker_name, stock_values)
    mail_report('you@example.com, youtoo@example.com', ticker_name)
    
    print(stock_values)
    
else:
    html = ''.join(sys.stdin.readlines())
    print(parse_stock_html(html, 'AAPL'))


