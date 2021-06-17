import json
import os
import numpy as np
import support as sp
import sys
import matplotlib.pyplot as plt

def getNames():
	filename = 'legislators-current.json'
	conData = []
	with open(filename) as json_file:
		js = json.load(json_file)
		for i in js:
			bio = i['id']['bioguide']
			name = i['name']['official_full']
			tlen = len(i['terms'])
			party = i['terms'][tlen-1]['party']
			tpe = i['terms'][tlen-1]['type']
			state = i['terms'][tlen-1]['state']

			temp = (bio, name, party, tpe, state)
			conData.append(temp)

	return conData

def divideHouses(data):
	House = []
	Senate = []
	for i in data:
		if i[3] == 'sen':
			Senate.append(i)
		if i[3] == 'rep':
			House.append(i)

	return House, Senate

def divideParties(data):
	Rep = []
	Dem = []
	for i in data:
		if i[2] == 'Republican':
			Rep.append(i)
		if i[2] == 'Democrat':
			Dem.append(i)

	return Rep, Dem

def Compute(A, B, house):
	countMat = []
	for i in range(0, len(A)):
		temp = []
		for j in range(0, len(B)):
			temp.append(0.0)
		countMat.append(temp)
	path = ''
	if house == 'senate':
		path = 'Source/s/'
	if house == 'house':
		path = 'Source/hr/'
	dirs = os.listdir(path)
	for i in dirs:
		filename = path  + '/' + i + '/data.json'
		with open(filename) as json_file:
			js = json.load(json_file)
			indexA = []
			indexB = []
			for j in js['cosponsors']:
				for k in range(0, len(A)):
					if j['bioguide_id'] == A[k][0]:
						indexA.append(k)

				for k in range(0, len(B)):
					if j['bioguide_id'] == B[k][0]:
						indexB.append(k)

			for j in indexA:
				for k in indexB:
					countMat[j][k] += 1

	countMat = np.array(countMat)

	return countMat

def bestFit(A, row, col):
	newA = []
	for i in range(0, len(row)):
		temp = []
		for j in range(0, len(col)):
			num = A[i][j] / (1 + (col[j] - row[i])**2) 
			temp.append(num)

		newA.append(temp)

	newA = np.array(newA)

	return newA

def mostComp(A):
	x = 0
	y = 0
	max_num = 0
	for i in range(0, len(A)):
		for j in range(0, len(A.transpose())):
			if A[i][j] > max_num:
				max_num = A[i][j]
				x = i
				y = j

	return x, y






conData = getNames()

House, Senate = divideHouses(conData)

RepublicanS, DemocratS = divideParties(Senate)

Dem2Repub = Compute(DemocratS, RepublicanS, "senate")
Repub2Dem = Compute(RepublicanS, DemocratS, "senate")

D2Rprob = sp.makeProb(Dem2Repub)
R2Dprob = sp.makeProb(Repub2Dem)

pairMat = sp.makePairMat(D2Rprob, R2Dprob)

compMat = sp.makeCompMat(pairMat)

rowScores, colScores = sp.totalScore(compMat)

fitMat = bestFit(compMat, rowScores, colScores)

RepublicanH, DemocratH = divideParties(House)

Dem2RepubH = Compute(DemocratH, RepublicanH, "house")
Repub2DemH = Compute(RepublicanH, DemocratH, "house")

D2RprobH = sp.makeProb(Dem2RepubH)
R2DprobH = sp.makeProb(Repub2DemH)

pairMatH = sp.makePairMat(D2RprobH, R2DprobH)

compMatH = sp.makeCompMat(pairMatH)

rowScoresH, colScoresH = sp.totalScore(compMatH)

fitMatH = bestFit(compMatH, rowScoresH, colScoresH)


#converting to json
print('Convetring to Json')
DemList = []
for i in range(0, len(rowScores)):
	tag = (DemocratS[i], rowScores[i])
	DemList.append(tag)

RepList = []
for i in range(0, len(colScores)):
	tag = (RepublicanS[i], colScores[i])
	RepList.append(tag)

outputCompMat = []
for i in range(0, len(rowScores)):
	for j in range(0, len(colScores)):
		tag = (DemocratS[i][1], RepublicanS[j][1], fitMat[i][j])
		outputCompMat.append(tag)

'''DemSenate = open('DemSenate.json', 'w')
json.dump(DemList, DemSenate)

RepSenate = open('RepSenate.json', 'w')
json.dump(RepList, RepSenate)

fitM = open('FitListS.json', 'w')
json.dump(outputCompMat, fitM)'''

DemHList = []
for i in range(0, len(rowScoresH)):
	tag = (DemocratH[i], rowScoresH[i])
	DemHList.append(tag)

RepHList = []
for i in range(0, len(colScoresH)):
	tag = (RepublicanH[i], colScoresH[i])
	RepHList.append(tag)

outputCompMatH = []
for i in range(0, len(rowScoresH)):
	for j in range(0, len(colScoresH)):
		tag = (DemocratH[i][1], RepublicanH[j][1], fitMatH[i][j])
		outputCompMatH.append(tag)

'''DemHouse = open('DemHouse.json', 'w')
json.dump(DemHList, DemHouse)

RepHouse = open('RepHouse.json', 'w')
json.dump(RepHList, RepHouse)

fitMH = open('FitListH.json', 'w')
json.dump(outputCompMatH, fitMH)'''

print('Finished Converting to Json')




print('Democrat scores')
for i, j in zip(DemocratS, rowScores):
	print(i[1] + '\t' + i[4] + '\t' + str(j))

print('------------------------------------')
print('Republican scores')
for i, j in zip(RepublicanS, colScores):
	print(i[1] + '\t' + i[4] + '\t' + str(j))

print('Mean Dem score: ' + str(np.mean(rowScores)))
print('Mean Rep score: ' + str(np.mean(colScores)))
dcount = []
dinv = []
for i in range(0, len(rowScores)):
	dinv.append(rowScores[i])
	dcount.append(i)

rcount = []
rinv = []
for i in range(0, len(colScores)):
	rinv.append(colScores[i])
	rcount.append(i)



plt.scatter(dcount, dinv, c='b', label="Democrats")
plt.scatter(rcount, rinv, c='r', label="Republicans")
#plt.plot(rowScores, c='b', label='Dem')
#plt.plot(colScores, c='r', label='Rep')
plt.legend()
plt.show()