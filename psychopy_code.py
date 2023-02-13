from __future__ import division
from psychopy import visual, core, data, event, sound
from psychopy.constants import *
from psychopy import parallel
from psychopy.tools import coordinatetools
import datetime
import os
import sys
import serial
import time
import struct
import numpy as np
import pandas as pd

# allocate window and graphics
win = visual.Window(
    size=(500, 500),
    pos=(100, 100),
    fullscr=False,
    screen=0,
    allowGUI=False,
    allowStencil=False,
    monitor='testMonitor',
    color='gray',
    colorSpace='rgb',
    blendMode='avg',
    useFBO=False,
    units='cm')

# circle stimulus
circle_stim = visual.Circle(win, radius=1, fillColor='white')
rt_stim = visual.Circle(win, radius=2, fillColor='red')
lf_stim = visual.Circle(win, radius=2, fillColor='blue')
fixation_cross = visual.ShapeStim(win,
lineColor='white',
lineWidth=2,
vertices=((-0.5, 0), (0.5, 0), (0, 0), (0, 0.5), (0, -0.5)),
closeShape=False,
pos=(0, 0))
mouse = event.Mouse(visible=False, win=win)

state = 'stim_presentation'

timer = core.Clock()

while True:

    resp = event.getKeys()
    mouse_position = mouse.getPos()

    if state == 'stim_presentation':
        circle_stim.pos = mouse_position
        circle_stim.draw()
        if 'right' in resp:
            state = 'response_feedback'
            timer.reset()
        if 'left' in resp: 
            state = 'response_feedback_lft'
            timer.reset()
    
    if state == 'response_feedback':
        rt_stim.draw()
        rt_stim.pos = mouse_position
        if timer.getTime() > 3:
           state = 'iti'
    
    elif state == 'response_feedback_lft': 
        lf_stim.draw()
        lf_stim.pos = mouse_position
        if timer.getTime() > 3: 
            state = 'iti'
    
    if state == 'iti':
        fixation_cross.draw()
        if timer.getTime() > 5: 
            state = 'stim_presentation'
            timer.reset()

    if 'escape' in resp:
        win.close()
        core.quit()

    win.flip()
    
    

