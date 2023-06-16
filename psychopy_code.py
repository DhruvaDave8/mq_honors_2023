#Import relevant libraries 
import numpy as np
import pandas as pd
from psychopy import visual, event, core
from psychopy.tools import coordinatetools, mathtools
from psychopy.constants import * 
import time

# Set seed for np.random
np.random.seed(1)

# Participant order
participant = 0

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

''' Set up text rendering on window '''
textStim = visual.TextStim(win)
    
#Screens 
welcomeMsg = visual.TextStim(win, text =  "Welcome!\n \n If you consent to participate please press the space bar to begin experiment.")
endMsg = visual.TextStim(win, text = "Thank you for participating!") 

# Instructions
''' Replication instructions '''

repInstructions = [
"Use the arrow keys to navigate through instructions", 
"You will complete a series of reaches to a variety of targets. \n\n Use the green ring on screen to guide your hand to the start position.", 
"The further away your hand, the larger the ring will be.", 
"After placing your cursor in the start target for 200ms, a target will appear in the distance and turn green.", 
"As soon as the target appears, make a rapid, accurate reach through the center of the target to slice through the target.", 
"Sometimes you will see the cursor, sometimes you wont. \n \n Use whatever visual feedback is available to slice as accurately through the target as possible."
]
    
''' Direct aiming instructions ''' 

aimInstructions = [ 
"Use the arrow keys to navigate through instructions", 
"You will complete a series of reaches to a variety of targets. \n\n  Use the green ring on screen to guide your hand to the start position.",
"The further away your hand, that larger the ring will be.", 
"After placing your cursor in the start target for 200ms, a target will appear in the distance and turn green.", 
"As soon as the target appears, make a rapid, accurate reach through the center of the target to slice through the target.", 
"Sometimes you will see the cursor, sometimes you wont. \n \n Ignore the cursor and move your hand as accurately through the target as possible."
]

# Functions

''' Instruction screens. Takes variable list of instruction as parameter.'''
def expInstructions(instructions):
    currentInstructionIndex = 0
    totalInstructions = len(instructions)
    while True:
        ''' Clear window '''
        win.flip()
        ''' Set the current instruction '''
        instruction = instructions[currentInstructionIndex]
        textStim.setText(instruction)
        ''' Draw the text stimulus on the window '''
        textStim.draw()
        win.flip()
        ''' Wait for a key press '''
        keys = event.waitKeys(keyList=['left', 'right', 'escape'])
        ''' Check if the left arrow key was pressed to navigate to the previous instruction '''
        if 'left' in keys:
            currentInstructionIndex -= 1
            if currentInstructionIndex < 0:
                currentInstructionIndex = 0
        ''' Check if the right arrow key was pressed to navigate to the next instruction '''
        if 'right' in keys:
            currentInstructionIndex += 1
            if currentInstructionIndex >= totalInstructions:
                return
        ''' Check if the escape key was pressed to exit the program'''
        if 'escape' in keys:
            win.close()
            core.quit()
            
            
        # Clear window
        win.flip()

# Stimuli 
guideRing = visual.Circle(win, lineColor='green', fillColor='none')
cursor = visual.Circle(win, radius=0.25, fillColor='white')
startPos = visual.Circle(win, radius=0.25, fillColor='red')
goPos = visual.Circle(win, radius=0.25, fillColor='green')
currentPos = startPos
target = visual.Circle(win, radius=0.25, fillColor='green')
targetDistance = 10 
targetAngle = 15
target.pos = (targetDistance, targetAngle)
hand = visual.Circle(win, radius=0.25, fillColor='white')
midPos = 5
hand.pos = (0, midPos)
lowFb = visual.Circle(win, radius=0.25, fillColor='white')
modFb = visual.Circle(win, radius=0.25, opacity=0.5, fillColor='white')



'''Sensory Uncertainty tiny circle parameters'''
cloudCirc = visual.Circle(win, radius=0.05, fillColor='white')
nCirc = 50 
circSize = 0.05
zero = 0
low = 0
moderate = 0 
high = 0

