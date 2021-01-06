import numpy as np
import pandas as pd
from functools import reduce

"""
Function to create a conditional probability table
Conditional probability is of the form p(x1 | x2, ..., xk)
varnames: vector of variable names (strings) first variable listed 
          will be x_i, remainder will be parents of x_i, p1, ..., pk
probs: vector of probabilities for the flattened probability table
outcomesList: a list containing a vector of outcomes for each variable
factorTable is in the type of pandas dataframe
See the test file for examples of how this function works
"""


def readFactorTable(varnames, probs, outcomesList):
    factorTable = pd.DataFrame({'probs': probs})

    totalfactorTableLength = len(probs)
    numVars = len(varnames)

    k = 1
    for i in range(numVars - 1, -1, -1):
        levs = outcomesList[i]
        numLevs = len(levs)
        col = []
        for j in range(0, numLevs):
            col = col + [levs[j]] * k  # [1, 0] -> [1,1,0,0] -> [1,1,1,1,0,0,0,0]
        factorTable[varnames[i]] = col * int(totalfactorTableLength / (k * numLevs))  # repeat len(probs)/(k*len(levs))
        k = k * numLevs

    return factorTable


"""
Build a factorTable from a data frame using frequencies
from a data frame of data to generate the probabilities.
data: data frame read using pandas read_csv
varnames: specify what variables you want to read from the table
factorTable is in the type of pandas dataframe
"""


def readFactorTablefromData(data, varnames):
    numVars = len(varnames)
    outcomesList = []

    for i in range(0, numVars):
        name = varnames[i]
        outcomesList = outcomesList + [list(set(data[name]))]

    lengths = list(map(lambda x: len(x), outcomesList))
    m = reduce(lambda x, y: x * y, lengths)

    factorTable = pd.DataFrame({'probs': np.zeros(m)})

    k = 1
    for i in range(numVars - 1, -1, -1):
        levs = outcomesList[i]
        numLevs = len(levs)
        col = []
        for j in range(0, numLevs):
            col = col + [levs[j]] * k
        factorTable[varnames[i]] = col * int(m / (k * numLevs))
        k = k * numLevs

    numLevels = len(outcomesList[0])

    # creates the vector called fact to index probabilities 
    # using matrix multiplication with the data frame
    fact = np.zeros(data.shape[1])
    lastfact = 1
    for i in range(len(varnames) - 1, -1, -1):
        fact = np.where(np.isin(list(data), varnames[i]), lastfact, fact)
        lastfact = lastfact * len(outcomesList[i])

    # Compute unnormalized counts of subjects that satisfy all conditions
    a = (data - 1).dot(fact) + 1
    for i in range(0, m):
        factorTable.at[i, 'probs'] = sum(a == (i + 1))

    # normalize the conditional probabilities
    skip = int(m / numLevels)
    for i in range(0, skip):
        normalizeZ = 0
        for j in range(i, m, skip):
            normalizeZ = normalizeZ + factorTable['probs'][j]
        for j in range(i, m, skip):
            if normalizeZ != 0:
                factorTable.at[j, 'probs'] = factorTable['probs'][j] / normalizeZ

    return factorTable


"""
Join of two factors
factor1, factor2: two factor tables

Should return a factor table that is the join of factor 1 and 2.
You can assume that the join of two factors is a valid operation.
Hint: You can look up pd.merge for mergin two factors
"""


def joinFactors(factor1, factor2):
    f1 = factor1.copy()  # copy factor1 to f1 so we won't change factor1
    f2 = factor2.copy()  # copy factor2 to f2 so we won't change factor2
    # add a common column to both f1 and f2
    # 1. if f1 and f2 only share the 'common' column:
    #        each row of f1 will merge with each row of f2
    # 2. if f1 and f2 not only share the 'common' column
    #        f1 and f2 will be merged together depend on their intersection of the columns
    f1['common'] = 1
    f2['common'] = 1
    columns1, columns2 = f1.columns, f2.columns
    # key is the intersection of the columns of f1 and f2 without 'probs'
    key = list(set(columns1) & set(columns2))
    key.remove('probs')
    joinedFactorTable = pd.merge(f1, f2, on=key, how='outer')
    # to mutiply the 'probs_x' and the 'probs_y'
    joinedFactorTable['probs'] = joinedFactorTable['probs_x'] * joinedFactorTable['probs_y']
    # drop the redundant columns 'probs_x', 'probs_y', 'common'
    joinedFactorTable.drop(['probs_x', 'probs_y', 'common'], axis=1, inplace=True)

    return joinedFactorTable


"""
Marginalize a variable from a factor
table: a factor table in dataframe
hiddenVar: a string of the hidden variable name to be marginalized

Should return a factor table that marginalizes margVar out of it.
Assume that hiddenVar is on the left side of the conditional.
Hint: you can look pd.groupby
"""


def marginalizeFactor(factorTable, hiddenVar):
    # columns do not include the hiddenVar and 'probs'
    columns = list(set(factorTable.columns) - set([hiddenVar, 'probs']))
    # we sum the same val of the columns to eliminate hiddenVar
    groups = factorTable.groupby(columns).sum()
    table = pd.DataFrame(groups)
    table.reset_index(inplace=True)
    # drop the hiddenVar
    table.drop(hiddenVar, axis=1, inplace=True)
    return table


