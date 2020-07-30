# pyTextbooks
pyTextbooks is a Python 3.7 command-based program to search Library Genesis via ISBN and fetch direct download links.

## Setup
The only setup necessary: You *must* go into config.ini and specify a Library Genesis domain on the `domain =` line. Otherwise this will not work.

`libgendomain = "http://libgendomain.com"`
This will only work if http:// is in front of the domain!

I am leaving domains out to avoid DMCA takedowns; other than the link, no code in this program has any pirated material (unfortunate news for you, textbook companies! ).
Add this link at your own risk. Good luck finding proxies.

## Usage
You actually have a lot more options than ever before!

### Command line:
`python pybooks.py -isbns separated by spaces here-`
Example:
`python pybooks.py 9780471202424`

### GUI:
Simply run:
`python pybooks.py -gui`

The program will guide you through all the other steps. It does all the work for you, so you can save money!

## Book downloads
If you run via commandline, the program will give you an option to either list to a .txt file or download now.
If you choose to download now, the program will open a new web tab for *every* book download there is and it will be handled by your browser download system.
These downloads are from Libgen and speed is not dependent of the program, nor is it my fault.
If you choose to list to a .txt, be wary that *every time* you choose to list to a txt, it will overwrite the last one.


## Requirements
Although the program has a requirements.txt that you can run `pip install -r requirements.txt` on, the requirements are:
```
beautifulsoup4==4.8.0
bs4==0.0.1
certifi==2019.9.11
chardet==3.0.4
decorator==4.4.2
defusedxml==0.6.0
grab==0.6.41
idna==2.8
isbnlib==3.9.8
libgenapi==1.2.1
lxml==4.4.1
Pillow==6.1.0
ping3==2.3.1
pycurl==7.43.0.3
pytils==0.3
requests==2.22.0
selection==0.0.14
six==1.12.0
soupsieve==1.9.3
urllib3==1.25.3
urllib5==5.0.0
user-agent==0.1.9
validators==0.16.0
weblib==0.1.30
```
You will also, of course, need to have installed any requirements that these requirements have.
