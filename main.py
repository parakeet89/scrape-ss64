# Part 1

import sys
from html.parser import HTMLParser
from urllib.request import Request, urlopen
from urllib.error import HTTPError
from http.client import InvalidURL
from re import findall

# Define the HTML parser class
class LinkParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.terms = {}

    def handle_starttag(self, tag, attributes):
        if tag == 'a':
            for attribute in attributes:
                if attribute[0] == 'href':
                    link = attribute[1].lower()
                    if link.endswith('.html') and not link.startswith(('http', '/')):
                        linksplit = link.split('.')
                        if len(linksplit) == 2:
                            term = linksplit[0]
                            self.terms[term] = ''

    def get_terms(self):
        return self.terms

# Ask the user for the OS path
OS = ''
while OS == '':
    try:
        OS = input('What is the operating system path? ')
        parenturl = 'https://ss64.com/' + OS
        request = Request(parenturl, headers={'User-Agent': 'Mozilla/5.0'})
        response = urlopen(request)
        pagecontents = response.read().decode().lower()
    except (HTTPError, InvalidURL):
        print('HTTPError/InvalidURL: Please check your input and try again.')
        sys.exit()

# Establish parser and feed html
parser = LinkParser()
parser.feed(pagecontents)

# Get terms
terms = parser.get_terms()

# Search HTML code for text matches and return a definition

class Page:
    def __init__(self):
        self.terms = {}
    def matches(self, pagecontents, searchstring, term):
        matches = findall(searchstring, pagecontents)
        result = matches[0] if matches else ''
        return result

page = Page()
for term in list(terms.keys()):
    searchstring = rf"<tr.*?>\s*<td.*?>.*?</td>\s*<td.*?><a href=\"{term}\.html\">{term}</a></td>\s*<td.*?>(.*?)</td>\s*</tr>"
    pageurl = parenturl + '/' + term + '.html'
    match = page.matches(pagecontents, searchstring, term)
    if match != '':
        terms[term] = [match, pageurl]
    else:           # remove terms that have an empty definition (these terms are probably not in the list of commands because there is no definition, such as 'syntax' and /syntax.html)
        del terms[term]

# Count terms
termCount = len(terms)
if termCount > 0:
    print('Operating system found. There are {} unique commands.'.format(termCount))
elif termCount == 0:
    print('Please check your input and try again. Please note that additional modifications to this program may be required in order to accommodate valid paths currently resulting in this error.')
    sys.exit()

# Part 2

# Ask the user if the user would like to update a definition

while True:
    userResponse = input('Would you like to update a definition (Y/N)? ').lower()
    if userResponse in ['y', 'yes']:
        term = input('Term: ').lower()
        if term not in terms.keys():
            print('Error: Term not found.')
        else:
            if terms[term] != '':
                print("{} is currently defined as '{}'".format(term, terms[term][0]))
                definition = input('Definition: ')
                terms[term] = [definition, pageurl]
            else:
                definition = input('Definition: ')
                terms[term] = [definition, pageurl]
    elif userResponse in ['n', 'no']:
        break
    else:
        print('Sorry, the system didn\'t recognize your response. Please try again.')

# Part 3

# asks the user what the new file should be saved as
filename = ''
while filename == '':
    filename = input('What would you like to save the file as? ')
    if filename == '':
        print('Please enter a valid filename.')

output = open(filename, 'w')

column1width = max(len(term) for term in terms.keys()) + 2
column2width = max(len(terms[term][0]) for term in terms.keys()) + 2
column3width = max(len(terms[term][1]) for term in terms.keys())

header = '{0:{x}}{1:{y}}{2:{z}}\n'.format('Term', 'Definition', 'See Also', x=column1width, y=column2width, z=column3width)
output.write(header)

for term in terms:
    row = '{0:{x}}{1:{y}}{2:{z}}\n'.format(term, terms[term][0], terms[term][1], x=column1width, y=column2width, z=column3width)
    output.write(row)
output.close()
print('File saved in your current working directory!')
