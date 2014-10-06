from collections import namedtuple

Website = namedtuple("Website", "name, domain, username, length, chars")
try:
    from Tkinter import *
except ImportError:
    from tkinter import *
from PIL import Image, ImageTk
from hashlib import md5
import random, csv
import tkSimpleDialog, tkMessageBox
import xerox as pyperclip
import os
from mapcanvas import * 

def resource_path(relative):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative)
    return os.path.join(relative)
    
class pw_gen(Tk):
    def __init__(self,parent,sites):
        Tk.__init__(self,parent)
        self.parent = parent
        self.sites = sites
        self.timer = None
        self.initialize()
        
    def draw_map(self):
        m = md5()
        m.update(self.name.get())
        m.update(self.domain.get())
        m.update(self.username.get())
        m.update(self.password.get())
        random.seed(int(m.hexdigest(),16))
        lands = []
        monsters = []
        try:
            landfiles = filter(lambda x: x.lower().endswith('gif') or x.lower().endswith('png'),os.listdir(os.path.join('emoji','land')))
            monsterfiles = filter(lambda x: x.lower().endswith('gif') or x.lower().endswith('png'),os.listdir(os.path.join('emoji','monsters')))
        except OSError:
            tkMessageBox.showerror(
                "No Emoji!",
                "No emoji available! Ensure there are images in the folders emoji/land and emoji/monsters."
            )
            return
        for i in range(6):
            filename = random.choice(landfiles)
            try:
                lands.append(Image.open(resource_path(os.path.join('emoji','land',filename))))
            except IOError:
                tkMessageBox.showerror(
                    "File Won't Open!",
                    "Critical failure while opening "+resource_path(os.path.join('emoji','land',filename))+". Please make sure this file is an image of the appropriate type or delete it."
                )
                return
            filename = random.choice(monsterfiles)
            try:
                im = Image.open(resource_path(os.path.join('emoji','monsters',filename)))
            except IOError:
                tkMessageBox.showerror(
                    "File Won't Open!",
                    "Critical failure while opening "+resource_path(os.path.join('emoji','monsters',filename))+". Please make sure this file is an image of the appropriate type or delete it."
                )
                return
            #the image needs to remember its filename for hashing purposes
            im.info['filename']=filename
            monsters.append(im)
        self.inventory.draw_inv(monsters)
        self.map.draw_map(lands,random)
        self.savepw.config(state=NORMAL)
    
    def reset_map(self,password,oldpaste):
        self.map.reset()
        self.inventory.reset()
        #just in case?
        self.password.delete(0,END)
        if pyperclip.paste()==password:
            pyperclip.copy(oldpaste)
    
    def wipe_map(self):
        self.map.wipe()
        self.inventory.wipe()
        if self.timer is not None:
            self.after_cancel(self.timer)
        #just in case?
        self.password.delete(0,END)
        self.timer = None
        if pyperclip.paste()==password:
            pyperclip.copy(oldpaste)
        
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
                self.wipe_map()
            return
        site = self.sites[self.name.get()]
        self.domain.set(site.domain)
        self.username.set(site.username)
        self.pw_length.set(site.length)
        self.chars.set(site.chars)
        self.prevname = self.name.get()
        self.password.delete(0, END)
        self.savepw.config(state=DISABLED)
        self.wipe_map()
        
    def save(self):
        with open("sites.csv", "wb") as sitefile:
            writer = csv.writer(sitefile)
            writer.writerows(self.sites.values())
            
    def update_record(self,*args):
        site = self.sites[self.name.get()]
        self.sites[self.name.get()] = site._replace(domain = self.domain.get(),username=self.username.get(),length=self.pw_length.get(),chars=self.chars.get())
        self.savepw.config(state=DISABLED)
        self.wipe_map()
        
    def gen_pw(self):
        selector = "1234567890qwertyuuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM"+self.chars.get()
        password=""
        m = md5()
        m.update(self.name.get())
        m.update(self.domain.get())
        m.update(self.username.get())
        m.update(self.password.get())
        try:
            m.update(self.map.extract_grid())
        except IllegalStateError:
            tkMessageBox.showerror("No Password Generated","The password cannot be generated until the map has been displayed. (Getting this error may indicate a software bug.)")
            self.savepw.config(state=DISABLED)
        random.seed(int(m.hexdigest(),16))
        for i in range(int(self.pw_length.get())):
            password=password+random.choice(selector)
        oldpaste = pyperclip.paste()
        pyperclip.copy(password);print password==pyperclip.paste()
        if self.timer is not None:
            self.after_cancel(self.timer)
        self.timer = self.after(60000,self.reset_map,password,oldpaste)
        
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
        c=c+1
        
        #Canvas to draw the inventory
        self.inventory = Inventory(self,relief=RAISED,bd=2,height=62)
        self.inventory.grid(column=0, row=c, columnspan=2, sticky='EW')
        c=c+1
        
        #Canvas to draw the map
        self.mapx = 11
        self.mapy = 8
        self.gridscale = 40
        self.map = CanvasDnd(self, self.mapx, self.mapy, True,
                    width=self.gridscale*self.mapx, height=self.gridscale*self.mapy)
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
