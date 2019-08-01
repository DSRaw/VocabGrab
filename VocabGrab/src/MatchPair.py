'''
Created on Aug 1, 2019

@author: Daphne
'''

import wx

class Match_Pair():
    '''
    @Description: This class facilitates both a "drag cycle", and a method for checking for matches between dragged objects. A drag cycle via this class begins with the creation of a Donkey and a Tail button as a pair. ***FINISH WRITING***
    @NOTABLE ATTRIBUTES:
    @parent: Receives top-level frame when this object is created 
    @self.Donkey: The button that REPRESENTS a target to which an object should be dragged
    @self.Tail: The button that REPRESENTS the information that is to be dragged to Donkey
    @self.drag_frame: Created within on_drag_start(). This is the ACTUAL object (wx.Frame with a child wx.Button) that will be draggable around the screen
    '''
    def __init__(self, parent_panel, match_counter):
        self.panel = parent_panel
        self.match_counter = match_counter #takes an outside variable to enable each match pair to add to a count of how many have been successfully matched
        self.delta = 0
        self.drag_frame = None
        
        self.AlreadyMatched = False #Can replace this by having on_release return _check_OnTarget's return value

        #Creation of widgets involved in visual representation of dragging process:
        self.Donkey = wx.Button(self.panel)
        self.Tail = wx.Button(self.panel)
        
        #The first of 2 events bound to Tail. Beginning of the drag cycle. All other events involved in drag cycle are created from within this event's handler function:
        self.Tail.Bind(wx.EVT_LEFT_DOWN, self.on_click)
    
#Non-event functions:
    def get_Donkey(self):
        return self.Donkey
    
    def get_Tail(self):
        return self.Tail
    
    def get_delta(self):
        return self.delta
    
    def get_dframe(self):
        return self.drag_frame
    
    def set_delta(self, tupl):
        self.delta = tupl
        
    def set_dframe(self, frame):
        self.drag_frame = frame
        
    def increment_match_counter(self):
        self.match_counter[0] +=1
        
    def check_match_and_reset(self):
        #When a drag cycle has finished, any straggling dragframes must be destroyed and Tail must either be reset to Shown or left Hidden if match was successful
        if(not self.AlreadyMatched):  #This prevents Tail from being being made visible again if EVT_LEAVE/ENTER_WINDOW was due to a successful match rather than unexpected loss of focus
            self.get_Tail().Show()
        
        if (self.get_dframe()): #if drag_frame still exists in any form, destroy it, regardless for reason why check_match was called
            self.get_dframe().Destroy()
            self.set_dframe(None)
        
        #These should be unbound regardless of whether or not a match was made:
        self.get_Tail().Unbind(wx.EVT_MOTION)
        self.panel.Unbind(wx.EVT_ENTER_WINDOW)
            
    def _check_OnTarget(self):  #Will check if the mouse is within the Donkey button's area on_release of the dragging event
        #Sets and Returns bool value of OnTarget based on whether or not the mouse is within the area of the Donkey btn on_release() of Tail's drag cycle
        #Does this by calculating the difference in distance (delta) between the mouse on release of dragging event and the origin point og Donkey btn
        #If statements delta is less than the width and height of Donkey btn. If yes, mouse is OnTarget (return True), otherwise mouse is not OnTarget (return False)
        Donkey_size = self.get_Donkey().GetSize()
        Donkey_pos = self.get_Donkey().GetPosition()
        m_pos = self.panel.ScreenToClient(wx.GetMousePosition())
        Donkey_delta = m_pos - Donkey_pos
        OnTarget = False
        if(Donkey_delta.x >= 0 and Donkey_delta.x <= Donkey_size.width):
            if(Donkey_delta.y >= 0 and Donkey_delta.y <= Donkey_size.height):
                OnTarget = True
                self.AlreadyMatched = True
                self.increment_match_counter()
        return (OnTarget)

