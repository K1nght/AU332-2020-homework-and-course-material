#!/usr/bin/env python3

from BayesianNetworks import *
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

#############################
## Example Tests from Bishop Pattern recognition textbook on page 377
#############################
BatteryState = readFactorTable(['battery'], [0.9, 0.1], [[1, 0]])
FuelState = readFactorTable(['fuel'], [0.9, 0.1], [[1, 0]])
GaugeBF = readFactorTable(['gauge', 'battery', 'fuel'], [0.8, 0.2, 0.2, 0.1, 0.2, 0.8, 0.8, 0.9], [[1, 0], [1, 0], [1, 0]])

carNet = [BatteryState, FuelState, GaugeBF] # carNet is a list of factors 
## Notice that different order of operations give the same answer
## (rows/columns may be permuted)
t1 = joinFactors(joinFactors(BatteryState, FuelState), GaugeBF)
t2 = joinFactors(joinFactors(GaugeBF, FuelState), BatteryState)
# print(t1)
# print(t2)

t3 = marginalizeFactor(joinFactors(GaugeBF, BatteryState), 'gauge')
t4 = joinFactors(marginalizeFactor(GaugeBF, 'gauge'), BatteryState)
# print(t3)
# print(t4)


t5 = joinFactors(marginalizeFactor(joinFactors(GaugeBF, BatteryState), 'battery'), FuelState)
t6 = marginalizeFactor(joinFactors(joinFactors(GaugeBF, FuelState), BatteryState), 'battery')
# print(t5)
# print(t6)

t7 = marginalizeFactor(joinFactors(marginalizeFactor(joinFactors(GaugeBF, BatteryState), 'battery'), FuelState), 'gauge')
t8 = marginalizeFactor(joinFactors(marginalizeFactor(joinFactors(GaugeBF, BatteryState), 'battery'), FuelState), 'fuel')
# print(t7)
# print(t8)

n1 = evidenceUpdateNet(carNet, 'fuel', '1')
n2 = evidenceUpdateNet(carNet, ['fuel', 'battery'], ['1', '0'])
# print(n1)
# print(n2)

## Marginalize must first combine all factors involving the variable to
## marginalize. Again, this operation may lead to factors that aren't
## probabilities.
n3 = marginalizeNetworkVariables(carNet, 'battery') ## this returns back a list
n4 = marginalizeNetworkVariables(carNet, 'fuel') ## this returns back a list
n5 = marginalizeNetworkVariables(carNet, ['battery', 'fuel'])
# print(n3)
# print(n4)
# print(n5)

# inference
print("inference starts")
print(inference(carNet, ['battery', 'fuel'], [], []) )        ## chapter 8 equation (8.30)
print(inference(carNet, ['battery'], ['fuel'], [0]))           ## chapter 8 equation (8.31)
print(inference(carNet, ['battery'], ['gauge'], [0]))          ##chapter 8 equation  (8.32)
print(inference(carNet, [], ['gauge', 'battery'], [0, 0]))    ## chapter 8 equation (8.33)
print("inference ends")
###########################################################################
#RiskFactor Data Tests
###########################################################################
riskFactorNet = pd.read_csv('RiskFactorsData.csv')

# Create factors

income      = readFactorTablefromData(riskFactorNet, ['income'])
smoke       = readFactorTablefromData(riskFactorNet, ['smoke', 'income'])
exercise    = readFactorTablefromData(riskFactorNet, ['exercise', 'income'])
long_sit    = readFactorTablefromData(riskFactorNet, ['long_sit', 'income'])
stay_up     = readFactorTablefromData(riskFactorNet, ['stay_up', 'income'])
bmi         = readFactorTablefromData(riskFactorNet, ['bmi', 'income'])
diabetes    = readFactorTablefromData(riskFactorNet, ['diabetes', 'bmi'])

## you need to create more factor tables

risk_net = [income, smoke, long_sit, stay_up, exercise, bmi, diabetes]
print("income dataframe is ")
print(income)
factors = riskFactorNet.columns

