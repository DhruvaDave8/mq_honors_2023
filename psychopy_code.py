#Import relevant libraries 
import numpy as np
from psychopy import visual, event, core
from psychopy.tools import coordinatetools, mathtools
import time

'''Create stimuli'''
#Window
win = visual.Window(size=(1000, 1000),
                    pos=(0, 0),
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
    
    
#Screens 
welcomeMsg = visual.TextStim(win, text =  "Welcome!\n \n If you consent to participate please press the space bar to begin experiment.")
baseInstruct1 = visual.TextStim(win, text = "Use the green ring to guide you to the start position for each trial.\n The ring shows how far you are from the target.") 
baseInstruct2 = visual. TextStim(win, text = "Please move to quickly and accurately slice through the target once start position turns green.")
adaptationInstructions = visual.TextStim(win, text = "Feedback on the following trials is not truthful. \n Please ignore feedback and aim to slice through the target as before.")  
endMsg = visual.TextStim(win, text = "Thank you for participating!") 


# Stimuli 
guideRing = visual.Circle(win, lineColor='green', fillColor='none')
cursor = visual.Circle(win, radius=0.25, fillColor='white')
startPos = visual.Circle(win, radius=0.25, fillColor='red')
goPos = visual.Circle(win, radius=0.25, fillColor='green')
currentPos = startPos
target = visual.Circle(win, radius=0.25, fillColor='green')
lowFb = visual.Circle(win, radius=0.25, fillColor='white')
modFb = visual.Circle(win, radius=0.25, opacity=0.5, fillColor='white')

'''Sensory Uncertainty tiny circle parameters'''
cloudCirc = visual.Circle(win, radius=0.05, fillColor='white')
nCirc = 50 
circSize = 0.05

# Blocks 
totalRun = 300
baseTrials = 20
adaptTirals = 200
washoutTrials = 'totalRun'
currentTrial = 0

# States
    #Initial state
state = 'welcomeScreen'
    # Pause for response
pause = 1

# Timer
stateClock = core.Clock()

while currentTrial < totalRun: 

    # Response and data collection
    resp = event.getKeys(keyList=['escape','space'])
    mouse = event.Mouse(visible=False, win=win)
    cursor.pos = mouse.getPos()
    #defining theta and r
    theta, r = coordinatetools.cart2pol(cursor.pos[0], cursor.pos[1])
    #data collection
    data = {'trial':[], 'endpoint_theta':[]}

    #Welcome screen 
    if state == 'welcomeScreen':
        welcomeMsg.draw()
    if 'space' in resp: 
        state = 'instructions'
        stateClock.reset()
        
    # Instruction screens
    if state == 'instructions':
        baseInstruct1.draw()
        if stateClock.getTime() >= pause:
            state = 'instructions2'
            stateClock.reset()

    if state == 'instructions2':
        baseInstruct2.draw()
        if stateClock.getTime() >= pause:
            state = 'baseline'
            stateClock.reset()
        

#Baseline block 
    if state == 'baseline':
        guideRing.radius = r
        guideRing.draw()
        if mathtools.distance(currentPos.pos, cursor.pos) < 1:
            state = 'hold' 
            currentPos.draw()
        while mathtools.distance(currentPos.pos, cursor.pos) < 0.25:
            currentPos = goPos
            target.draw()
            stateClock.reset()

#Exit/End
    if state == 'endExp':
        endMsg.draw()
    if 'escape' in resp: 
        win.Close()
        core.quit()
            
    
    win.flip()