#Event handler functions:
    def on_click(self, event):
        #These events are triggered very frequently by common mouse movement
        #by not binding these immediately, we prevent unnecessary event calls every time the cursor passes over a button or the parent panel
        self.panel.Bind(wx.EVT_ENTER_WINDOW, self.on_parent_reentry) #will destroy dragframe(if it's been created already) when mouse leaves dragframe and reenters parent panel
        event.GetEventObject().Bind(wx.EVT_MOTION, self.on_drag_start)
        
    #Events for Tail and drag_frame:    
    def on_drag_start(self, event):
        #Gets the origin of the Tail button in the parents geometry, and calculates the difference between Tails' starting position and where the mouse was first clicked, allowing the mouse position to stay constant relative to the button origin throughout the drag.
        #The calculations in the Calculation block can only be done here because the Tail button (the calling object) immediately loses focus and exits it's event cycle once drag_frame is created and shown over top of it. At that point, the events bound to drag_frame from within this function take over.
        #If significantly changing the placement of drag_frame's creation, consider moving these calculations from here to a separate left-click event bound to Tail.
        if(event.Dragging() and event.LeftIsDown()):
            # Begin Calculation block #
            btn_start_pos = event.GetEventObject().GetPosition()                #gets btn position in terms of its parent panel
            self.set_delta(self.panel.ScreenToClient(wx.GetMousePosition()) - btn_start_pos)   #put mouse pos in terms of same parent panel before subtracting
            btn_scrn_pos = self.panel.ClientToScreen(btn_start_pos)                #puts btn pos in terms of screen so it can be directly passed to drag_frame
            # End Calculation block #
            
            #Creation of frame and its child button used to visually represent the drag operation
            #Uses self so that event handlers later in cycle can refer to it for destruction. May be replaceable by getting parent of event.GetEventObject
            drag_label = event.GetEventObject().GetLabel()  #gets Tail's label for use as drag_btn's label
            drag_frame = wx.Frame(self.panel, pos=btn_scrn_pos, style=wx.BORDER_NONE | wx.FRAME_FLOAT_ON_PARENT | wx.FRAME_NO_TASKBAR)
            drag_btn = wx.Button(drag_frame, label=drag_label)
            
            #Add button to drag_frame's geometry. SetSizerAndFit will ensure the frame is only large enough to hold the button
            sizer = wx.BoxSizer(wx.HORIZONTAL)
            sizer.Add(drag_btn, 1, wx.ALL | wx.EXPAND)
            drag_frame.SetSizerAndFit(sizer)
            
            #Once the frame is shown, the dragging operation is now handled by the following events:
            #EVT_LEAVE_WINDOW will help prevent cases where Destroy() is not called because the frame's focus get's unexpectedly pulled away by the client's OS before the mouse button is actually released.
            drag_btn.Bind(wx.EVT_MOTION, self.on_dragging)
            drag_btn.Bind(wx.EVT_LEFT_UP, self.on_release)     #LEFT_UP and LEAVE_WINDOW are both called when Donkey is destroyed in on_release
            drag_btn.Bind(wx.EVT_LEAVE_WINDOW, self.on_leave)  #Therefore, separate events are required to avoid duplicating calls to code within on_release

            drag_frame.Show()
            self.get_Tail().Hide()
            
            self.set_dframe(drag_frame)

        event.Skip()
        
    def on_dragging(self, event):
        #Moves drag_frame along with the mouse's movement. Subtracts delta from the current mouse position, in order to keep the cursor constant relative to the drag_frame.
        if(event.LeftIsDown() and self.get_dframe()): #if left is held AND dragframe still exists might need to re-add event.Dragging() is there's any weird behavior
            m_pos = wx.GetMousePosition()
            new_pos = m_pos - self.get_delta()
            self.get_dframe().Move(new_pos)
        event.Skip()
        
    def on_release(self, event):
        if(self._check_OnTarget()):  #if Tail is within area of Donkey when drag is released
            self.get_Donkey().Disable() #if match was successful, disable Donkey for visual feedback
        self.check_match_and_reset()
        event.Skip()
    
    #extra assurance that any dragframes that were unexpectedly not destroyed are killed when mouse leaves dragframe and/or renters the parent panel
    def on_leave(self, event):
        self.check_match_and_reset()
        event.Skip()
        
    def on_parent_reentry(self, event): #extra assurance that any dragframes that were unexpectedly not destroyed are killed when the mouse renters the parent panel
        self.check_match_and_reset()
        event.Skip()
        
        