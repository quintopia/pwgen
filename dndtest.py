

"""
This code demonstrates a real-world drag and drop.
"""

#Set Verbosity to control the display of information messages:
#    2 Displays all messages
#    1 Displays all but dnd_accept and dnd_motion messages
#    0 Displays no messages
Verbosity = 0

#When you drag an existing object on a canvas, we normally make the original
#    label into an invisible phantom, and what you are ACTUALLY dragging is
#    a clone of the objects label. If you set "LeavePhantomVisible" then you
#    will be able to see the phantom which persists until the object is
#    dropped. In real life you don't want the user to see the phantom, but
#    for demonstrating what is going on it is useful to see it. This topic
#    beaten to death in the comment string for Dragged.Press, below.
LeavePhantomVisible = 0

from Tkinter import *
import Tkdnd
from PIL import Image,ImageTk

def MouseInWidget(Widget,Event):
    """
    Figure out where the cursor is with respect to a widget.
    
    Both "Widget" and the widget which precipitated "Event" must be
        in the same root window for this routine to work.
        
    We call this routine as part of drawing a DraggedObject inside a
        TargetWidget, eg our Canvas. Since all the routines which need
        to draw a DraggedObject (dnd_motion and it's friends) receive
        an Event, and since an event object contain e.x and e.y values which say
        where the cursor is with respect to the widget you might wonder what all
        the fuss is about; why not just use e.x and e.y? Well it's never
        that simple. The event that gets passed to dnd_motion et al was an
        event against the InitiatingObject and hence what e.x and e.y say is 
        where the mouse is WITH RESPECT TO THE INITIATINGOBJECT. Since we want
        to know where the mouse is with respect to some other object, like the
        Canvas, e.x and e.y do us little good. You can find out where the cursor
        is with respect to the screen (w.winfo_pointerxy) and you can find out
        where it is with respect to an event's root window (e.*_root). So we
        have three locations for the cursor, none of which are what we want.
        Great. We solve this by using w.winfo_root* to find the upper left
        corner of "Widget" with respect to it's root window. Thus we now know
        where both "Widget" and the cursor (e.*_root) are with respect to their
        common root window (hence the restriction that they MUST share a root
        window). Subtracting the two gives us the position of the cursor within
        the widget. 
        
    Yes, yes, we could have said:
        return (Event.X_root-Widget.winfo_rootx(),Event.y_root-Widget.winfo_rooty())
    and done it all on one line, but this is DEMO code and the three line version
    below makes it rather more obvious what's going on. 
    """
    x = Event.x_root - Widget.winfo_rootx()
    y = Event.y_root - Widget.winfo_rooty()
    return (x,y)

def MouseInItem(Canvas,ID,Event):
    x1,y1 = Canvas.coords(ID)
    print x1,y1
    x1 = x1 + Canvas.winfo_rootx()
    y1 = y1 + Canvas.winfo_rooty()
    x = Event.x_root - x1
    y = Event.y_root - y1
    return (x,y)
    
def Blab(Level,Message):
    """
    Display Message if Verbosity says to.
    """
    if Verbosity >= Level:
        print Message
    
