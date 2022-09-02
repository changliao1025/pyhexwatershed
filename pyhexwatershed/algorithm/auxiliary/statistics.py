import numpy as np
def remap( x, oMin, oMax, nMin, nMax ):

    #range check
    if oMin == oMax:
        print ("Warning: Zero input range")
        return None
    if nMin == nMax:
        print ("Warning: Zero output range")
        return None
    #check reversed input range
    reverseInput = False
    oldMin = np.min( np.array([oMin, oMax]) )
    oldMax = np.max( np.array([oMin, oMax]) )
    if not oldMin == oMin:
        reverseInput = True
    #check reversed output range
    reverseOutput = False   
    newMin = np.min( np.array([nMin, nMax]) )
    newMax = np.max( np.array([nMin, nMax]) )
    if not newMin == nMin :
        reverseOutput = True
    portion = (x-oldMin)*(newMax-newMin)/(oldMax-oldMin)
    if reverseInput:
        portion = (oldMax-x)*(newMax-newMin)/(oldMax-oldMin)
    result = portion + newMin
    if reverseOutput:
        result = newMax - portion
    return result