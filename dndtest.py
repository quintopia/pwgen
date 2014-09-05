

"""
This code demonstrates a real-world drag and drop.
"""

from Tkinter import *
import Tkdnd
from PIL import Image,ImageTk

def mouse_in_widget(Widget,event):
    """
    Figure out where the cursor is with respect to a widget.
    
    Both "Widget" and the widget which precipitated "event" must be
        in the same root window for this routine to work.
    """
    x = event.x_root - Widget.winfo_rootx()
    y = event.y_root - Widget.winfo_rooty()
    return (x,y)

def mouse_in_item(canvas,ID,event):
    x1,y1 = canvas.coords(ID)
    x1 = x1 + canvas.winfo_rootx()
    y1 = y1 + canvas.winfo_rooty()
    x = event.x_root - x1
    y = event.y_root - y1
    return (x,y)
    
class Dragged:
    """
    This is a prototype thing to be dragged and dropped.
    
    Derive from (or mixin) this class to creat real draggable objects.
    """
    
    def __init__(self,image):
        #When created we are not on any canvas
        self.canvas = None
        self.original_canvas = None
        #This sets where the mouse cursor will be with respect to our label
        self.offset_x = 0
        self.offset_y = 0
        self.image = image
        self.imagetk = ImageTk.PhotoImage(self.image)
        
    def dnd_end(self,Target,event):
        #this gets called when we are dropped
        if self.canvas==None and self.original_canvas==None:
            #We were created and then dropped in the middle of nowhere, or
            #    we have been told to self destruct. In either case
            #    nothing needs to be done and we will evaporate shortly.
            return
        if self.canvas==None and self.original_canvas<>None:
            self.canvas = self.original_canvas
            self.id = self.original_id
            self.canvas.itemconfig(self.id,state=NORMAL)
            self.canvas.dnd_enter(self,event)
            return
        self.canvas.tag_bind(self.id,'<ButtonPress>',self.press)
        if self.original_canvas:
            self.original_canvas.delete(self.original_id)
            self.original_canvas = None
            self.original_id = None
            
    def winfo_height(self):
        x,y=self.image.size
        return y
        
    def winfo_width(self):
        x,y=self.image.size
        return x


    def appear(self, canvas, xy=None, bounds=None):
        """
        Put an label representing this Dragged instance on canvas.
        
        xy says where the mouse pointer is. We don't, however, necessarily want
            to draw our upper left corner at xy. Why not? Because if the user
            pressed over an existing label AND the mouse wasn't exactly over the
            upper left of the label (which is pretty likely) then we would like
            to keep the mouse pointer at the same relative position inside the
            label. We therefore adjust X and Y by self.offset_x and self.OffseY
            thus moving our upper left corner up and/or left by the specified
            amounts. These offsets are set to a nominal value when an instance
            of Dragged is created (where it matters rather less), and to a useful
            value by our "press" routine when the user clicks on an existing
            instance of us.
        """
        if self.canvas:
            #we are already on a canvas; do nothing
            return
        if xy is not None:
            self.x, self.y = xy
        if not hasattr(self, 'x'):
            self.x=0
        if not hasattr(self, 'y'):
            self.y=0
        if bounds is None:
            minx,miny,maxx,maxy = 0,0,canvas.winfo_width(),canvas.winfo_height()
        else:
            minx,miny,maxx,maxy = bounds
        self.x = min(max(self.x-self.offset_x,minx),maxx-self.winfo_width())+self.offset_x
        self.y = min(max(self.y-self.offset_y,miny),maxy-self.winfo_height())+self.offset_y

        #Display the label on a window on the canvas. We need the ID returned by
        #    the canvas so we can move the label around as the mouse moves.
        self.id = canvas.create_image((self.x-self.offset_x, self.y-self.offset_y), image=self.imagetk, anchor="nw")
        #Note the canvas on which we drew the label.
        self.canvas = canvas

    def vanish(self,all=0):
        """
        If there is a label representing us on a canvas, make it go away.
        
        if self.canvas is not None, that implies that "Appear" had prevously
            put a label representing us on the canvas and we delete it.
            
        if "all" is true then we check self.original_canvas and if it not None
            we delete from it the label which represents us.
        """
        if self.canvas:
            #we have a label on a canvas; delete it
            self.canvas.delete(self.id)
            #flag that we are not represented on the canvas
            self.canvas = None
            #Since ID and Label are no longer meaningful, get rid of them lest they
            #confuse the situation later on. Not necessary, but tidy.
            self.id = None
        
        if all and self.original_canvas:
            #Delete label representing us from self.original_canvas
            self.original_canvas.delete(self.original_id)
            self.original_canvas = None
            del self.original_id

    def move(self,xy,bounds):
        """
        If we have a label a canvas, then move it to the specified location. 
        
        xy is with respect to the upper left corner of the canvas
        """    
        assert self.canvas, "Can't move because we are not on a canvas"
        self.x, self.y = xy
        minx,miny,maxx,maxy = bounds
        #print self.offset_x,self.offset_y
        self.x = min(max(self.x-self.offset_x,minx),maxx-self.winfo_width())+self.offset_x
        self.y = min(max(self.y-self.offset_y,miny),maxy-self.winfo_height())+self.offset_y
        #print self.x-self.offset_x,self.y-self.offset_y
        self.canvas.coords(self.id,self.x-self.offset_x,self.y-self.offset_y)
        
    def set_pos(self,xy):
        """
        Move to exactly the position specified, don't worry about offsets
        """
        self.x, self.y = xy
        if self.canvas is not None:
            self.canvas.coords(self.id,self.x,self.y)

    def press(self,event):
        """
        User has clicked on a label representing us. Initiate drag and drop.
        """
        #Save our current label as the Original label
        self.original_id = self.id
        self.original_canvas = self.canvas
        self.canvas.itemconfig(self.id,state=HIDDEN)
        #Say we have no current label    
        self.id = None
        self.canvas = None
        #Ask Tkdnd to start the drag operation
        if Tkdnd.dnd_start(self,event):
            #Save where the mouse pointer was in the label so it stays in the
            #    same relative position as we drag it around
            self.offset_x, self.offset_y = mouse_in_item(self.original_canvas,self.original_id,event)
            #print self.offset_x, self.offset_y
            #Draw a label of ourself for the user to drag around
            xy = mouse_in_widget(self.original_canvas,event)
            width = self.original_canvas.winfo_width()
            height = self.original_canvas.winfo_height()
            bounds = (0,0,width,height)
            self.appear(self.original_canvas,xy,bounds)
    
