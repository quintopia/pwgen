from collections import namedtuple

Website = namedtuple("Website", "name, domain, username, length, chars")
try:
    from Tkinter import *
except ImportError:
    from tkinter import *
from PIL import Image, ImageTk
from hashlib import md5
import random, csv
import tkSimpleDialog
import pyperclip
import Tkdnd
    
class pw_gen(Tk):
    def __init__(self,parent,sites):
        Tk.__init__(self,parent)
        self.parent = parent
        self.sites = sites
        self.initialize()
        
    def draw_map(self):
        m = md5()
        m.update(self.name.get())
        m.update(self.domain.get())
        m.update(self.username.get())
        m.update(self.password.get())
        random.seed(m.digest())
        print random.randrange(1000)
        print random.randrange(1000)
        print random.randrange(1000)
        
        self.savepw.config(state=NORMAL)
    
    def update_fields(self,*args):
        if self.name.get() == self.prevname:
            return #do nothing if the selection did not change
        if self.name.get() == "New Site...":
            sitename = tkSimpleDialog.askstring("Create New Site", "Enter name of site:" ,parent=self)
            if sitename is None:
                self.name.set(self.prevname)
            else:
                self.optionList['menu'].insert_command(len(sites),label=sitename,command=lambda name=sitename: self.name.set(name))
                sites[sitename]=Website(name=sitename,domain='',username='',length='10',chars='-_.`~#%^&(){}\'!@*=+[]{}\\|;:",<>/?')
                self.prevname = sitename
                self.name.set(sitename)
                self.domain.set('')
                self.username.set('')
                self.pw_length.set('10')
                self.chars.set('-_.`~#%^&(){}\'!@*=+[]{}\\|;:",<>/?')
                self.optionList.update()
                self.savepw.config(state=DISABLED)
            return
        site = self.sites[self.name.get()]
        self.domain.set(site.domain)
        self.username.set(site.username)
        self.pw_length.set(site.length)
        self.chars.set(site.chars)
        self.prevname = self.name.get()
        self.password.delete(0, END)
        self.savepw.config(state=DISABLED)
        
    def save(self):
        with open("sites.csv", "wb") as sitefile:
            writer = csv.writer(sitefile)
            writer.writerows(self.sites.values())
            
    def update_record(self,*args):
        site = self.sites[self.name.get()]
        self.sites[self.name.get()] = site._replace(domain = self.domain.get(),username=self.username.get(),length=self.pw_length.get(),chars=self.chars.get())
        self.savepw.config(state=DISABLED)
        
    def gen_pw(self):
        selector = "1234567890qwertyuuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM"+self.chars.get()
        password=""
        #todo:initialize rand seed from map data
        for i in range(int(self.pw_length.get())):
            password=password+random.choice(selector)
        pyperclip.copy(password)
        self.password.delete(0, END)
        
    def initialize(self):
        label=Label(self,anchor="w",text="Website Name:")
        c=0
        #Option to select website
        label.grid(column=0,row=c,sticky='EW',padx=20, pady=10)
        self.name = StringVar(self)
        self.name.trace("w", lambda *args: self.after_idle(self.update_fields, *args))
        self.prevname = ""
        sitelist = self.sites.keys()
        sitelist.append("New Site...")
        self.optionList = OptionMenu(self, self.name, *(sitelist))
        self.optionList.grid(column=1,row=c,sticky='EW',padx=20, pady=10)
        c=c+1
        
        #Textbox for the domain name
        label=Label(self,anchor="w",text="Root Domain Name:")
        label.grid(column=0, row=c,sticky='EW',padx=20, pady=10)
        self.domain = StringVar(self)
        self.domain.trace("w", self.update_record)
        self.domainentry = Entry(self, textvariable=self.domain)
        self.domainentry.grid(column=1,row=c,sticky='EW',padx=20, pady=10)
        c=c+1
        
        #Textbox for username
        label=Label(self,anchor="w",text="User Name:")
        label.grid(column=0, row=c,sticky='EW',padx=20, pady=10)
        self.username = StringVar(self)
        self.username.trace("w", self.update_record)
        self.usernameentry = Entry(self,textvariable=self.username)
        self.usernameentry.grid(column=1,row=c,sticky='EW',padx=20, pady=10)
        c=c+1
        
        #Textbox for password
        label=Label(self,anchor="w",text="Global Password:")
        label.grid(column=0, row=c,sticky='EW',padx=20, pady=10)
        self.password = Entry(self,show='*')
        self.password.grid(column=1, row=c,sticky='EW',padx=20, pady=10)
        c=c+1
        
        #Option for selecting password length
        label=Label(self,anchor="w",text="Password Length:")
        label.grid(column=0, row=c,sticky='EW',padx=20, pady=10)
        self.pw_length = StringVar(self)
        self.pw_length.trace("w", self.update_record)
        self.lengthList = OptionMenu(self, self.pw_length, *['8','9','10','11','12','13','14','15','16'])
        self.lengthList.grid(column=1, row=c, sticky='EW', padx=20, pady=10)
        c=c+1
        
        #Textbox for allowable special characters
        self.chars = StringVar(self)
        self.chars.trace("w",self.update_record)
        label=Label(self,anchor="w",text="Allowed Special Characters:")
        label.grid(column=0, row=c,sticky='EW',padx=20,pady=10)
        self.charsentry = Entry(self, textvariable=self.chars,width=32)
        self.charsentry.grid(column=1,row=c,sticky='EW',padx=20,pady=10)
        c=c+1
        
        #Buttons for drawing the map and copying the result to the clipboard
        self.getmap = Button(self, text="Draw Map", command=self.draw_map)
        self.getmap.grid(column=0,row=c)
        self.savepw = Button(self, text="Copy Password to Clipboard", command=self.gen_pw, state=DISABLED)
        self.savepw.grid(column=1,row=c)
        c=c+1
        
        #Buttons for saving the current sites and quitting
        self.savebutton = Button(self, text="Save", command=self.save)
        self.savebutton.grid(column=0,row=c)
        self.exitbutton = Button(self, text="Quit", command=self.destroy)
        self.exitbutton.grid(column=1,row=c)
        
        #Canvas to draw the map
        c=c+1
        self.map = Canvas(self, height=300)
        self.map.grid(column=0, row=c, columnspan=2, sticky='EW')
        self.name.set(sitelist[0]) #pick the option LAST so that the call to update_fields works
        
        
if __name__ == "__main__":
    sites = {}
    try:
        for site in map(Website._make, csv.reader(open("sites.csv", "rb"))):
            sites[site.name] = site
    except IOError:
        pass #we already have an empty dictionary, which should be what we want in this case
    app = pw_gen(None,sites)
    app.title('Deterministic Password Generator')
    app.mainloop()
    
'''
try:
            self.image = Image.open("emoji/monsters/1.gif")
        except IOError:
            tkMessageBox.showerror(
                "Open file",
                "No emoji available! Ensure there are images in the folders emoji/land and emoji/monsters"
            )
            return
'''