# example test p(diabetes|smoke=1,exercise=2,long_sit=1)

margVars = list(set(factors) - {'diabetes', 'smoke', 'exercise','long_sit'})
obsVars  = ['smoke', 'exercise','long_sit']
obsVals  = [1, 2, 1]

p = inference(risk_net, margVars, obsVars, obsVals)
print(p)


### Please write your own test scrip similar to  the previous example 
###########################################################################
#HW4 test scrripts start from here
###########################################################################

riskFactorNet = pd.read_csv('RiskFactorsData.csv')

factors = riskFactorNet.columns

income = readFactorTablefromData(riskFactorNet, ['income'])
smoke = readFactorTablefromData(riskFactorNet, ['smoke', 'income'])
exercise = readFactorTablefromData(riskFactorNet, ['exercise', 'income'])
long_sit = readFactorTablefromData(riskFactorNet, ['long_sit', 'income'])
stay_up = readFactorTablefromData(riskFactorNet, ['stay_up', 'income'])
bmi = readFactorTablefromData(riskFactorNet, ['bmi', 'income', 'exercise', 'long_sit'])
bp = readFactorTablefromData(riskFactorNet, ['bp', 'exercise', 'long_sit', 'stay_up', 'smoke', 'income'])
cholesterol = readFactorTablefromData(riskFactorNet, ['cholesterol', 'exercise', 'stay_up', 'income', 'smoke'])
diabetes = readFactorTablefromData(riskFactorNet, ['diabetes', 'bmi'])
stroke = readFactorTablefromData(riskFactorNet, ['stroke', 'bmi', 'bp', 'cholesterol'])
attack = readFactorTablefromData(riskFactorNet, ['attack', 'bmi', 'bp', 'cholesterol'])
angina = readFactorTablefromData(riskFactorNet, ['angina', 'bmi', 'bp', 'cholesterol'])


# 1.--------------------------------------------------------------------------------------------------------------------
my_risk_net = [income, smoke, long_sit, stay_up, exercise, bmi, diabetes, stroke, attack, angina, bp, cholesterol]

my_risk_net_size = 0
for net in my_risk_net:
    my_risk_net_size += len(net)

print(
    "The size of the total risk factor net is {}.\nAnd the factors are {}.\nMy risk factor net is of {} probabilities.".format(
        len(riskFactorNet), list(factors[1:]), my_risk_net_size))
# print(factors)
# print(my_risk_net_size)

# 2.--------------------------------------------------------------------------------------------------------------------
obsVars_2_habits = ['smoke', 'exercise', 'long_sit', 'stay_up']
obsVals_2_badhabits = [1, 2, 1, 1]
# start inferring 

# p(diabetes|smoke=1,exercise=2,long_sit=1,stay_up=1)
margVars_2_badhabits_diabetes = list(set(factors) - {'diabetes', 'smoke', 'exercise', 'long_sit', 'stay_up'})
p_2_diabetes_on_badhabits = inference(my_risk_net, margVars_2_badhabits_diabetes, obsVars_2_habits, obsVals_2_badhabits)
print("The probability of the diabetes with the bad habits\n", p_2_diabetes_on_badhabits)

# p(stroke|smoke=1,exercise=2,long_sit=1,stay_up=1)
margVars_2_badhabits_stroke = list(set(factors) - {'stroke', 'smoke', 'exercise', 'long_sit', 'stay_up'})
p_2_stroke_on_badhabits = inference(my_risk_net, margVars_2_badhabits_stroke, obsVars_2_habits, obsVals_2_badhabits)
print("The probability of the stroke with the bad habits\n", p_2_stroke_on_badhabits)

# p(attack|smoke=1,exercise=2,long_sit=1,stay_up=1)
margVars_2_badhabits_attack = list(set(factors) - {'attack', 'smoke', 'exercise', 'long_sit', 'stay_up'})
p_2_attack_on_badhabits = inference(my_risk_net, margVars_2_badhabits_attack, obsVars_2_habits, obsVals_2_badhabits)
print("The probability of the attack with the bad habits\n", p_2_attack_on_badhabits)

