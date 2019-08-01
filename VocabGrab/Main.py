'''
Created on Aug 1, 2019

@author: Daphne
'''
import wx
import GameFrame

if __name__ == '__main__':
    test_app = wx.App()
    test_frame = GameFrame.My_Frame()
    test_app.MainLoop()