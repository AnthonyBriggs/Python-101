
"""
Copyright (C) 2016 Anthony Briggs <anthony.briggs@gmail.com>,
except for the URL matching regexp which is (C) John Gruber / Daring
Fireball, but seems to be intended to be released publicly

This file is part of Chat-thing.

    Chat-thing is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as 
    published by the Free Software Foundation, either version 3 of 
    the License, or (at your option) any later version.

    Chat-thing is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.

    You should have received a copy of the GNU Affero General Public 
    License along with Chat-thing.  If not, see 
    <http://www.gnu.org/licenses/agpl.txt>.
"""

import cgi
import re

# https://mathiasbynens.be/demo/url-regex might be useful if this doesn't work...

# URL matching regexp pulled from Markdown: http://daringfireball.net/2010/07/improved_regex_for_matching_urls 
#
# So nasty...

url_regexp = r"""(							# Capture 1: entire matched URL
  (?:
    [a-z][\w-]+:				# URL protocol and colon
    (?:
      /{1,3}						# 1-3 slashes
      |								#   or
      [a-z0-9%]						# Single letter or digit or '%'
      								# (Trying not to match e.g. "URI::Escape")
    )
    |							#   or
    www\d{0,3}[.]				# "www.", "www1.", "www2." ... "www999."
    |							#   or
    [a-z0-9.\-]+[.][a-z]{2,4}/	# looks like domain name followed by a slash
    |
    \d{1,3}.{4}/                     # dotted quads
  )
  (?:							# One or more:
    [^\s()<>]+						# Run of non-space, non-()<>
    |								#   or
    \(([^\s()<>]+|(\([^\s()<>]+\)))*\)	# balanced parens, up to 2 levels
  )+
  (?:							# End with:
    \(([^\s()<>]+|(\([^\s()<>]+\)))*\)	# balanced parens, up to 2 levels
    |									#   or
    [^\s`!()\[\]{};:'".,<>?]		# not a space or one of these punct char
  )
)
"""


find_url = re.compile(url_regexp, re.VERBOSE)

if __name__ == '__main__':
    print((dir(find_url)))
    print((find_url.search("www.cool.com.au")))
    print((find_url.search("https://pbs.twimg.com/media/CitlLnyWYAEsWJt.jpg")))
    print((dir(find_url.search("https://pbs.twimg.com/media/CitlLnyWYAEsWJt.jpg"))))
    print((find_url.search("https://pbs.twimg.com/media/CitlLnyWYAEsWJt.jpg").groups()))
    print((find_url.search("http://pbs.twimg.com/").groups()))
    print(("DOUBLE:", find_url.search("www.cool.com.au and pbs.twimg.com").groups()))
    print((dir(find_url.search("www.cool.com.au and pbs.twimg.com"))))

    print((find_url.search("The url is pbs.twimg.com/media/CitlLnyWYAEsWJt.jpg, an image on twitter").groups()))

    print((find_url.search("http://192.168.0.1/").groups()))
    #print(find_url.search("192.168.0.1").groups())
    print((find_url.search("http://192.168.1/").groups()))
    
    
def is_image(the_url):
    image_tags = ['.gif', '.jpg', '.png', '.jpeg']
    for tag in image_tags:
        if the_url.endswith(tag):
            return True

def repunctuate(link, part):
    if part.endswith("..."):
        return link + "..."
    if part[-1] in "!;:.,?":
        return link + part[-1]
    return link
    
def make_urls(the_line):
    output = []
    for part in the_line.split():
        match = find_url.search(part)
        if match:
            the_url = match.groups()[0]
            if not "://" in the_url[:8]:
                the_url = "http://" + the_url
            if is_image(the_url):
                link = '<img src="%s">' % the_url
            else:
                link = '<a href="%s">%s</a>' % (the_url, the_url)
            link = repunctuate(link, part)
            output.append(link)
        else:
            output.append(cgi.escape(part))
    return ' '.join(output)
    
if __name__ == '__main__':
    print((make_urls("The url is pbs.twimg.com/media/CitlLnyWYAEsWJt.jpg, an image on twitter")))
    print((make_urls("The url is pbs.twimg.com/media/CitlLnyWYAEsWJt/FNord... a link on twitter")))
    print((make_urls("https://pbs.twimg.com/media/CitlLnyWYAEsWJt.jpg! an image on twitter")))
    print((make_urls("""<script type="text/javascript">alert("ha ha butts!");</script>""")))
    