# p(angina|smoke=1,exercise=2,long_sit=1,stay_up=1)
margVars_2_badhabits_angina = list(set(factors) - {'angina', 'smoke', 'exercise', 'long_sit', 'stay_up'})
p_2_angina_on_badhabits = inference(my_risk_net, margVars_2_badhabits_angina, obsVars_2_habits, obsVals_2_badhabits)
print("The probability of the angina with the bad habits\n", p_2_angina_on_badhabits)

obsVals_2_goodhabits = [2, 1, 2, 2]
# p(diabetes|smoke=2,exercise=1,long_sit=2,stay_up=2)
margVars_2_goodhabits_diabetes = list(set(factors) - {'diabetes', 'smoke', 'exercise', 'long_sit', 'stay_up'})
p_2_diabetes_on_goodhabits = inference(my_risk_net, margVars_2_goodhabits_diabetes, obsVars_2_habits,
                                       obsVals_2_goodhabits)
print("The probability of the diabetes with the good habits\n", p_2_diabetes_on_goodhabits)

# p(stroke|smoke=2,exercise=1,long_sit=2,stay_up=2)
margVars_2_goodhabits_stroke = list(set(factors) - {'stroke', 'smoke', 'exercise', 'long_sit', 'stay_up'})
p_2_stroke_on_goodhabits = inference(my_risk_net, margVars_2_goodhabits_stroke, obsVars_2_habits, obsVals_2_goodhabits)
print("The probability of the stroke with the good habits\n", p_2_stroke_on_goodhabits)

# p(attack|smoke=2,exercise=1,long_sit=2,stay_up=2)
margVars_2_goodhabits_attack = list(set(factors) - {'attack', 'smoke', 'exercise', 'long_sit', 'stay_up'})
p_2_attack_on_goodhabits = inference(my_risk_net, margVars_2_goodhabits_attack, obsVars_2_habits, obsVals_2_goodhabits)
print("The probability of the attack with the good habits\n", p_2_attack_on_goodhabits)

# p(angina|smoke=2,exercise=1,long_sit=2,stay_up=2)
margVars_2_goodhabits_angina = list(set(factors) - {'angina', 'smoke', 'exercise', 'long_sit', 'stay_up'})
p_2_angina_on_goodhabits = inference(my_risk_net, margVars_2_goodhabits_angina, obsVars_2_habits, obsVals_2_goodhabits)
print("The probability of the angina with the good habits\n", p_2_angina_on_goodhabits)

obsVars_2_health = ['bp', 'cholesterol', 'bmi']
obsVals_2_badhealth = [1, 1, 3]

# p(diabetes|bp=1,cholesterol=1,bmi=3)
margVars_2_badhealth_diabetes = list(set(factors) - {'diabetes', 'bp', 'cholesterol', 'bmi'})
p_2_diabetes_on_badhealth = inference(my_risk_net, margVars_2_badhealth_diabetes, obsVars_2_health, obsVals_2_badhealth)
print("The probability of the diabetes with the bad health\n", p_2_diabetes_on_badhealth)

# p(stroke|bp=1,cholesterol=1,bmi=3)
margVars_2_badhealth_stroke = list(set(factors) - {'stroke', 'bp', 'cholesterol', 'bmi'})
p_2_stroke_on_badhealth = inference(my_risk_net, margVars_2_badhealth_stroke, obsVars_2_health, obsVals_2_badhealth)
print("The probability of the stroke with the bad health\n", p_2_stroke_on_badhealth)

# p(attack|bp=1,cholesterol=1,bmi=3)
margVars_2_badhealth_attack = list(set(factors) - {'attack', 'bp', 'cholesterol', 'bmi'})
p_2_attack_on_badhealth = inference(my_risk_net, margVars_2_badhealth_attack, obsVars_2_health, obsVals_2_badhealth)
print("The probability of the attack with the bad health\n", p_2_attack_on_badhealth)