class Dragged:
    """
    This is a prototype thing to be dragged and dropped.
    
    Derive from (or mixin) this class to creat real draggable objects.
    """
    #We use this to assign a unique number to each instance of Dragged.
    #    This isn't a necessity; we do it so that during the demo you can
    #    tell one instance from another.
    NextNumber = 0
    
    def __init__(self):
        Blab(1, "An instance of Dragged has been created")
        #When created we are not on any canvas
        self.Canvas = None
        self.OriginalCanvas = None
        #This sets where the mouse cursor will be with respect to our label
        self.OffsetX = 20
        self.OffsetY = 10
        #Assign ourselves a unique number
        self.Number = Dragged.NextNumber
        Dragged.NextNumber += 1
        #Use the number to build our name
        self.Name = 'DragObj-%s'%self.Number
        self.image = Image.open("emoji/monsters/1.gif")
        self.imagetk = ImageTk.PhotoImage(self.image)
        
    def dnd_end(self,Target,Event):
        #this gets called when we are dropped
        Blab(1, "%s has been dropped; Target=%s"%(self.Name,`Target`))
        if self.Canvas==None and self.OriginalCanvas==None:
            #We were created and then dropped in the middle of nowhere, or
            #    we have been told to self destruct. In either case
            #    nothing needs to be done and we will evaporate shortly.
            return
        if self.Canvas==None and self.OriginalCanvas<>None:
            #We previously lived on OriginalCanvas and the user has
            #   dragged and dropped us in the middle of nowhere. What you do
            #   here rather depends on your own personal taste. There are 2 choices:
            #   1) Do nothing. The dragged object will simply evaporate. In effect
            #      you are saying "dropping an existing object in the middle
            #      of nowhere deletes it".  Personally I don't like this option because
            #      it means that if the user, while dragging an important object, 
            #      twitches their mouse finger as the object is in the middle of
            #      nowhere then the object gets immediately deleted. Oops.
            #   2) Resurrect the original label (which has been there but invisible)
            #      thus saying "dropping an existing dragged object in the middle of
            #      nowhere is as if no drag had taken place". Thats what the code that
            #      follows does.
            self.Canvas = self.OriginalCanvas
            self.ID = self.OriginalID
            self.Canvas.itemconfig(self.ID,state=NORMAL)
            #We call the canvases "dnd_enter" method here to keep its ObjectDict up
            #    to date. We know that we had been dragged off the canvas, so before
            #    we call "dnd_enter" the cansases ObjectDict says we are not on the
            #    canvas. The call to "dnd_enter" will till the canvas that we are,
            #    in effect, entering the canvas. Note that "dnd_enter" will in turn
            #    call our "Appear" method, but "Appear" is smart enough to realize
            #    that we already have a label on self.Canvas, so it quietly does
            #    does nothing,
            self.Canvas.dnd_enter(self,Event)
            return
        #At this point we know that self.Canvas is not None, which means we have an
        #    label of ourself on that canvas. Bind <ButtonPress> to that label so the
        #    the user can pick us up again if and when desired.            
        self.Canvas.tag_bind(self.ID,'<ButtonPress>',self.Press)
        #If self.OriginalCanvas exists then we were an existing object and our
        #    original label is still around although hidden. We no longer need
        #    it so we delete it.
        if self.OriginalCanvas:
            self.OriginalCanvas.delete(self.OriginalID)
            self.OriginalCanvas = None
            self.OriginalID = None
            
    def winfo_height(self):
        x,y=self.image.size
        return y
        
    def winfo_width(self):
        x,y=self.image.size
        return x


    def Appear(self, Canvas, XY, Bounds):
        """
        Put an label representing this Dragged instance on Canvas.
        
        XY says where the mouse pointer is. We don't, however, necessarily want
            to draw our upper left corner at XY. Why not? Because if the user
            pressed over an existing label AND the mouse wasn't exactly over the
            upper left of the label (which is pretty likely) then we would like
            to keep the mouse pointer at the same relative position inside the
            label. We therefore adjust X and Y by self.OffsetX and self.OffseY
            thus moving our upper left corner up and/or left by the specified
            amounts. These offsets are set to a nominal value when an instance
            of Dragged is created (where it matters rather less), and to a useful
            value by our "Press" routine when the user clicks on an existing
            instance of us.
        """
        if self.Canvas:
            #we are already on a canvas; do nothing
            return
        self.X, self.Y = XY
        minx,miny,maxx,maxy = Bounds
        self.X = min(max(self.X-self.OffsetX,minx),maxx-self.winfo_width())+self.OffsetX
        self.Y = min(max(self.Y-self.OffsetY,miny),maxy-self.winfo_height())+self.OffsetY        

        #Display the label on a window on the canvas. We need the ID returned by
        #    the canvas so we can move the label around as the mouse moves.
        self.ID = Canvas.create_image((self.X-self.OffsetX, self.Y-self.OffsetY), image=self.imagetk, anchor="nw")
        #Note the canvas on which we drew the label.
        self.Canvas = Canvas

    def Vanish(self,All=0):
        """
        If there is a label representing us on a canvas, make it go away.
        
        if self.Canvas is not None, that implies that "Appear" had prevously
            put a label representing us on the canvas and we delete it.
            
        if "All" is true then we check self.OriginalCanvas and if it not None
            we delete from it the label which represents us.
        """
        if self.Canvas:
            #we have a label on a canvas; delete it
            self.Canvas.delete(self.ID)
            #flag that we are not represented on the canvas
            self.Canvas = None
            #Since ID and Label are no longer meaningful, get rid of them lest they
            #confuse the situation later on. Not necessary, but tidy.
            self.ID = None
        
        if All and self.OriginalCanvas:
            #Delete label representing us from self.OriginalCanvas
            self.OriginalCanvas.delete(self.OriginalID)
            self.OriginalCanvas = None
            del self.OriginalID

    def Move(self,XY,Bounds):
        """
        If we have a label a canvas, then move it to the specified location. 
        
        XY is with respect to the upper left corner of the canvas
        """    
        assert self.Canvas, "Can't move because we are not on a canvas"
        self.X, self.Y = XY
        minx,miny,maxx,maxy = Bounds
        #print self.OffsetX,self.OffsetY
        self.X = min(max(self.X-self.OffsetX,minx),maxx-self.winfo_width())+self.OffsetX
        self.Y = min(max(self.Y-self.OffsetY,miny),maxy-self.winfo_height())+self.OffsetY
        #print self.X-self.OffsetX,self.Y-self.OffsetY
        self.Canvas.coords(self.ID,self.X-self.OffsetX,self.Y-self.OffsetY)
        
    def SetPos(self,XY):
        """
        Move to exactly the position specified, don't worry about offsets
        """
        self.X, self.Y = XY
        self.Canvas.coords(self.ID,self.X,self.Y)

    def Press(self,Event):
        """
        User has clicked on a label representing us. Initiate drag and drop.
        """
        Blab(1, "Dragged.press")
        #Save our current label as the Original label
        self.OriginalID = self.ID
        self.OriginalCanvas = self.Canvas
        self.Canvas.itemconfig(self.ID,state=HIDDEN)
        #Say we have no current label    
        self.ID = None
        self.Canvas = None
        #Ask Tkdnd to start the drag operation
        if Tkdnd.dnd_start(self,Event):
            #Save where the mouse pointer was in the label so it stays in the
            #    same relative position as we drag it around
            self.OffsetX, self.OffsetY = MouseInItem(self.OriginalCanvas,self.OriginalID,Event)
            #print self.OffsetX, self.OffsetY
            #Draw a label of ourself for the user to drag around
            XY = MouseInWidget(self.OriginalCanvas,Event)
            width = self.OriginalCanvas.winfo_width()
            height = self.OriginalCanvas.winfo_height()
            Bounds = (0,0,width,height)
            self.Appear(self.OriginalCanvas,XY,Bounds)
    
