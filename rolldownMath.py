import numpy as np
import math
import scipy as sp
from scipy.special import binom

#initialize array for roll probabilities (9x5)
rollProbs = np.array([[1,0,0,0,0],[1,0,0,0,0],[0.75,0.25,0,0,0],[0.55,0.3,0.15,0,0],
                     [0.4,0.35,0.2,0.05,0],[0.25,0.35,0.3,0.1,0],[0.19,0.3,0.35,0.15,0.01],
                     [0.14,0.2,0.35,0.25,0.06],[0.1,0.15,0.3,0.3,0.15]], dtype=object)

#initialize array for champ pools (5x3)
champPool = np.array([[13,29,377], [13,22,286], [13,18,234], [10,12,120], [8,10,80]])

#initialize left two columns for bottom array of Sheet1
dynamicRollProbs = np.array([[0,0,0,0,0,0],[1,0,0,0,0,0],[1,1,0,0,0,0],
                            [2,0,0,0,0,0],[2,1,0,0,0,0],[2,2,0,0,0,0],
                            [3,0,0,0,0,0],[3,1,0,0,0,0],[3,2,0,0,0,0],[3,3,0,0,0,0],
                            [4,0,0,0,0,0],[4,1,0,0,0,0],[4,2,0,0,0,0],[4,3,0,0,0,0],[4,4,0,0,0,0],
                            [5,0,0,0,0,0],[5,1,0,0,0,0],[5,2,0,0,0,0],[5,3,0,0,0,0],[5,4,0,0,0,0],[5,5,0,0,0,0]], dtype=object)

def main():
    #main inputs
    level = int(input("Level: "))
    unitCost = int(input("Unit Cost: "))
    unitsSameCostGone = int(input("Units Same Cost Gone: "))
    unitsGone = int(input("Units Gone: "))
    gold = int(input("Gold: "))

    #secondary inputs
    levelProb = 0.0
    totalUnits = 0
    unitsInPool = 0
    wantedUnitsInPool = 0

    #outputs
    oneUnitProbPerRoll = 0.0
    expectedUnitsPerRoll = 0.0

    oneUnitProbTotalGold = 0.0
    expectedUnitsTotalGold = 0.0

    #Update secondary inputs based on user inputs
    #Level prob = probability to roll unit based on level (in one slot)
    levelProb = rollProbs[level-1][unitCost-1]
    #Total # of x-cost units
    totalUnits = champPool[unitCost-1][2]
    #Number of x-cost units in pool
    unitsInPool = totalUnits-unitsSameCostGone
    #number of specific units in pool
    wantedUnitsInPool = champPool[unitCost-1][1] - unitsGone

    #fill in right 4 columns of array
    count = 0
    for x in dynamicRollProbs:
        #Prob of rolling specific cost units
        p = binom(5,x[0])
        q = levelProb ** x[0]
        r = (1-levelProb)
        t = (5-x[0])
        dynamicRollProbs[count,2] = p * q * r ** t
        #Cond. prob of rolling specific units
        a = binom(wantedUnitsInPool,x[1])
        b1 = (unitsInPool-wantedUnitsInPool)
        b2 = (x[0]-x[1])
        b = binom((b1),(b2))
        c = binom(unitsInPool, x[0])
        d = a*b/c
        dynamicRollProbs[count,3] = d
        #Joint prob
        dynamicRollProbs[count,4] = dynamicRollProbs[count][2] * dynamicRollProbs[count][3]
        dynamicRollProbs[count,5] = dynamicRollProbs[count][1] * dynamicRollProbs[count][4]
        count = count + 1

    #update roll chances
    y=0
    z=0
    for x in dynamicRollProbs:
        z = z + x[5]
        if x[1] > 0:
            y = y + x[4]
    #Prob of rolling at least one specific unit per roll
    oneUnitProbPerRoll = y
    #expected number of specific units per roll
    expectedUnitsPerRoll = z
    #Prob of rolling at least one specific unit in X gold
    oneUnitProbTotalGold = 1-(1-oneUnitProbPerRoll)**(gold/2)
    #Expected number of specific units rolled in X gold
    expectedUnitsTotalGold = expectedUnitsPerRoll*gold/2
        
    #Print out info function
    print("level: " + str(level) + ", unitCost: " + str(unitCost) + ", unitsSameCostGone: " + str(unitsSameCostGone)
          + ", unitsGone: " + str(unitsGone) + ", gold: " + str(gold))
    print("levelProb: " + str(levelProb) + ", totalUnits: " + str(totalUnits) + ", unitsInPool: " + str(unitsInPool)
          + ", wantedUnitsInPool: " + str(wantedUnitsInPool))
    print("oneUnitProbPerRoll: " + str(oneUnitProbPerRoll) + ", expectedUnitsPerRoll: " + str(expectedUnitsPerRoll)
          + ", oneUnitProbTotalGold: " + str(oneUnitProbTotalGold) + ", expectedUnitsTotalGold: " + str(expectedUnitsTotalGold))
    print("dynamicRollProbs:")
    print(dynamicRollProbs)

def calculate(level, unitCost, unitsSameCostGone, unitsGone, gold):
    #Update secondary inputs based on user inputs
    #Level prob = probability to roll unit based on level (in one slot)
    levelProb = rollProbs[level-1][unitCost-1]
    #Total # of x-cost units
    totalUnits = champPool[unitCost-1][2]
    #Number of x-cost units in pool
    unitsInPool = totalUnits-unitsSameCostGone
    #number of specific units in pool
    wantedUnitsInPool = champPool[unitCost-1][1] - unitsGone

    #fill in right 4 columns of array
    count = 0
    for x in dynamicRollProbs:
        #Prob of rolling specific cost units
        p = binom(5,x[0])
        q = levelProb ** x[0]
        r = (1-levelProb)
        t = (5-x[0])
        dynamicRollProbs[count,2] = p * q * r ** t
        #Cond. prob of rolling specific units
        a = binom(wantedUnitsInPool,x[1])
        b = binom((unitsInPool-wantedUnitsInPool),(x[0]-x[1]))
        c = binom(unitsInPool, x[0])
        d = a*b/c
        dynamicRollProbs[count,3] = d
        #Joint prob
        dynamicRollProbs[count,4] = dynamicRollProbs[count][2] * dynamicRollProbs[count][3]
        #X * P(X=x)
        dynamicRollProbs[count,5] = dynamicRollProbs[count][1] * dynamicRollProbs[count][4]
        count = count + 1
        
    y=0
    z=0
    for x in dynamicRollProbs:
        z = z + x[5]
        if x[1] > 0:
            y = y + x[4]
    #Prob of rolling at least one specific unit per roll
    oneUnitProbPerRoll = y
    #expected number of specific units per roll
    expectedUnitsPerRoll = z
    #Prob of rolling at least one specific unit in X gold
    oneUnitProbTotalGold = 1-(1-oneUnitProbPerRoll)**(gold//2)
    #Expected number of specific units rolled in X gold
    expectedUnitsTotalGold = expectedUnitsPerRoll*(gold//2)
    return oneUnitProbPerRoll, expectedUnitsPerRoll, oneUnitProbTotalGold, expectedUnitsTotalGold

if __name__ == '__main__':
    main()