class CanvasDnd(Canvas):
    """
    A canvas to which we have added those methods necessary so it can
        act as both a TargetWidget and a TargetObject. 
        
    Use (or derive from) this drag-and-drop enabled canvas to create anything
        that needs to be able to receive a dragged object.    
    """    
    def __init__(self, master, *args, **kw):
        if kw.has_key('gridsize'):
            self.gridsize=kw['gridsize']
        else:
            self.gridsize=40
        cnf = {}
        if len(args)>0:
            cnf = args[-1]
            if type(cnf) in (DictionaryType, TupleType):
                print cnf
                args = args[:-1]
            else:
                cnf = {}
        if len(args)<3:
            self.drawgrid = False
        else:
            self.drawgrid = args[2]
        if len(args)<2:
            gridy = 1
        else:
            gridy = args[1]
        if len(args)<1:
            gridx = 3
        else:
            gridx = args[0]
        if self.drawgrid:
            self.grid = [[None]*5 for i in range(5)]
            kw['width']=gridx*self.gridsize
            kw['height']=gridy*self.gridsize
        Canvas.__init__(self, master, kw)
        #draw gridlines
        if self.drawgrid:
            for i in range(1,gridx):
                self.create_line(self.gridsize*i,0,self.gridsize*i,gridy*self.gridsize,fill='gray')
            for i in range(1,gridy):
                self.create_line(0,self.gridsize*i,gridx*self.gridsize,self.gridsize*i,fill='gray')

    #----- TargetWidget functionality -----
    
    def dnd_accept(self,source,event):
        return self

    #----- TargetObject functionality -----

    def dnd_enter(self,source,event):
        #This is called when the mouse pointer goes from outside the
        #   Target Widget to inside the Target Widget.
        #Figure out where the mouse is with respect to this widget
        xy = mouse_in_widget(self,event)
        x,y = xy

        width = self.winfo_width()
        height = self.winfo_height()
        bounds = (0,0,width,height)
        xy = (x,y)
        source.appear(self,xy,bounds)
        #cast a rectangular "shadow" on the grid
        if self.drawgrid:
            rectx=x-x%self.gridsize
            recty=y-y%self.gridsize
            #free up the grid for Dragged
            if rectx/self.gridsize<len(self.grid) and recty/self.gridsize<len(self.grid[0]) and self.grid[rectx/self.gridsize][recty/self.gridsize]==source:
                self.grid[rectx/self.gridsize][recty/self.gridsize]=None
            #redraw the shadow iff there's nothing there
            if rectx/self.gridsize<len(self.grid) and recty/self.gridsize<len(self.grid[0]) and self.grid[rectx/self.gridsize][recty/self.gridsize] is None:
                #delete old rectangle
                self.delete('shadow')
                #make new rectangle
                self.create_rectangle(rectx,recty,rectx+self.gridsize,recty+self.gridsize,fill="gray",tags='shadow')
                self.tag_raise(source.id,'shadow')
        
    def dnd_leave(self,source,event):
        #This is called when the mouse pointer goes from inside the
        #    Target Widget to outside the Target Widget.
        #Since the mouse pointer is just now leaving us (the TargetWidget), we
        #    ask the DraggedObject to remove the representation of itself that it
        #    had previously drawn on us.
        source.vanish()
        #remove shadow
        self.delete('shadow')

        
    def dnd_motion(self,source,event):
        #This is called when the mouse pointer moves within the TargetWidget.
        #Figure out where the mouse is with respect to this widget
        xy = mouse_in_widget(self,event)
        #Ask the DraggedObject to move it's representation of itself to the
        #    new mouse pointer location.



        width = self.winfo_width()
        height = self.winfo_height()
        (x,y)=xy
        bounds = (0,0,width,height)
        source.move(xy,bounds)
        #cast a rectangle "shadow" on a grid
        if self.drawgrid:
            rectx=x-x%self.gridsize
            recty=y-y%self.gridsize
            #free up the grid for Dragged
            if rectx/self.gridsize<len(self.grid) and recty/self.gridsize<len(self.grid[0]) and self.grid[rectx/self.gridsize][recty/self.gridsize]==source:
                self.grid[rectx/self.gridsize][recty/self.gridsize]=None
            #redraw the shadow iff there's nothing there
            if rectx/self.gridsize<len(self.grid) and recty/self.gridsize<len(self.grid[0]) and self.grid[rectx/self.gridsize][recty/self.gridsize] is None:
                #delete old rectangle
                self.delete('shadow')
                #make new rectangle
                self.create_rectangle(rectx,recty,rectx+self.gridsize,recty+self.gridsize,fill="gray",tags="shadow")
                self.tag_raise(source.id,'shadow')
        
    def dnd_commit(self,source,event):
        #This is called if the DraggedObject is being dropped on us.
        if self.drawgrid:
            #snap Dragged to grid
            width = self.winfo_width()
            height = self.winfo_height()
            bounds = (0,0,width,height)
            #position should be the position of the shadow
            try:
                x,y,_,_=self.coords('shadow')
            except ValueError:
                #this means there was no shadow when dropping, which means a Dragged entered above a
                #non-empty square, which means we want to cancel our commitment to accept the drop
                self.dnd_leave(source,event)
                return
            xy=(x,y)
            source.set_pos(xy)
            #remove shadow
            self.delete('shadow')
            #mark its place in the grid
            self.grid[int(x/self.gridsize)][int(y/self.gridsize)] = source



