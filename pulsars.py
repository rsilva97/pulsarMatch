#hh:mm:ss RA
#dd:mm:ss DEC
#binary search sorted lists
#Vela pulsar B0833-45 coincident with the beam S20404_1
#S57302_8 15:14:17.9 -66:57:00
#beam last line: S61305_1.hdr 06:38:26.0 +04:52:45.0

import os
import math

def simpleMatch(ra, dec, names, output):
    decFile = open(dec, 'r')
    raFile = open(ra, 'r')
    namesFile = open(names, 'r')
    outFile = open(output, 'w')

    decList = decFile.readlines()
    raList = raFile.readlines()
    namesList = namesFile.readlines()

    for i in range(0, len(namesList)):
        outFile.write(namesList[i].strip() + " " +
                      raList[i].strip() + " " +
                      decList[i])

    decFile.close()
    raFile.close()
    namesFile.close()
    outFile.close()

def matchCoordinates(declinations, rightAscensions, output):

    #opening files
    decFile = open(declinations, 'r')
    raFile = open(rightAscensions, 'r')
    outputFile = open(output, 'w')

    #two lists with the lines from input files
    listOfDec = decFile.readlines()
    listOfRa = raFile.readlines()

    outputLines = []

    for i in range(0, len(listOfDec)):
        decValues = listOfDec[i].split(":")
        decValues[len(decValues)-1] = decValues[len(decValues)-1].strip() #remove '\n'

        decToDegrees = 0

        if (len(decValues) == 3):
            decToDegrees = float(decValues[2])/3600 + float(decValues[1])/60 + abs(float(decValues[0]))
        elif (len(decValues) == 2):
            decToDegrees = float(decValues[1])/60 + abs(float(decValues[0]))
        else:
            decToDegrees = abs(float(decValues[0]))

        if decValues[0][0] == '-':
            decToDegrees = decToDegrees * -1

        raValues = listOfRa[i].split(":")
        raValues[len(raValues)-1] = raValues[len(raValues)-1].strip()
        
        raToDegrees = 0
        
        if(len(raValues) == 3):   
            raToDegrees = (float(raValues[2])/3600 + float(raValues[1])/60 + float(raValues[0]))*15
        elif (len(raValues) == 2):
            raToDegrees = (float(raValues[1])/60 + float(raValues[0]))*15
        else:
            raToDegrees = float(raValues[0])*15

        newEntry = []
        newEntry.append(decToDegrees)
        newEntry.append(raToDegrees)
        outputLines.append(newEntry)

    for line in outputLines:
        outputFile.write(str(line[0]) + " " + str(line[1]) + "\n")

    decFile.close()
    raFile.close()
    outputFile.close()


def findResults(known, beams, pulsarNames, beamNames, output, beamsDec, beamsRa, pulsarsDec, pulsarsRa):

    knownFile = open(known, 'r')
    beamsFile = open(beams, 'r')
    pulsarNamesFile = open(pulsarNames, 'r')
    beamNamesFile = open(beamNames, 'r')
    beamsDecFile = open(beamsDec, 'r')
    beamsRaFile = open(beamsRa, 'r')
    pulsarsDecFile = open(pulsarsDec, 'r')
    pulsarsRaFile = open(pulsarsRa, 'r')
    outFile = open(output, 'w')

    listOfPulsarNames = pulsarNamesFile.readlines()
    listOfBeamNames = beamNamesFile.readlines()
    listOfKnownCoords = knownFile.readlines()
    listOfBeamsCoords = beamsFile.readlines()
    listOfBeamDec = beamsDecFile.readlines()
    listOfBeamRa = beamsRaFile.readlines()
    listOfPulsarsDec = pulsarsDecFile.readlines()
    listOfPulsarsRa = pulsarsRaFile.readlines()

    for j in range(0, len(listOfKnownCoords)):
        knownValues = listOfKnownCoords[j].split(" ")
        knownValues[len(knownValues)-1] = knownValues[len(knownValues)-1].strip()

        for k in range(0, len(listOfBeamsCoords)):
            beamValues = listOfBeamsCoords[k].split(" ")
            beamValues[len(beamValues)-1] = beamValues[len(beamValues)-1].strip()

            result = math.sqrt((float(beamValues[0])-float(knownValues[0]))**2+(float(beamValues[1])-float(knownValues[1]))**2)

            if (result < 0.375757):
                pulsarName = listOfPulsarNames[j].strip()
                pulsarDec = listOfPulsarsDec[j].strip()
                pulsarRa = listOfPulsarsRa[j].strip()
                beamName = listOfBeamNames[k].strip()
                beamDec = listOfBeamDec[k].strip()
                beamRa = listOfBeamRa[k].strip()
                outFile.write(beamName + " " + beamRa + " " + beamDec + " " + pulsarName + " " + pulsarRa + " " + pulsarDec + " " + str(result*60) + "\n")

    pulsarNamesFile.close()
    beamNamesFile.close()
    knownFile.close()
    beamsFile.close()
    beamsDecFile.close()
    beamsRaFile.close()
    pulsarsDecFile.close()
    pulsarsRaFile.close()
    outFile.close()

    #beamname beamRAJ beamDECJ psrname psrRAJ psrDECJ distance(in arcmin)

def condenseResults(results, condensed):
    resFile = open(results, 'r')
    outFile = open(condensed, 'w')

    listOfEntries = resFile.readlines()
    entries = {}
    
    for item in listOfEntries:
        if(item not in entries):
            entries[item] = 1
        else:
            entries[item] = entries[item] + 1

    for item in entries:
        outFile.write(str(entries.get(item)) + " " + item)

    resFile.close()
    outFile.close()
            
def main():

    #simpleMatch("atnf_ra.txt", "atnf_dec.txt", "atnf_name.txt", "simply_matched_pulsars.txt")
    #simpleMatch("master_ra.txt", "master_dec.txt", "master_name.txt", "simply_matched_beams.txt")
    matchCoordinates("atnf_dec.txt", "atnf_ra.txt", "matchedKnown.txt")
    matchCoordinates("master_dec.txt", "master_ra.txt", "matchedBeams.txt")
    findResults("matchedKnown.txt", "matchedBeams.txt", "atnf_name.txt", "master_name.txt", "finalResult.txt", "master_dec.txt", "master_ra.txt", "atnf_dec.txt", "atnf_ra.txt")
    condenseResults("finalResult.txt", "condensedResult.txt")

main()
