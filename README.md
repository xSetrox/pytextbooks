# pyTextbooks
pyTextbooks is a Python 3.7 command-based program to search Library Genesis via ISBN and fetch direct download links.


## Setup
The only setup necessary: You *must* complete line 7 of the code to specify a Library Genesis domain. Otherwise this will not work.

`libgendomain = "libgendomain.com"`

I am leaving domains out to avoid DMCA takedowns; other than the link, no code in this program has any pirated material.
Add this link at your own risk. Good luck finding proxies.
Converting libgendomain to a list with multiple domains *should* work due to how LibGenAPI works- I have not tried.

## Usage
Either run pytextbooks.py directly i.e simply `python pytextbooks.py` or add an ISBN as an option such as `python pytextbooks.py 9780321202178`

The program will guide you through all the other steps. It does all the work, but will ask you if you'd like things such as seeing the cover page, if you want to actually download it, and if it can't verify something, your permission to search anyways.

## Book downloads
The program simply opens direct download links (to .pdf's and .epub's) in the user's default web browser, as a way of downloading the files easily. The program does not handle the download in any other way, and the speeds are entirely dependent on the mirror(s) the file(s) are from. 

## Requirements
Although the program has a requirements.txt that you can run `pip install -r requirements.txt` on, the requirements are:
```
isbnlib==3.9.8
requests==2.21.0
beautifulsoup4==4.8.0
libgenapi==1.2.1
```
You will also, of course, need to have installed any requirements that these requirements have (such as lxml). Quite the paradox.
