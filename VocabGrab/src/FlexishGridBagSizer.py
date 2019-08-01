'''
Created on Aug 1, 2019

@author: Daphne
'''

import wx
import math
import random

#Using GridBagSizer as opposed to just FlexGridSizer allows determining the necessary number of rows and columns upon creation.
class FlexishGridBagSizer(wx.GridBagSizer):
    def __init__(self, num_items):
        super().__init__(10,10)
        self.num_items = num_items
        self.num_cols = 0
        self.num_rows = 0

        self.calc_lowest_col_row(self.num_items)    #rows and columns should be calculated on instantiation for correct functioning of add functions
    
    def make_all_growable(self):
        for col in range(self.GetCols()-1): #Range() is already exclusive, so the -1 actually means that the right-most column will not be set to growable   
            self.AddGrowableCol(col)        #This prevents wasteful white-space between right-most column and its sizer as a side-effect of the growth
         
        for row in range(self.GetRows()):
            self.AddGrowableRow(row)
            
    #implicit differentiation may be the key to coming up with a really certain math formula for this:
    def calc_lowest_col_row(self, num_items):
        self.num_rows = math.floor(math.sqrt(num_items))           #Uses sqrt to get a number of columns that allows staying as close as possible to a square geometry of columns x rows
        self.num_cols = math.ceil(num_items/self.num_rows)          #divides to figure out how many more rows we need in order to fit total number of items, and ceilings up to account for fractions
        #print("cols: {}, rows: {}".format(self.num_cols, self.num_rows))
    
    def add_to_random(self, obj):
        rand_row = random.randint(0, self.num_rows-1)
        rand_col = random.randint(0, self.num_cols-1)
        pos = wx.GBPosition(rand_row, rand_col)
        new_obj = wx.GBSizerItem(obj, pos)
        
        #If an object already exists at pos (which causes Add() to raise an error), do function again to reroll for empty random pos
        if not (self.CheckForIntersection(new_obj)): #if inserting obj at position would not cause an overlap:
            self.Add(new_obj)
        else:
            #print ("An item already exists at position: {}".format(pos))
            self.add_to_random(obj)