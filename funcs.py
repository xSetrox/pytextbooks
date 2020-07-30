import re
import urllib.parse
import urllib.request
import isbnlib
import requests
from bs4 import BeautifulSoup
import validators
import configparser

# please set a libgen domain before usage!
config = configparser.ConfigParser()
config.read('config.ini')
libgendomain = config['pybooks']['domain']


# "ping" function which is actually just checking for a response code of 200
def ping(address):
    return urllib.request.urlopen(address).getcode() == 200


def cleanhtml(raw_html):
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_html)
    return cleantext


# runs isbnlib's isbn-check functions to see if input is actually a valid isbn

def isibnvalid(isbn):
    return isbnlib.is_isbn10(isbn) or isbnlib.is_isbn13(isbn)

def searchlibgen(isbn):
    # make sure we actually have a domain before running. might want to move this to the beginning of the code in main.
    if (libgendomain == ""):
        return "libgenthrow"
    # identifier is isbn
    try:
        # use search api to find book via isbn
        # we can also use the title and such but this is an isbn-based tool
        page = requests.get("{0}/search.php?req={1}&open=0&res=25&view=simple&phrase=1&column=identifier".format(libgendomain,isbn)).content
        soup = BeautifulSoup(page, features='lxml')
        results = soup.find('tr',{'bgcolor':'#C6DEFF'})
        if results:
            results = results.findAll('a',href=True)
            if not results:
                return ['error','']
        else:
            return ['error','']
        bookquery = []
        for link in results:
            if validators.url(link['href']):
                bookquery.append(link['href'])
        del bookquery[-1]
    except Exception as e:
        return ['exception', str(e)]
    # set this to initially "no", update if we actually find a mirror
    propermirror = "no"
    # loop thru everything in the 'mirrors' key that libgenapi generates, 'ping' each to see if they're up
    # and by ping i mean check the response via urllib. if it's 200 we can assume its good.
    for mirror in bookquery:
        if (ping(mirror)):
            propermirror = mirror
            break
    # use beautifulsoup and lxml to parse the page. the first href link on the page is the "GET"
    # ie the link we need to click to download the pdf directly
    if (propermirror != "no"):
        page = requests.get(mirror)
        data = page.content
        soup = BeautifulSoup(data, "lxml")
        pdflink = soup.find('a').get('href')
        # pdflink = soup.get_text()
        # the GET link is actually relative, use urllib to combine it with the domain its relative to
        # ie the mirror domain
        pdflink = urllib.parse.urljoin(mirror, pdflink)
        # originally this was going to download the file without the need for a web browser.
        # i figured it'd be better to just use the user's web browser download thing, for multiple reasons
        # newfile = urllib.request.urlretrieve(mirror)
        # Popen_arg = r'explorer /select, "' + f + '"'
        # subprocess.Popen(Popen_arg)
        # and finally open the full link in web browser
        return pdflink
    else:
        # oops
        return ['error','']

# working ISBN for debug/test: 9780230584778