class Inventory(CanvasDnd):
    """
    A small Canvas that loads images and keeps them left-justified.
    """
    def __init__(self,master,items,**kw):
        self.objects = []
        self.height = 0
        self.left = 5
        for image in items:
            obj = Dragged(image)
            self.objects.append(obj)
            xy = self.left,5
            obj.set_pos(xy)
            self.left+=obj.winfo_width()+5
            #make this widget's height default to the max height of its items
            if obj.winfo_height()>self.height:
                self.height = obj.winfo_height()
        if not kw.has_key('height') or self.height+5>kw['height']:
            kw['height']=self.height+5
        if not kw.has_key('width') or self.width>kw['width']:
            kw['width']=self.left
        CanvasDnd.__init__(self, master, **kw)
        bounds = 0,0,self.left,self.height+5
        for obj in self.objects:
            obj.appear(self,bounds=bounds)
            self.tag_bind(obj.id,'<ButtonPress>',obj.press)
            
    def delete(self,id):
        self.left=5
        CanvasDnd.delete(self,id)
        for obj in self.objects[:]:
            if hasattr(obj,'original_id') and obj.original_id==id and obj.canvas<>self:
                self.objects.remove(obj)
            else:
                xy=self.left,5
                obj.set_pos(xy)
                self.left+=(obj.winfo_width()+5)
        
    def dnd_commit(self,source,event):
        xy = self.left,5
        source.set_pos(xy)
        self.left+=source.winfo_width()+5
        if source not in self.objects:
            self.objects.append(source)
        