class CanvasDnd(Canvas):
    """
    A canvas to which we have added those methods necessary so it can
        act as both a TargetWidget and a TargetObject. 
        
    Use (or derive from) this drag-and-drop enabled canvas to create anything
        that needs to be able to receive a dragged object.    
    """    
    def __init__(self, Master, *args, **kw):
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
        Canvas.__init__(self, Master, kw)
        #ObjectDict is a dictionary of dragable object which are currently on
        #    this canvas, either because they have been dropped there or because
        #    they are in mid-drag and are over this canvas.
        self.ObjectDict = {}
        #draw gridlines
        if self.drawgrid:
            for i in range(1,gridx):
                self.create_line(self.gridsize*i,0,self.gridsize*i,gridy*self.gridsize,fill='gray')
            for i in range(1,gridy):
                self.create_line(0,self.gridsize*i,gridx*self.gridsize,self.gridsize*i,fill='gray')

    #----- TargetWidget functionality -----
    
    def dnd_accept(self,Source,Event):
        #Tkdnd is asking us (the TargetWidget) if we want to tell it about a
        #    TargetObject. Since CanvasDnd is also acting as TargetObject we
        #    return 'self', saying that we are willing to be the TargetObject.
        Blab(2, "Canvas: dnd_accept")
        #we aren't ready to accept unless there is a shadow present or the area under the Dragged is clear
        return self

    #----- TargetObject functionality -----

    def dnd_enter(self,Source,Event):
        #This is called when the mouse pointer goes from outside the
        #   Target Widget to inside the Target Widget.
        Blab(1, "Receptor: dnd_enter")
        #Figure out where the mouse is with respect to this widget
        XY = MouseInWidget(self,Event)
        #Since the mouse pointer is just now moving over us (the TargetWidget),
        #    we ask the DraggedObject to represent itself on us.
        #    "Source" is the DraggedObject.
        #    "self" is us, the CanvasDnd on which we want the DraggedObject to draw itself.
        #    "XY" is where (on CanvasDnd) that we want the DraggedObject to draw itself.
        x,y = XY

        width = self.winfo_width()
        height = self.winfo_height()
        Bounds = (0,0,width,height)
        XY = (x,y)
        Source.Appear(self,XY,Bounds)
        #cast a rectangular "shadow" on the grid
        if self.drawgrid:
            rectx=x-x%self.gridsize
            recty=y-y%self.gridsize
            #free up the grid for Dragged
            if rectx/self.gridsize<len(self.grid) and recty/self.gridsize<len(self.grid[0]) and self.grid[rectx/self.gridsize][recty/self.gridsize]==Source:
                self.grid[rectx/self.gridsize][recty/self.gridsize]=None
            #redraw the shadow iff there's nothing there
            if rectx/self.gridsize<len(self.grid) and recty/self.gridsize<len(self.grid[0]) and self.grid[rectx/self.gridsize][recty/self.gridsize] is None:
                #delete old rectangle
                self.delete('shadow')
                #make new rectangle
                self.create_rectangle(rectx,recty,rectx+self.gridsize,recty+self.gridsize,fill="gray",tags='shadow')
                self.tag_raise(Source.ID,'shadow')
        #Add the DraggedObject to the dictionary of objects which are on this
        #    canvas.
        self.ObjectDict[Source.Name] = Source
        
    def dnd_leave(self,Source,Event):
        #This is called when the mouse pointer goes from inside the
        #    Target Widget to outside the Target Widget.
        Blab(1, "Receptor: dnd_leave")
        #Since the mouse pointer is just now leaving us (the TargetWidget), we
        #    ask the DraggedObject to remove the representation of itself that it
        #    had previously drawn on us.
        Source.Vanish()
        #remove shadow
        self.delete('shadow')
        #Remove the DraggedObject from the dictionary of objects which are on 
        #    this canvas
        del self.ObjectDict[Source.Name]
        
    def dnd_motion(self,Source,Event):
        #This is called when the mouse pointer moves within the TargetWidget.
        Blab(2, "Receptor: dnd_motion")
        Blab(2, "canvas width: "+str(self.winfo_width())+" and label width: "+str(Source.winfo_width()))
        #Figure out where the mouse is with respect to this widget
        XY = MouseInWidget(self,Event)
        #Ask the DraggedObject to move it's representation of itself to the
        #    new mouse pointer location.



        width = self.winfo_width()
        height = self.winfo_height()
        (x,y)=XY
        Bounds = (0,0,width,height)
        Source.Move(XY,Bounds)
        #cast a rectangle "shadow" on a grid
        if self.drawgrid:
            rectx=x-x%self.gridsize
            recty=y-y%self.gridsize
            #free up the grid for Dragged
            if rectx/self.gridsize<len(self.grid) and recty/self.gridsize<len(self.grid[0]) and self.grid[rectx/self.gridsize][recty/self.gridsize]==Source:
                self.grid[rectx/self.gridsize][recty/self.gridsize]=None
            #redraw the shadow iff there's nothing there
            if rectx/self.gridsize<len(self.grid) and recty/self.gridsize<len(self.grid[0]) and self.grid[rectx/self.gridsize][recty/self.gridsize] is None:
                #delete old rectangle
                self.delete('shadow')
                #make new rectangle
                self.create_rectangle(rectx,recty,rectx+self.gridsize,recty+self.gridsize,fill="gray",tags="shadow")
                self.tag_raise(Source.ID,'shadow')
        
    def dnd_commit(self,Source,Event):
        #This is called if the DraggedObject is being dropped on us.
        #This demo doesn't need to do anything here (the DraggedObject is
        #    already in self.ObjectDict) but a real application would
        #    likely want to do stuff here.
        Blab(1, "Receptor: dnd_commit; Object received= %s"%`Source`)
        if self.drawgrid:
            #snap Dragged to grid
            width = self.winfo_width()
            height = self.winfo_height()
            Bounds = (0,0,width,height)
            #position should be the position of the shadow
            try:
                x,y,_,_=self.coords('shadow')
            except ValueError:
                #this means there was no shadow when dropping, which means a Dragged entered above a
                #non-empty square, which means we want to cancel our commitment to accept the drop
                self.dnd_leave(Source,Event)
                return
            XY=(x,y)
            Source.SetPos(XY)
            #remove shadow
            self.delete('shadow')
            #mark its place in the grid
            self.grid[int(x/self.gridsize)][int(y/self.gridsize)] = Source

    #----- code added for demo purposes -----

    def ShowObjectDict(self,Comment):
        """
        Print Comment and then print the present content of our ObjectDict.
        """
        print Comment
        if len(self.ObjectDict) > 0:
            for Name,Object in self.ObjectDict.items():
                print '    %s %s'%(Name,Object)
        else:
            print "    <empty>"    

