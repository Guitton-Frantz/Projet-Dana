#!/usr/bin/env python3
# -*- coding: utf-8 -
import csv
from sys import argv

def ounceToKG(p):
    return p*0.0283495231

def poundToKG(p):
    return p*0.45359237

if __name__=='__main__':
    if len(argv)!=3:
        print(f"""utilisation : {argv[0]} <source> <destination>
        - <source> est le chemin vers le csv contenant les données source
        - <destination> est le chemin vers le csv contenant les données modifiées. Si le fichier existe déjà, cela l'écrase.""")
        exit(1)

    f= open(argv[1])
    fDest = open(argv[2], "w")
    read = csv.reader(f)
    write = csv.writer(fDest, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    stop = False
    for row in read:
        newRow = []
        nColumn = 0
        for c in row:
            nColumn = nColumn + 1
            if("weight" in c):
                stop = True
                newRow.append("weight(kg)")
            else:
                newRow.append(c)
        write.writerow(newRow)
        if(stop == False):
            print("Error")
        break

    rowNumber = 2
    for row in read:
        rowNumber = rowNumber + 1
        nC = 0
        newRow = []
        for c in row:
            nC = nC +1
            if(nC == nColumn):
                newWeight = 0
                c = c.lower()
                #print("inti: " + c)
                s = c.split(" ")
                if(len(s) == 1):
                    print("Error row " + str(rowNumber) + " contain: " + c) #Pour l'instant je les mets à 0 du coup
                elif(s[1] == "pounds" or s[1] == "lbs" or s[1] == "lb." or s[1] == "lb"):
                    kg = poundToKG(float(s[0]))
                elif(s[1] == "ounces" or s[1] == "oz"):
                    kg = ounceToKG(float(s[0]))
                elif(s[1] == "g"):
                    kg = float(s[0])/1000
                elif(s[1] == "kg"):
                    kg = float(kg)
                newWeight = "%.3f" % kg  #arrondie au gramme près
                
                #print("change: " + str(newWeight))
                newRow.append(newWeight)
            else:
                newRow.append(c)
        write.writerow(newRow)


