# VocabGrab
A fresh attempt at my old VocabDrag project, this time using wxPython

**2019/08/01 version 0.0.0a**
My attempt at creating smooth drag and drop functionality in wxPython turned into writing most of the basic code for gameplay.

**Summary of Functionality:**

Technical:

This is a very early vision of the functionality. Some features that are intended to be user-selectable are currently hard-coded. These include: The path to the file containing the vocabulary list, which fields are displayed in the drag and drop areas, the starting point in the list, and the amount of words to display par session. The file parsing logic also assumes that your file is formatted similarly to this: "vocab word, meaning, additional info" with each single line having a single word on it. "Test File.txt" is a brief example.

Gameplay:

This program creates a drag and drop matching game from a file containing a list of vocabulary words. Each piece of info about a single vocabulary word is split onto the labels of "Donkey buttons" and "Tail buttons". A Tail button can be dragged to its matching Donkey button, at which point the program will count it as a match and disable the Donkey button to provide visual feedback. Once an entire set of vocabulary has been matched, a new set can be requested via the "Next Set" button on the left. Once the end of the vocabulary list has been reached, the "Next Set" button will be disabled, and will display a message indicating that there is no further vocabulary in the list.

**Module Overview:**

*GameFrame: Inherets wx.Frame*

This module creates the GUI structure of the game window. It initializes the variables necessary for keeping track of the current list of vocabulary words, how many successful matches the user has made so far, and where in the list our next practice set should be pulled from.
The sizers contaning the buttons for dragging and dropping to are created dynamically, already populated with the necessary buttons, and then destroyed when a new practice set is requested. This includes some logic for determining the new minimum size of the window based on the new sizer and forcing layout updates, so that the user does not experience unintuitive graphical behavior.

*FlexishGridBagSizer: Inherets wx.GridBagSizer*

This could probably use a better name. The purpose of extending GridBagZier was to allow dynamically adding widgets to the sizer. I wanted to keep the number of columns and rows in the grid as close to square as possible (i.e. given 12 items, I want a grid of 4x3, not 6x2). GridBagSizer forces you to know the position at which you want to add the items to the grid. This class allows dynamically determining the max number of rows and columns needed to hold a given total number of items. It also allows adding an object to a random position withn those rows and columns, so that there can be a random order to the vocabulary words displayed.

*MatchPair:*

This class contains all of code that provides drag and drop functionality and the method for determining if a match was made. The logic for this is almost entirely self contained. It only takes a list object from GameFrame in order to add to the count of total matches that have been made per each practice set. When a single vocabulary word is turned into a Match_Pair, both its Donkey button and Tail button are created as a single instance of this class. When a Match_Pair object's Tail is dragged and released, it will check if it was released within the area of the same object's Donkey button. This means there is no need for cross communication among buttons to determine if a Tail was dragged to the wrong Donkey. As far as each Match_Pair object is concerned, it has the only two Donkey and Tail buttons in existence.

Additionally, smooth dragging is achieved by created a new frame with a facsimile of the Tail button. There was previously quite a bit of glitchy behavior with EVT_MOTION being too active and drag_frame not being destroyed properly when mouse movement was too quick or there was an unexpected loss of focus. This is the reason for binding and unbinding some of the events here dynamically. Theorectically, the events should only be bound immediately before they are needed, and should become unbound immediately after they are no longer useful.

**Future Features**

Intend to add functionality to allow user to take an unformatted list of vocabular words and format them such that they can be used with this program.

Also needed is a way to allow the user to dynamically choose how their vocabulary is displayed during the game, how large they want their practice set to be, and a way for them to save their place on exit.

Aditionally, the status frame needs some useful stats added to it, and a timer for users to test how fast their recognition is.