class TrashBin(CanvasDnd):
    """
    A canvas specifically for deleting dragged objects.
    """
    def __init__(self,Master,**kw):
        #Set default height/width if user didn't specify.
        if not kw.has_key('width'):
            kw['width'] =150
        if not kw.has_key('height'):
            kw['height'] = 25
        CanvasDnd.__init__(self, Master, **kw)
        #Put the text "trash" in the middle of the canvas
        X = kw['width'] / 2
        Y = kw['height'] /2
        self.create_text(X,Y,text='TRASH')
    
    def dnd_commit(self,Source,Event):
        """
        Accept an object dropped in the trash.
        
        Note that the dragged object's 'dnd_end' method is called AFTER this
            routine has returned. We call the dragged objects "Vanish(All=1)"
            routine to get rid of any labels it has on any canvas. Having done
            so, it will, at 'dnd_end' time, allow itself to evaporate. If you
            DON'T call "Vanish(All=1)" AND there is a phantom label of the dragged
            object on an OriginalCanvas then the dragged object will think it 
            has been erroniously dropped in the middle of nowhere and it will 
            resurrect itself from the OriginalCanvas label. Since we are trying 
            to trash it, we don't want this to happen.
        """
        Blab(1, "TrashBin: dnd_commit")
        #tell the dropped object to remove ALL labels of itself.
        Source.Vanish(All=1)
        #were a trash bin; don't keep objects dropped on us.
        self.ObjectDict.clear()    

