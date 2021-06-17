import numpy as np
import math


def makeProb(feat):
	d = []
	n = len(feat)
	for i in range(0,n):
		sum = 0
		m = len(feat[i])
		for j in range(0,m):
			sum += feat[i][j]
		sum += 0.00000001
		d.append(sum)
	recip = np.reciprocal(d)
	Dia = np.diag(recip)
	probMat = np.matmul(Dia, feat)
	return probMat

def makePairMat(A, B):
	result = []
	for i in range(0, len(A)):
		temp = []
		for j in range(0, len(B)):
			num1 = A[i][j]
			num2 = B[j][i]
			pair = (num1, num2)
			temp.append(pair)
		result.append(temp)

	result = np.array(result)
	return result

def makeCompMat(A):
	n = len(A)
	Fin = []
	for i in A:
		temp = []
		for j in i:
			num = math.sqrt(j[0]*j[1])
			temp.append(num)

		Fin.append(temp)

	Fin = np.array(Fin)
	return Fin

def totalScore(A):
	totalrow = []
	totalcol  = []
	for i in A:
		totalrow.append(float(sum(i) / 2))

	for i in np.transpose(A):
		totalcol.append(float(sum(i) / 2))

	return totalrow, totalcol
