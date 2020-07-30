import argparse
from gui import guiloop
import funcs as f
import webbrowser

parser = argparse.ArgumentParser(description='ISBN input')
parser.add_argument('isbns', type=str, nargs='*',
                    help='Opens pyBooks GUI')
parser.add_argument('-gui', help='Opens up the GUI', action='store_true')

args = parser.parse_args()
if args.gui:
    guiloop()
else:
    if len(args.isbns) == 0:
        print('You must either run -gui or input some ISBNs')
    else:
        isbns = args.isbns
        invalids = ''
        valids = []
        total = 0
        for isbn in isbns:
            if not f.isibnvalid(isbn):
                invalids += isbn + "\n"
            else:
                valids.append(isbn)
                pass
            total += 1
        if len(invalids) > 0:
            print("The following ISBNs were invalid and will be skipped:\n\n" + invalids)
        if len(valids) > 0:
            print("The tool is now searching for PDFs...")
            links = []
            linkstr = ""
            errors = ""
            for isbn in valids:
                code = f.searchlibgen(isbn)
                if code[0] == "error":
                    errors += isbn + "\n"
                elif code[0] == "exception":
                    print('An exception was encountered:', code[1])
                else:
                    links.append(code)
                    linkstr += code + "\n"
            if len(errors) > 0:
                print("Downloads could not be found for the following ISBN's:\n\n" + errors)
            if len(links) > 0:
                ans = input("{0}/{1} download(s) were found!\nWould you like to download now? If you input no, the links will be written into links.txt instead of opened (Y/N):".format(len(links), total))
                ans = ans.lower()
                if ans == 'y':
                    for link in links:
                        webbrowser.open(link)
                else:
                    with open('links.txt', 'w+') as f:
                        for link in links:
                            f.write(link + '\n')
    print('Thank you for using pyBooks, I hope you enjoyed! :)')