# p(angina|bp=1,cholesterol=1,bmi=3)
margVars_2_badhealth_angina = list(set(factors) - {'angina', 'bp', 'cholesterol', 'bmi'})
p_2_angina_on_badhealth = inference(my_risk_net, margVars_2_badhealth_angina, obsVars_2_health, obsVals_2_badhealth)
print("The probability of the angina with the bad health\n", p_2_angina_on_badhealth)

obsVals_2_goodhealth = [3, 2, 2]
# p(diabetes|bp=3,cholesterol=2,bmi=2)
margVars_2_goodhealth_diabetes = list(set(factors) - {'diabetes', 'bp', 'cholesterol', 'bmi'})
p_2_diabetes_on_goodhealth = inference(my_risk_net, margVars_2_goodhealth_diabetes, obsVars_2_health,
                                       obsVals_2_goodhealth)
print("The probability of the diabetes with the good health\n", p_2_diabetes_on_goodhealth)

# p(stroke|bp=3,cholesterol=2,bmi=2)
margVars_2_goodhealth_stroke = list(set(factors) - {'stroke', 'bp', 'cholesterol', 'bmi'})
p_2_stroke_on_goodhealth = inference(my_risk_net, margVars_2_goodhealth_stroke, obsVars_2_health, obsVals_2_goodhealth)
print("The probability of the stroke with the good health\n", p_2_stroke_on_goodhealth)

# p(attack|bp=3,cholesterol=2,bmi=2)
margVars_2_goodhealth_attack = list(set(factors) - {'attack', 'bp', 'cholesterol', 'bmi'})
p_2_attack_on_goodhealth = inference(my_risk_net, margVars_2_goodhealth_attack, obsVars_2_health, obsVals_2_goodhealth)
print("The probability of the attack with the good health\n", p_2_attack_on_goodhealth)

# p(angina|bp=3,cholesterol=2,bmi=2)
margVars_2_goodhealth_angina = list(set(factors) - {'angina', 'bp', 'cholesterol', 'bmi'})
p_2_angina_on_goodhealth = inference(my_risk_net, margVars_2_goodhealth_angina, obsVars_2_health, obsVals_2_goodhealth)
print("The probability of the angina with the good health\n", p_2_angina_on_goodhealth)

# 3.--------------------------------------------------------------------------------------------------------------------
# p(four health outcome|income=1~8)
health_outcome = {'diabetes': [1, 2, 3, 4], 'stroke': [1, 2], 'attack': [1, 2], 'angina': [1, 2]}
health_outcome_discribe = {('diabetes', 1): "having diabetes",
                           ('diabetes', 2): "having diabetes only during pregnancy",
                           ('diabetes', 3): "not having diabetes",
                           ('diabetes', 4): "having pre-diabetic",
                           ('stroke', 1): "having a stroke",
                           ('stroke', 2): "not having a stroke",
                           ('attack', 1): "having a heart attack",
                           ('attack', 2): "not having a heart attack",
                           ('angina', 1): "having angina",
                           ('angina', 2): "not having angina"}