# Create configuration files

# Read in participant condition assignment csv
config = pd.read_csv('config.csv')

# Create experimental Conditions dataframe
experimentDf = pd.DataFrame({
"trial" : [trial for trial in range(300)],
"block" : ['baseline']*20 + ['rotation'] * 180 + ['washout'] * 100,
"rotation" : [0] * 20 + list(np.random.normal(loc=12, scale=4, size=180)) + [0] * 100,
"sensoryUncertainty" : [zero] * 20 + ([zero] * 45 + [low] * 45 + [moderate] * 45 + ['high'] * 45) + [zero] * 100
})


# Temporary data storage 
trialData = {'endpointHandAngel' : []}


# Blocks 
baseTrials = 20
adaptTirals = 180
washoutTrials = 100
totalRun = 300
currentTrial = 0

# States
    #Initial state
state = 'welcomeScreen'
    # Pause for response
pause = 1

# Timer and times
stateClock = core.Clock()
trialDuration = 1
midpointTime = 0.1

# Experiment Run
while currentTrial < totalRun: 
    # Get experimental condition
    instructionSet = config.iloc[participant].experimentalCondition
    
    # Get current Trial 
    condition = experimentDf.iloc[currentTrial]
    ''' to get the block value at the current row: 
        block = condition.block
    '''
    # Response and data collection
    resp = event.getKeys(keyList=['escape','space'])
    mouse = event.Mouse(visible=False, win=win)
    cursor.pos = mouse.getPos()
    
    #defining theta and r
    theta, r = coordinatetools.cart2pol(cursor.pos[0], cursor.pos[1])
    
    
    #Welcome screen 
    if state == 'welcomeScreen':
        welcomeMsg.draw()
        if 'space' in resp: 
            state = 'instructions'
            stateClock.reset()
        
    # Instruction screens
    if state == 'instructions':
        if instructionSet == 'repInstructions': 
            expInstructions(repInstructions)
        elif instructionSet == 'aimInstructions': 
            expInstructions(aimInstructions)
        state = 'search'
        
    # Find start position using guide ring 
    if state == 'search': 
        guideRing.radius = r
        guideRing.draw()
        if mathtools.distance(currentPos.pos, cursor.pos) < 1:
            state = 'hold' 
        
    # Wait for participant to properly get on the start position
    if state == 'hold': 
        currentPos.draw()
        cursor.draw()
        if mathtools.distance(currentPos.pos, cursor.pos) < 0.25:
            stateClock.reset()
            state = 'reach'
    
    if state == 'reach': 
        currentPos = goPos
        currentPos.draw()
        cursor.draw()
        target.draw()
        if stateClock.getTime() >= trialDuration: 
             state = 'search' 
        if mathtools.distance(currentPos.pos, cursor.pos) > 0.25:
                state = 'wait' 
                currentPos = startPos
            
    if state == 'wait':
        target.draw()
        if r >= midPos: 
            state = 'midpoint' 
        if stateClock.getTime() >= trialDuration: 
            state = 'iti'
            
    if state == 'midpoint':
        modFb.pos = cursor.pos
        modFb.draw() #place holder for whatever uncertainty condition is assigned to the trial
        target.draw()
        if r >= targetDistance:
            state = 'iti'
            stateClock.reset
            
    if state == 'iti':
        #Add data to data frame
        if r == targetDistance:
            trialData['endpointHandAngel'].append(theta[targetDistance])
        # Move data in data frame to csv file
        pd.DataFrame([trialData]).to_csv('{}Data.csv'.format(participant))
        # Add to number of trials complete and set state to search
        currentTrial += 1
        if stateClock.getTime() >= 0.5:  
            state == 'search'
        
    if 'escape' in resp: 
        pd.DataFrame(trialData).to_csv(('{}Data.csv').format(participant))
        win.close()
        core.quit()
            
    win.flip()
