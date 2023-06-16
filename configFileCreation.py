# Import libraries
import numpy as np
import pandas as pd

# randomise participant IDs
participantIds = [num for num in range(40)]
np.random.shuffle(participantIds)


# randomise experimental condition
expCondition = ['repInstructions'] * 20 + ['aimInstructions'] * 20
np.random.shuffle(expCondition)

# Create data frame 
experiments = {
"participantId": participantIds, 
"experimentalCondition" : expCondition
}

''' 
convert the dictionary to a dataframe using pandas
use sample() with frac (fraction) set to 1 so all of it is suffled
print to csv file without an index
'''
pd.DataFrame(experiments).to_csv('config.csv')

