'''
Created on Aug 1, 2019

@author: Daphne
'''

import wx
import csv

from MatchPair import Match_Pair
from FlexishGridBagSizer import FlexishGridBagSizer as custom_sizer
    
class My_Frame(wx.Frame):
    def __init__(self):
        super().__init__(parent=None, title='GridBagFrame')
        self.deck_filepath = "Test File.txt"
        self.current_deck = []
        self.cur_deck_length = 0
        
        self.current_set = 0
        self.study_start = 0
        self.study_range = 10
        self.correct_matches = [0,0]   #[amount correct, total amount of cards displayed thus far]
        
        self.top_panel = wx.Panel(self, name="top-level panel")
        
        #Sizer creation:
        self.base_sizer = wx.BoxSizer(wx.HORIZONTAL)
        
        self.container_sizer = wx.StaticBoxSizer(wx.HORIZONTAL, self.top_panel, label="container")
        self.game_sizer = wx.StaticBoxSizer(wx.VERTICAL, self.top_panel, label="game")
        self.status_sizer = wx.StaticBoxSizer(wx.VERTICAL, self.top_panel, label="status")
        
        self.drop_sizer = wx.StaticBoxSizer(wx.HORIZONTAL, self.top_panel, label="drop here")
        self.drag_sizer = wx.StaticBoxSizer(wx.HORIZONTAL, self.top_panel, label="drag these")
        
        #Sizer adding and setting: drop and drag -> game |then| game and status -> container |then| container -> panel -> base
        
        self.game_sizer.Add(self.drop_sizer, 1, wx.ALL | wx.EXPAND | wx.ALIGN_CENTER)   #adding wx.EXPAND will make these strech with the window
        self.game_sizer.Add(self.drag_sizer, 2, wx.ALL | wx.EXPAND | wx.ALIGN_CENTER)
        
        self.container_sizer.Add(self.game_sizer, 3, wx.ALL | wx.EXPAND | wx.ALIGN_CENTER)
        self.container_sizer.Add(self.status_sizer, 1, wx.ALL | wx.EXPAND)
        
        self.top_panel.SetSizer(self.container_sizer)
        
        self.base_sizer.Add(self.top_panel, 1, wx.ALL | wx.EXPAND)
        
        self.SetSizer(self.base_sizer) 
        
        #status_sizer widgets:
        self.next_btn = wx.Button(self.top_panel, label="Next Set")
        self.next_btn.Bind(wx.EVT_BUTTON, self.create_populated_game_GUI)
        self.status_sizer.Add(self.next_btn, 0, wx.ALL | wx.ALIGN_CENTER)
        
        #Creation of dynamic GUI and non-GUI elements:
        self.listify_deck(self.deck_filepath)
        self.create_populated_game_GUI()  #creates SortaFlexiGridBagSizers, populates them, and adds them to drag and drop sizers
        
        self.Show()
        
    def inform_end_of_deck(self):
        self.next_btn.Unbind(wx.EVT_BUTTON)
        self.next_btn.SetLabel("You reached the end...\nYABAI!!!")
        
    def listify_deck(self, filepath):
        #parse deck file into list:
        with open(filepath, "r", encoding="utf8") as deck_file:
            deck_list = list(csv.reader(deck_file, delimiter="\t"))   #uses csv reader to get each line of deck_part as a list and puts them into a list of lists
            self.current_deck = deck_list   #keeps entire deck in memory for life of frame. Might be memory expensive
            self.cur_deck_length = len(deck_list)
    
    def create_populated_game_GUI(self, event=None):
        #This is ALMOST the only function in this class that directly refers to "self" variables. Only exceptions are "self.current_deck" and "self.cur_deck_length" which are referred to in create_populated_pairs()
        #All other functions in this class have the self variables passed into their local scope
        #If this func was called by an event, then drop and drag sizer grids already exist.
        #Determine how many correct matches were made before the set was changed
        #Then delete existing grids and their children to make room for new ones   
        if (event is not None):
            self.drop_sizer.Clear(delete_windows = True)
            self.drag_sizer.Clear(delete_windows = True)
            
            self.correct_matches[1] += self.study_range         #updates the amount of total possible matches the user could've made up to and including this set
            print ("correct matches: {} out of {}".format(self.correct_matches[0], self.correct_matches[1]))
            self.current_set += 1                               #increment the current set of cards out of deck
            
        start_of_set = self.study_start + (self.study_range * self.current_set)  #user-defined starting point + (study_rage * the amount of sets requested this session, beginning at 0)
        safe_range = self.study_range
        
        #check study range to ensure we stay inbounds of deck list:
        if (start_of_set + safe_range > self.cur_deck_length):
            amount_over = (start_of_set + safe_range) - self.cur_deck_length
            safe_range -= amount_over
            self.inform_end_of_deck()
            
        #create new list of pairs for this set, then create grids populated by those pairs:
        match_list = self.create_populated_pairs(self.top_panel, self.current_deck, self.correct_matches, start_of_set, safe_range)
        grid_tup = self.create_grids(match_list, self.study_range)
        
        #pack new grids into their existing sizers from __init__:
        self.drop_sizer.Add(grid_tup[0], 1, wx.ALL | wx.ALIGN_CENTER)
        self.drag_sizer.Add(grid_tup[1], 1, wx.ALL | wx.ALIGN_CENTER)
        
        #get new minimum size of base_sizer necessary to fit top_panel after its new grids were added:
        new_min_size = self.base_sizer.ComputeFittingClientSize(self.top_panel)
        
        #if new length or width is greater than the frame's current size, set a new minimum to properly fit contents, resize box_sizer, and force a layout update:
        if(new_min_size[0] > self.GetSize()[0] or new_min_size[1] > self.GetSize()[1]):
            self.SetMinClientSize(new_min_size)
            self.SetSize(new_min_size)
            self.Layout()
        else:   #if new size is not bigger than window length, do not force a resize, but allow user to resize window to the new, smaller minimum size
            self.SetMinClientSize(new_min_size)
            self.Layout()
    
    def create_populated_pairs(self, parent_panel, deck_list, match_counter, study_start, study_range):
        match_list = []
        #create MatchPairs populated by vocab in study_range taken from deck_list:
        for x in range(study_range):
            card = deck_list[study_start+x]
            pair = Match_Pair(parent_panel, match_counter)
            pair.get_Donkey().SetLabel("{}".format(card[0]))
            pair.get_Tail().SetLabel("{}\n{}".format(card[2], card[1]))
            match_list.append(pair)
            
        return match_list
    
    def create_grids(self, match_pairs, study_range):
        
        donkey_grid = custom_sizer(study_range)
        tail_grid = custom_sizer(study_range)
        
        for pair in match_pairs:
            print("")
            donkey_grid.add_to_random(pair.get_Donkey())
            tail_grid.add_to_random(pair.get_Tail())
            
        donkey_grid.make_all_growable()
        donkey_grid.SetFlexibleDirection(wx.BOTH)
        
        tail_grid.make_all_growable()
        tail_grid.SetFlexibleDirection(wx.BOTH)
            
        return (donkey_grid, tail_grid)