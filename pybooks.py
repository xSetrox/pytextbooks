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
    if (urllib.request.urlopen(address).getcode() == 200):
        return True
    else:
        return False


def cleanhtml(raw_html):
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_html)
    return cleantext


# runs isbnlib's isbn-check functions to see if input is actually a valid isbn

def isibnvalid(isbn):
    if isbnlib.is_isbn10(isbn) or isbnlib.is_isbn13(isbn):
        return True
    else:
        return False


def getisbninfo(isbninput):
    # make sure its an isbn thats inputted
    if isibnvalid(isbninput):
        # meta actually queries the database and outputs a dictionary containing authors and other info
        try:
            foundbook = isbnlib.meta(isbninput)
        except:
            tryanyways = input("ISBN could not be found. Search libgen anyways? Y/N: ").upper()
            if (tryanyways == "Y"):
                searchlibgen(isbninput)
                return
            else:
                return
        print("ISBN: " + isbninput)
        print("Title: " + foundbook['Title'] + "\n")
        # make new line not just for clean format but also cause we cant concatenate list + string
        print("Author(s): ")
        # separate each part of the dict. into separate lines
        print("\n".join(foundbook['Authors']))
        # open coverimage in browser so user can verify its the right book
        showcover = input("Show cover? Y/N: ").upper()
        if showcover == "Y":
            coverimage = isbnlib.cover(isbninput)
            # print(coverimage)
            webbrowser.open(coverimage["thumbnail"])
        searchlibgen(isbninput)
    else:
        lasttry = input("ISBN is invalid- search libgen anyways? Y/N: ").upper()
        if (lasttry == "Y"):
            searchlibgen(isbninput)


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
    dlquestion = input("Would you like to try and install it? Y/N: ").upper()
    if (dlquestion == "Y"):
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
        testisbn = sys.argv[1]
        if isibnvalid(testisbn):
            getisbninfo(testisbn)
    else:
        print("An isbn was not specified, running directly via input")
        print("To avoid this, simply execute this script with the ISBN as an option")
        isbn = input("ISBN: ").strip()
        getisbninfo(isbn)
# working ISBN for debug/test: 0793587018