for outcomeVar, outcomeVals in health_outcome.items():
    obsVars_3 = ['income']
    margVars_3 = list(set(factors) - {outcomeVar, 'income'})
    d = {}

    for val in outcomeVals:
        d[val] = []

    # store the result of inference
    for i in range(1, 9):
        # P(y|income=i)
        p_3_on_income = inference(my_risk_net, margVars_3, obsVars_3, [i])
        for key in d.keys():
            d[key].append(p_3_on_income[p_3_on_income[outcomeVar] == key]['probs'].values[0])
        print("The probability of the %s with income[%d]\n" % (outcomeVar, i), p_3_on_income)

    # plot the inference result
    plt.figure(figsize=(18, 5*len(outcomeVals)//2))
    for i, (key, arr) in enumerate(d.items()):
        plt.subplot(len(outcomeVals) // 2, 2, i + 1)
        plt.plot(np.arange(1, len(arr) + 1), arr)
        plt.xlabel('income')
        plt.ylabel('P(%s=%d|income)' % (outcomeVar, key))
        plt.title("The probability of {} with different incomes".format(health_outcome_discribe[(outcomeVar, i + 1)]))
        plt.grid(True)
    # save the figure
    plt.savefig('img/{}_on_income.PNG'.format(outcomeVar))
    # plt.show()

# 4.--------------------------------------------------------------------------------------------------------------------
# add edges from smoking and exercise to each of the four outcomes
diabetes_with_smoke_and_exercise = readFactorTablefromData(riskFactorNet, ['diabetes', 'bmi', 'smoke', 'exercise'])
stroke_with_smoke_and_exercise = readFactorTablefromData(riskFactorNet,
                                                         ['stroke', 'bmi', 'bp', 'cholesterol', 'smoke', 'exercise'])
attack_with_smoke_and_exercise = readFactorTablefromData(riskFactorNet,
                                                         ['attack', 'bmi', 'bp', 'cholesterol', 'smoke', 'exercise'])
angina_with_smoke_and_exercise = readFactorTablefromData(riskFactorNet,
                                                         ['angina', 'bmi', 'bp', 'cholesterol', 'smoke', 'exercise'])

my_risk_net_4 = [income, smoke, long_sit, stay_up, exercise, bmi, bp, cholesterol, diabetes_with_smoke_and_exercise,
                 stroke_with_smoke_and_exercise, attack_with_smoke_and_exercise, angina_with_smoke_and_exercise]
# start inferring
obsVars_4_habits = ['smoke', 'exercise', 'long_sit', 'stay_up']
obsVals_4_badhabits = [1, 2, 1, 1]

# p(diabetes|smoke=1,exercise=2,long_sit=1,stay_up=1)
margVars_4_badhabits_diabetes = list(set(factors) - {'diabetes', 'smoke', 'exercise', 'long_sit', 'stay_up'})
p_4_diabetes_on_badhabits = inference(my_risk_net_4, margVars_4_badhabits_diabetes, obsVars_4_habits,
                                      obsVals_4_badhabits)
print("The probability of the diabetes with the bad habits after adding edges on smoke and exercise\n",
      p_4_diabetes_on_badhabits)

# p(stroke|smoke=1,exercise=2,long_sit=1,stay_up=1)
margVars_4_badhabits_stroke = list(set(factors) - {'stroke', 'smoke', 'exercise', 'long_sit', 'stay_up'})
p_4_stroke_on_badhabits = inference(my_risk_net_4, margVars_4_badhabits_stroke, obsVars_4_habits, obsVals_4_badhabits)
print("The probability of the stroke with the bad habits after adding edges on smoke and exercise\n",
      p_4_stroke_on_badhabits)

# p(attack|smoke=1,exercise=2,long_sit=1,stay_up=1)
margVars_4_badhabits_attack = list(set(factors) - {'attack', 'smoke', 'exercise', 'long_sit', 'stay_up'})
p_4_attack_on_badhabits = inference(my_risk_net_4, margVars_4_badhabits_attack, obsVars_4_habits, obsVals_4_badhabits)
print("The probability of the attack with the bad habits after adding edges on smoke and exercise\n",
      p_4_attack_on_badhabits)

# p(angina|smoke=1,exercise=2,long_sit=1,stay_up=1)
margVars_4_badhabits_angina = list(set(factors) - {'angina', 'smoke', 'exercise', 'long_sit', 'stay_up'})
p_4_angina_on_badhabits = inference(my_risk_net_4, margVars_4_badhabits_angina, obsVars_4_habits, obsVals_4_badhabits)
print("The probability of the angina with the bad habits after adding edges on smoke and exercise\n",
      p_4_angina_on_badhabits)

obsVals_4_goodhabits = [2, 1, 2, 2]
# p(diabetes|smoke=2,exercise=1,long_sit=2,stay_up=2)
margVars_4_goodhabits_diabetes = list(set(factors) - {'diabetes', 'smoke', 'exercise', 'long_sit', 'stay_up'})
p_4_diabetes_on_goodhabits = inference(my_risk_net_4, margVars_4_goodhabits_diabetes, obsVars_4_habits,
                                       obsVals_4_goodhabits)
print("The probability of the diabetes with the good habits after adding edges on smoke and exercise\n",
      p_4_diabetes_on_goodhabits)

# p(stroke|smoke=2,exercise=1,long_sit=2,stay_up=2)
margVars_4_goodhabits_stroke = list(set(factors) - {'stroke', 'smoke', 'exercise', 'long_sit', 'stay_up'})
p_4_stroke_on_goodhabits = inference(my_risk_net_4, margVars_4_goodhabits_stroke, obsVars_4_habits,
                                     obsVals_4_goodhabits)
print("The probability of the stroke with the good habits after adding edges on smoke and exercise\n",
      p_4_stroke_on_goodhabits)

# p(attack|smoke=2,exercise=1,long_sit=2,stay_up=2)
margVars_4_goodhabits_attack = list(set(factors) - {'attack', 'smoke', 'exercise', 'long_sit', 'stay_up'})
p_4_attack_on_goodhabits = inference(my_risk_net_4, margVars_4_goodhabits_attack, obsVars_4_habits,
                                     obsVals_4_goodhabits)
print("The probability of the attack with the good habits after adding edges on smoke and exercise\n",
      p_4_attack_on_goodhabits)

# p(angina|smoke=2,exercise=1,long_sit=2,stay_up=2)
margVars_4_goodhabits_angina = list(set(factors) - {'angina', 'smoke', 'exercise', 'long_sit', 'stay_up'})
p_4_angina_on_goodhabits = inference(my_risk_net_4, margVars_4_goodhabits_angina, obsVars_4_habits,
                                     obsVals_4_goodhabits)
print("The probability of the angina with the good habits after adding edges on smoke and exercise\n",
      p_4_angina_on_goodhabits)

obsVars_4_health = ['bp', 'cholesterol', 'bmi']
obsVals_4_badhealth = [1, 1, 3]

# p(diabetes|bp=1,cholesterol=1,bmi=3)
margVars_4_badhealth_diabetes = list(set(factors) - {'diabetes', 'bp', 'cholesterol', 'bmi'})
p_4_diabetes_on_badhealth = inference(my_risk_net_4, margVars_4_badhealth_diabetes, obsVars_4_health,
                                      obsVals_4_badhealth)
print("The probability of the diabetes with the bad health after adding edges on smoke and exercise\n",
      p_4_diabetes_on_badhealth)

# p(stroke|bp=1,cholesterol=1,bmi=3)
margVars_4_badhealth_stroke = list(set(factors) - {'stroke', 'bp', 'cholesterol', 'bmi'})
p_4_stroke_on_badhealth = inference(my_risk_net_4, margVars_4_badhealth_stroke, obsVars_4_health, obsVals_4_badhealth)
print("The probability of the stroke with the bad health after adding edges on smoke and exercise\n",
      p_4_stroke_on_badhealth)

# p(attack|bp=1,cholesterol=1,bmi=3)
margVars_4_badhealth_attack = list(set(factors) - {'attack', 'bp', 'cholesterol', 'bmi'})
p_4_attack_on_badhealth = inference(my_risk_net_4, margVars_4_badhealth_attack, obsVars_4_health, obsVals_4_badhealth)
print("The probability of the attack with the bad health after adding edges on smoke and exercise\n",
      p_4_attack_on_badhealth)

# p(angina|bp=1,cholesterol=1,bmi=3)
margVars_4_badhealth_angina = list(set(factors) - {'angina', 'bp', 'cholesterol', 'bmi'})
p_4_angina_on_badhealth = inference(my_risk_net_4, margVars_4_badhealth_angina, obsVars_4_health, obsVals_4_badhealth)
print("The probability of the angina with the bad health after adding edges on smoke and exercise\n",
      p_4_angina_on_badhealth)

obsVals_4_goodhealth = [3, 2, 2]
# p(diabetes|bp=3,cholesterol=2,bmi=2)
margVars_4_goodhealth_diabetes = list(set(factors) - {'diabetes', 'bp', 'cholesterol', 'bmi'})
p_4_diabetes_on_goodhealth = inference(my_risk_net_4, margVars_4_goodhealth_diabetes, obsVars_4_health,
                                       obsVals_4_goodhealth)
print("The probability of the diabetes with the good health after adding edges on smoke and exercise\n",
      p_4_diabetes_on_goodhealth)

# p(stroke|bp=3,cholesterol=2,bmi=2)
margVars_4_goodhealth_stroke = list(set(factors) - {'stroke', 'bp', 'cholesterol', 'bmi'})
p_4_stroke_on_goodhealth = inference(my_risk_net_4, margVars_4_goodhealth_stroke, obsVars_4_health,
                                     obsVals_4_goodhealth)
print("The probability of the stroke with the good health after adding edges on smoke and exercise\n",
      p_4_stroke_on_goodhealth)

# p(attack|bp=3,cholesterol=2,bmi=2)
margVars_4_goodhealth_attack = list(set(factors) - {'attack', 'bp', 'cholesterol', 'bmi'})
p_4_attack_on_goodhealth = inference(my_risk_net_4, margVars_4_goodhealth_attack, obsVars_4_health,
                                     obsVals_4_goodhealth)
print("The probability of the attack with the good health after adding edges on smoke and exercise\n",
      p_4_attack_on_goodhealth)

# p(angina|bp=3,cholesterol=2,bmi=2)
margVars_4_goodhealth_angina = list(set(factors) - {'angina', 'bp', 'cholesterol', 'bmi'})
p_4_angina_on_goodhealth = inference(my_risk_net_4, margVars_4_goodhealth_angina, obsVars_4_health,
                                     obsVals_4_goodhealth)
print("The probability of the angina with the good health after after adding edges on smoke and exercise\n",
      p_4_angina_on_goodhealth)

# 5.--------------------------------------------------------------------------------------------------------------------
# add an edge from diabetes to stroke
stroke_with_diabetes = readFactorTablefromData(riskFactorNet,
                                               ['stroke', 'bmi', 'bp', 'cholesterol', 'diabetes', 'smoke', 'exercise'])
my_risk_net_5 = [income, smoke, long_sit, stay_up, exercise, bmi, bp, cholesterol, diabetes_with_smoke_and_exercise,
                 stroke_with_diabetes,
                 attack_with_smoke_and_exercise, angina_with_smoke_and_exercise]

margVars_5_stroke = list(set(factors) - {'stroke', 'diabetes'})
obsVars_5 = ['diabetes']
# p(stroke|diabetes=1)
obsVals_5_1 = [1]
p_5_stroke_on_diabetes1_net1 = inference(my_risk_net_4, margVars_5_stroke, obsVars_5, obsVals_5_1)
p_5_stroke_on_diabetes1_net5 = inference(my_risk_net_5, margVars_5_stroke, obsVars_5, obsVals_5_1)
print("The probability of the stroke with diabetes in the net4\n", p_5_stroke_on_diabetes1_net1)
print("The probability of the stroke with diabetes in the net5\n", p_5_stroke_on_diabetes1_net5)
# p(stroke|diabetes=3)
obsVals_5_3 = [3]
p_5_stroke_on_diabetes3_net1 = inference(my_risk_net_4, margVars_5_stroke, obsVars_5, obsVals_5_3)
p_5_stroke_on_diabetes3_net5 = inference(my_risk_net_5, margVars_5_stroke, obsVars_5, obsVals_5_3)
print("The probability of the stroke without diabetes in the net4\n", p_5_stroke_on_diabetes3_net1)
print("The probability of the stroke without diabetes in the net5\n", p_5_stroke_on_diabetes3_net5)