if __name__ == "__main__":

    def on_dnd_start(Event):
        """
        This is invoked by InitiationObject to start the drag and drop process
        """
        #Create an object to be dragged
        ThingToDrag = Dragged()
        #Pass the object to be dragged and the event to Tkdnd
        Tkdnd.dnd_start(ThingToDrag,Event)

    def ShowObjectDicts():
        """
        Some demo code to let the user see what ojects we think are
            on each of the three canvases.
        """
        TargetWidget_TargetObject.ShowObjectDict('UpperCanvas')
        TargetWidget_TargetObject2.ShowObjectDict('LowerCanvas')
        Trash.ShowObjectDict('Trash bin')
        print '----------'
    
    Root = Tk()
    Root.title('Drag-and-drop "real-world" demo')

    #Create a button to act as the InitiationObject and bind it to <ButtonPress> so
    #    we start drag and drop when the user clicks on it.
    #The only reason we display the content of the trash bin is to show that it
    #    has no objects, even after some have been dropped on it.
    InitiationObject = Button(Root,text='InitiationObject')
    InitiationObject.pack(side=TOP)
    InitiationObject.bind('<ButtonPress>',on_dnd_start)
    
    #Create two canvases to act as the Target Widgets for the drag and drop. Note that
    #    these canvases will act as both the TargetWidget AND the TargetObject.
    TargetWidget_TargetObject = CanvasDnd(Root,5,5,True,relief=RAISED,bd=2,background='white')
    TargetWidget_TargetObject.pack(expand=YES,fill=BOTH)
    
    TargetWidget_TargetObject2 = CanvasDnd(Root,5,5,True,relief=RAISED,bd=2,background='white')
    TargetWidget_TargetObject2.pack(expand=YES,fill=BOTH)
    
    #Create an instance of a trash can so we can get rid of dragged objects
    #    if so desired.
    Trash = TrashBin(Root, relief=RAISED,bd=2)
    Trash.pack(expand=NO)
    
    #Create a button we can press to display the current content of the
    #    canvases ObjectDictionaries.
    Button(text='Show canvas ObjectDicts',command=ShowObjectDicts).pack()
    
    Root.mainloop()