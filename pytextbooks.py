import re
import sys
import urllib.parse
import urllib.request
import webbrowser

import isbnlib
import libgenapi
import requests
from bs4 import BeautifulSoup

# import subprocess
# import os

# please set a libgen domain before usage!

libgendomain = ""
libgen = libgenapi.Libgenapi(libgendomain)


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


def getisbninfo(isbninput):
    # make sure its an isbn thats inputted
    if isibnvalid(isbninput):
        # meta actually queries the database and outputs a dictionary containing authors and other info
        try:
            foundbook = isbnlib.meta(isbninput)
            print("ISBN: " + isbninput)
            print("Title: " + foundbook['Title'] + "\n")
            # make new line not just for clean format but also cause we cant concatenate list + string
            print("Author(s): ")
            # separate each part of the dict. into separate lines
            print("\n".join(foundbook['Authors']))
            # open coverimage in browser so user can verify its the right book
            searchlibgen(isbninput)
        except:
            print("ISBN could not be found on google books for " + isbninput + ". Searching Libgen anyways...")
            searchlibgen(isbninput)
    else:
        print(isbninput + " was an invalid ISBN.")


def searchlibgen(isbn):
    # make sure we actually have a domain before running. might want to move this to the beginning of the code in main.
    if (libgen == ""):
        print("Error! Libgen is not defined. Please define libgen and then run this function again.")
        return
    # identifier is isbn
    print("Searching for book on libgen at " + libgendomain)
    try:
        # use search api to find book via isbn
        # we can also use the title and such but this is an isbn-based tool
        bookquery = libgen.search(isbn, "identifier")
        bookquery = bookquery[0]
        # print(bookquery)
    except:
        print("Sorry! That book wasn't found on libgen or another error occurred :(")
        return
    print("We found the book on LibGen! The book is " + bookquery['size'] + " in size.")
    # set this to initially "no", update if we actually find a mirror
    propermirror = "no"
    # loop thru everything in the 'mirrors' key that libgenapi generates, 'ping' each to see if they're up
    # and by ping i mean check the response via urllib. if it's 200 we can assume its good.
    for mirror in bookquery["mirrors"]:
        print("Checking " + mirror + "...")
        if (ping(mirror)):
            print("Successful!")
            propermirror = mirror
            break
        else:
            print("Unsuccessful, moving to next mirror")
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
        webbrowser.open(pdflink)
    else:
        # oops
        print("We were unable to find any working mirrors.. this is very rare; something else may be up. Sorry.")
        return


# run only if this script is called as main
if __name__ == '__main__':
    if int(len(sys.argv)) > 1:
        # remove duplicates
        sys.argv = list(dict.fromkeys(sys.argv))
        for i in sys.argv[1: ]:
            if isibnvalid(i):
                getisbninfo(i)
    else:
        print("An isbn was not specified, running directly via input")
        print("To avoid this, simply execute this script with the ISBN as an option")
        isbn = input("ISBN(s): ").strip().split()
        # once again, remove duplicates
        isbn = list(dict.fromkeys(isbn))
        for book in isbn:
            if isibnvalid(book):
                getisbninfo(book)
    print("Done")

# working ISBN for debug/test: 9780230584778
