#!/usr/bin/env python3

import pandas as pd
from matplotlib import pyplot as plt
import copy

calData = pd.read_csv("data/calData.csv")
#CALDATA DATE , BURNTCAL , CONSUMEDCAL
perData = pd.read_csv("data/perData.csv")
#PERDATA DATE , AGE , WEIGHT , HEIGHT
sports = pd.read_csv("data/sports.csv")

def createNewDay(date):

    days = []

    for x in calData["DATE"]:

        days.append(x)
    
    if date not in days:

        lastDay = perData.iloc[-1]
        text = date + "," + str(lastDay["AGE"]) + "," + str(lastDay["WEIGHT"]) + "," + str(lastDay["HEIGHT"]) + "\n"
        a = open("data/perData.csv","a")
        a.write(text)
        a.close()

        text = date + "," + str(calculateDefaultCaloriesBurnt(date)) + "," +"0\n"
        a = open("data/calData.csv","a")
        a.write(text)
        a.close()

def changePersonalAttribute(date,changeName,newValue):

    burnt = 0

    if calData.loc[calData["DATE"]==date, "BURNTCAL"].iloc[0] != calculateDefaultCaloriesBurnt(date):

        print(calData.loc[calData["DATE"]==date,"BURNTCAL"].iloc[0],calculateDefaultCaloriesBurnt(date))
        a = calData.loc[calData["DATE"]==date,"BURNTCAL"].iloc[0] - calculateDefaultCaloriesBurnt(date)
        burnt = copy.copy(a)

    if changeName == "age":
        perData.loc[perData["DATE"]==date,"AGE"] = newValue

    elif changeName == "height":
        perData.loc[perData["DATE"]==date,"HEIGHT"] = newValue

    elif changeName == "weight":
        perData.loc[perData["DATE"]==date,"WEIGHT"] = newValue

    else:
        print("yo there's something wrong w dis")
        

    calData.loc[calData["DATE"]==date, "BURNTCAL"] = burnt + calculateDefaultCaloriesBurnt(date)

    perData.to_csv("data/perData.csv",index=False)
    calData.to_csv("data/calData.csv",index=False)
    


def calculateDefaultCaloriesBurnt(date):

    age = perData.loc[perData["DATE"]==date,"AGE"].iloc[0]
    weight = perData.loc[perData["DATE"]==date,"WEIGHT"].iloc[0]
    height = perData.loc[perData["DATE"]==date,"HEIGHT"].iloc[0]

    cweight = int(weight * 13.4)
    cheight = int(height * 4.8)
    cage = int(age * 5.7)

    defaultCalories = cweight + cheight - cage + 88
    
    return defaultCalories

def calculateBurntCalorieWithBodyMass (date,sport,minutes):

    sportcpm = sports.loc[sports["SPORT"]==sport,"AVGCPM"].iloc[0]
    index = perData.loc[perData["DATE"]==date,"WEIGHT"].iloc[0] / 70

    burntCalories = int(index * sportcpm)
    burntCalories = burntCalories * minutes
    
    return burntCalories

def addOrRemoveToConsumedCalories(date,cal,aor):

    if aor == "add":
        calData.loc[calData["DATE"]==date,"CONSUMEDCAL"] += cal
    
    if aor == "remove":

        calData.loc[calData["DATE"]==date,"CONSUMEDCAL"] -= cal
    
    calData.to_csv("data/calData.csv",index=False)

def addOrRemoveToBurntCalories(date,cal,aor):

    if aor == "add":
        calData.loc[calData["DATE"] == date, "BURNTCAL"] += cal
    elif aor == "remove":
        calData.loc[calData["DATE"] == date, "BURNTCAL"] -= cal

    calData.to_csv("data/calData.csv", index=False)

