import sys
import random
import requests
from urlparse import urljoin

from bs4 import BeautifulSoup

domain_list = """\
example.com
example.com.au
"""

domains = domain_list.split("\n")

if '-d' in sys.argv:
    for domain in domains:
        print "1.2.3.4\t" + domain
        print "1.2.3.4\twww." + domain
    sys.exit()

bad_page_terms = ['Error', 'Unhandled exception', 'Exception', '5433', 'Welcome to nginx!', ]

def is_valid(link):
    href = link.get('href')
    if (href is None or
        href.startswith('#') or
        href.startswith('http') or
        href.startswith('mailto')):
        return False
    return True
    
    
for domain in domains:
    url = "http://" + domain
    print "Checking", url
    r = requests.get(url)
    if r.status_code != 200:
        print domain, "FAIL: status code is", r.status_code
    for bad_term in bad_page_terms:
        if bad_term in r.text:
            print domain, "FAIL: term", bad_term, "found in page", r.url
    
    soup = BeautifulSoup(r.text, 'html.parser')
    
    #print dir(soup)
    links = soup.find_all('a')
    if links is not None:
        # there are links on the page, check one
        links = [l for l in links if is_valid(l) 
                 and l.href != '/' and l.href != '/index.html')]
        
        print "   ", len(links), "links found"
        if links != []:
            second_page = urljoin(r.url, random.choice(links).get('href'))
            print "    Checking", second_page
            r2 = requests.get(urljoin(r.url, random.choice(links).get('href')))
            if r2.status_code != 200:
                print domain, "FAIL: status code is", r2.status_code
            for bad_term in bad_page_terms:
                if bad_term in r2.text:
                    print domain, "FAIL: term", bad_term, "found in page", r2.url
            
            # also make sure that it's not the same as the root page
            if r2.text == r.text:
                print domain, "FAIL: page and subpages have the same content! (misconfigured nginx?)"
                
    print "PASS:", domain
    print