class TrashBin(CanvasDnd):
    """
    A Canvas specifically for deleting dragged objects.
    """
    def __init__(self,master,**kw):
        #Set default height/width if user didn't specify.
        if not kw.has_key('width'):
            kw['width'] =150
        if not kw.has_key('height'):
            kw['height'] = 25
        CanvasDnd.__init__(self, master, **kw)
        #Put the text "trash" in the middle of the canvas
        X = kw['width'] / 2
        Y = kw['height'] /2
        self.create_text(X,Y,text='TRASH')
    
    def dnd_commit(self,source,event):
        """
        Accept an object dropped in the trash.
        
        Note that the dragged object's 'dnd_end' method is called AFTER this
            routine has returned. We call the dragged objects "vanish(all=1)"
            routine to get rid of any labels it has on any canvas. Having done
            so, it will, at 'dnd_end' time, allow itself to evaporate. If you
            DON'T call "vanish(all=1)" AND there is a phantom label of the dragged
            object on an original_canvas then the dragged object will think it 
            has been erroniously dropped in the middle of nowhere and it will 
            resurrect itself from the original_canvas label. Since we are trying 
            to trash it, we don't want this to happen.
        """
        #tell the dropped object to remove ALL labels of itself.
        source.vanish(all=1)

if __name__ == "__main__":

    def on_dnd_start(event):
        """
        This is invoked by initiation_object to start the drag and drop process
        """
        #Create an object to be dragged
        try:
            image = Image.open("emoji/monsters/1.gif")
        except IOError:
            tkMessageBox.showerror(
                "Open file",
                "No emoji available! Ensure there are images in the folders emoji/land and emoji/monsters"
            )
            return
        thing_to_drag = Dragged(image)
        thing_to_drag.offset_x=20
        thing_to_drag.offset_y=10
        #Pass the object to be dragged and the event to Tkdnd
        Tkdnd.dnd_start(thing_to_drag,event)

    
    Root = Tk()
    Root.title('Drag-and-drop "real-world" demo')

    #Create a button to act as the initiation_object and bind it to <ButtonPress> so
    #    we start drag and drop when the user clicks on it.
    #The only reason we display the content of the trash bin is to show that it
    #    has no objects, even after some have been dropped on it.
    initiation_object = Button(Root,text='initiation_object')
    initiation_object.pack(side=TOP)
    initiation_object.bind('<ButtonPress>',on_dnd_start)
    
    #Create two canvases to act as the Target Widgets for the drag and drop. Note that
    #    these canvases will act as both the TargetWidget AND the TargetObject.
    items = []
    try:
        for i in range(5):
            items.append(Image.open("emoji/monsters/"+str(i+1)+".gif"))
    except IOError:
        tkMessageBox.showerror(
            "Open file",
            "No emoji available! Ensure there are images in the folders emoji/land and emoji/monsters"
        )
    target_widget_target_object = Inventory(Root,items,relief=RAISED,bd=2,background='white')
    target_widget_target_object.pack(expand=YES,fill=BOTH)
    
    target_widget_target_object2 = CanvasDnd(Root,5,5,True,relief=RAISED,bd=2,background='white')
    target_widget_target_object2.pack(expand=YES,fill=BOTH)
    
    #Create an instance of a trash can so we can get rid of dragged objects
    #    if so desired.
    trash = TrashBin(Root, relief=RAISED,bd=2)
    trash.pack(expand=NO)
    

    
    Root.mainloop()