"""
Marginalize a list of variables 
bayesnet: a list of factor tables and each table is in dataframe type
hiddenVar: a string of the variable name to be marginalized

Should return a Bayesian network containing a list of factor tables that results
when the list of variables in hiddenVar is marginalized out of bayesnet.
"""


def marginalizeNetworkVariables(bayesNet, hiddenVar):
    # to ensure the iterator work successfully
    # we check whether the input hiddenVar is a string, and turn it into a list
    if isinstance(hiddenVar, str):
        hiddenVar = [hiddenVar]
    # if there's no hiddenVar or there's no table in the bayesNet, we just return bayesNet
    V = len(hiddenVar)
    N = len(bayesNet)
    if V == 0 or N == 0:
        return bayesNet
    # else we need a newNet to store the Network after having marginalized the hidden Variables
    newNet = []
    # in order not to change the original bayesNet, so we copy each table in the bayesNet to the newNet
    for table in bayesNet:
        newNet.append(table.copy())
    # for each variable in the list of hidden variables:
    # we marginalize it by joining every table having that variable and finally eliminate it from the table
    for var in hiddenVar:
        tmpNet = []
        tmpTable = None
        for table in newNet:
            if var in table.columns:
                tmpTable = table if tmpTable is None else joinFactors(table, tmpTable)
            else:
                tmpNet.append(table)
        if tmpTable is not None:
            tmpNet.append(marginalizeFactor(tmpTable, var))
        newNet = tmpNet
    return newNet


"""
Update BayesNet for a set of evidence variables
bayesNet: a list of factor and factor tables in dataframe format
evidenceVars: a vector of variable names in the evidence list
evidenceVals: a vector of values for corresponding variables (in the same order)

Set the values of the evidence variables. Other values for the variables
should be removed from the tables. You do not need to normalize the factors
"""


def evidenceUpdateNet(bayesNet, evidenceVars, evidenceVals):
    # to ensure the iterator work successfully
    # we check whether the input evidenceVars and evidenceVals are strings, and turn them into lists respectively
    if isinstance(evidenceVars, str):
        evidenceVars = [evidenceVars]
    if isinstance(evidenceVals, str):
        evidenceVals = [evidenceVals]

    N = len(bayesNet)
    V = len(evidenceVars)
    newNet = []
    for i in range(N):
        # process each table in the bayesNet
        curColumns = bayesNet[i].columns
        curVars = []
        curVals = []

        # if the columns of the current table has intersection with evidenceVars
        # add the var and val to curVars and curVals
        for j in range(V):
            if evidenceVars[j] in curColumns:
                curVars.append(evidenceVars[j])
                curVals.append(evidenceVals[j])

        # get the rows according to the evidenceVal and drop the rest
        if len(curVars):
            # data type transform
            curVals = np.array(curVals).astype(np.array(bayesNet[i][curVars])[0].dtype).tolist()
            # print([v == curVals for v in bayesNet[i][curVars].values.tolist()])
            newNet.append(bayesNet[i].loc[[v == curVals for v in bayesNet[i][curVars].values.tolist()]])
        else:
            newNet.append(bayesNet[i])
    return newNet

"""
normalizeFactor is used to sum the probabilities of each row and normalize them by the sum
"""
def normalizeFactor(factorTable):
    total = sum(factorTable['probs'])
    factorTable['probs'] = factorTable['probs'] / total
    return factorTable

"""
Run inference on a Bayesian network
bayesNet: a list of factor tables and each table iin dataframe type
hiddenVar: a string of the variable name to be marginalized
evidenceVars: a vector of variable names in the evidence list
evidenceVals: a vector of values for corresponding variables (in the same order)

This function should run variable elimination algorithm by using 
join and marginalization of the sets of variables. 
The order of the elimiation can follow hiddenVar ordering
It should return a single joint probability table. The
variables that are hidden should not appear in the table. The variables
that are evidence variable should appear in the table, but only with the single
evidence value. The variables that are not marginalized or evidence should
appear in the table with all of their possible values. The probabilities
should be normalized to sum to one.
"""

def inference(bayesNet, hiddenVar, evidenceVars, evidenceVals):
    N = len(bayesNet)
    if N == 0:
        return bayesNet
    #  create a newNet to store the result in order not to change the original bayesNet
    newNet = []
    for table in bayesNet:
        newNet.append(table.copy())
    # to eliminate all the hidden Variables
    newNet = marginalizeNetworkVariables(newNet, hiddenVar=hiddenVar)
    # to get the table according to the evidence Variables and evidence Values
    newNet = evidenceUpdateNet(newNet, evidenceVars, evidenceVals)
    # joining all the table in the newNet together
    N = len(newNet)
    if N == 1:
        table = newNet[0]
    else:
        table = newNet[0]
        for i in range(1, N):
            table = joinFactors(table, newNet[i])
    # finally return the normalized table
    return normalizeFactor(table).reset_index(drop=True)
