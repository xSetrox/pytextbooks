# run this file first if you would like to use the beta GUI
from tkinter import *
from tkinter import messagebox
import funcs as f
import webbrowser

def submitButton():
    isbns = str(isbnbox.get())
    isbns = isbns.split(" ")
    invalids = ""
    valids = []
    total = 0
    for isbn in isbns:
        if not f.isibnvalid(isbn):
            invalids += isbn + "\n"
            #print("ISBN {0} was invalid, skipping".format(isbn))
        else:
            total += 1
            valids.append(isbn)
            pass
    if len(invalids) > 0:
        messagebox.showwarning("ISBN(s) invalid", "The following ISBNs were invalid and will be skipped:\n\n" + invalids)
    if len(valids) > 0:
        messagebox.showinfo("Searching","The tool will now attempt to find textbook downloads.")
        links = []
        linkstr = ""
        errors = ""
        for isbn in valids:
            code = f.searchlibgen(isbn)
            if code[0] == "error":
                errors += isbn + "\n"
            elif code[0] == "exception":
                messagebox.showwarning("Exception", "A very bad thing happened. Here is what the thing says: \n\n\"{0}\"\n\n"
                                                    "If you have tried multiple times and still get this issue, you "
                                                    "should probably ask Lance for help. Show him this.".format(code[1]))
            else:
                links.append(code)
                linkstr += code + "\n"
        if len(errors) > 0:
            messagebox.showwarning("Not found", "Downloads could not be found for the following ISBN's:\n\n" + errors)
        if len(links) > 0:
            messagebox.showinfo("Found", "{0}/{1} download(s) were found!\n\nWhen you click OK, the tool will open some "
                                         "(perhaps several) tabs in your web browser that will initiate PDF downloads. "
                                         "Do not panic- this is normal!\n\n"
                                         "**You will need to click save file on each of the popups.**\n\nAlso, these downloads"
                                         " sometimes take forever, I have no control over that.\n\nReady?".format(len(links),total))
            if total != len(links):
                notfound = total - len(links)
                messagebox.showinfo("Lance","Also, you are still missing {0} books. If you contact me, I can help you "
                                            "find them, if a PDF of them exists.".format(notfound))
            for link in links:
                pass
                webbrowser.open(link)
def guiloop():
    isbninput = ""
    password = ""
    global window
    window = Tk()
    window.title("pyBooks GUI")
    window.geometry('350x240')
    l1 = Label(window, text="pyBooks",justify="center",font=("Arial Bold", 15))
    l2 = Label(window, text="The GUI edition of pyTextbooks!",font=("Arial",10))
    l3 = Label(window, text="github.com/xSetrox/pytextbooks",font=("Arial",8))
    l1.pack()
    l2.pack()
    l3.pack()
    spacer = LabelFrame(window,height=10)
    spacer.pack()
    l4 = Label(window,text="Input ISBN(s) (separate with spaces): ",justify="left")
    l4.pack()
    scroll = Scrollbar(window,orient="horizontal")
    global isbnbox
    isbnbox = Entry(window, xscrollcommand=scroll.set,width=1000,bd=2,textvariable=isbninput)
    isbnbox.pack()
    scroll.config(command=isbnbox.xview)
    scroll.pack(fill=X)
    searchb = Button(window, text="Search", bg="#33ff99", activebackground="#66ffb3", command=submitButton)
    searchb.pack()
    global donate
    donate = Button(window, text="Donate", bg="#00bfff", activebackground="#7bdcfc", command=lambda: webbrowser.open("https://www.paypal.me/lancefaltinsky"))
    donate.pack(side=LEFT)

    window.mainloop()


