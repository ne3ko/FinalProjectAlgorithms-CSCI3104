# Nikolai Alexander
# Final Project
# December 8, 2018

import numpy as np
import pandas as pd
import csv
import random
import math
import sys


# -----PROBLEM 1 CODE-----
def read_sequence(filename) :
	# Open the file and read the sequence into a string called 'seq'.
	# Replace line breaks ('\n') with no character, pieces the sequence into 
	# one line.
	with open(filename, 'r') as file_a :
		seq = file_a.read().replace('\n', '')

	# Get rid of the '>' symbol at the beginning of the sequence
	seq = seq.replace('>','')

	return seq

def LCS_Table(x, y) :
	# Create a zero matrix of the dimensions of the lengths of the sequences + 1
	col_len = len(x) + 1
	row_len = len(y) + 1
	S = np.zeros((row_len, col_len))

	# Iterates through rows and columns. If the characters match, add to the
	# previous matched character in the sequence. If the the characters no not
	# match, assign the largest length and move on.
	# We start at index 1 instead of 0 to avoid the spaces in the beginning
	# of each string in 
	for j in range(1,row_len) :
		for i in range(1, col_len) :
			if x[i-1] == y[j-1] :
				S[j,i] = S[j-1,i-1] + 1
			else :
				S[j,i] = max(S[j-1,i], S[j,i-1])

	return S

def LCS_Subsequence(S, x, y) :
	i = len(x)
	j = len(y)

	# Create an empty string to store the sequence
	seq = ''

	# Iterate backwards through table until you reach S[0,i] or S[j,0]
	while i > 0 and j > 0 :
		# If the characters match, move to the next of each character
		if x[i-1] == y[j-1] :
			seq = x[i-1] + seq
			i -= 1
			j -= 1
		else :
			# If x is apart of a larger sequence, move to that sequence
			if S[j,i] == S[j-1,i] :
				j -= 1
			# If y is appart of a larger sequence, move to that sequence
			elif S[j,i] == S[j,i-1] :
				i -= 1

	return seq

def problem_1() :
	print("___PROBLEM 1: Longest Common Subsequence___")

	# Read sequences into strings
	seqa = read_sequence("sequence_A.fa")
	seqb = read_sequence("sequence_B.fa")
	seqc = read_sequence("sequence_C.fa")

	# Create tables comparing each string
	a_vs_b = LCS_Table(seqa,seqb)
	a_vs_c = LCS_Table(seqa,seqc)
	b_vs_c = LCS_Table(seqb,seqc)

	print("A vs B Table:\n", a_vs_b)
	print()
	print("A vs C Table:\n", a_vs_c)
	print()
	print("B vs C Table:\n", b_vs_c)
	print()
	print()

	# Find the Longest Common Subsequence for each combination
	abseq = LCS_Subsequence(a_vs_b, seqa, seqb)
	acseq = LCS_Subsequence(a_vs_c, seqa, seqc)
	bcseq = LCS_Subsequence(b_vs_c, seqb, seqc)

	print("AB Subsequence:\n%s" % abseq)
	print()
	print("AC Subsequence:\n%s" % acseq)
	print()
	print("BC Subsequence:\n%s" % bcseq)
	print()
	print()

	# Determine which sequences are humand and which sequence is a soybean.
	# We know there are two human chomosomes and 1 soybean chromosome. Therefore,
	# the sequences with the longest Longest Common Subsequence are human
	# chromosomes, while the remaining sequence is that of a soybean.
	LCS_length = max(len(abseq), len(acseq), len(bcseq))
	if LCS_length == len(abseq) :
		print("Sequence_A and Sequence_B are Homo Sapien (human)")
		print("Sequence_C is of Glycine Max (soybean).")
	elif LCS_length == len(acseq) :
		print("Sequence_A and Sequence_C are of Homo Sapien.")
		print("Sequence_B is of Glycine Max (soybean).")
	elif LCS_length == len(bcseq) :
		print("Sequence_B and Sequence_C are of Homo Sapien.")
		print("Sequence_A is of Glycine Max (soybean).")
	print()
	print()
	print()

	return

# Export Longest Common Subsequence tables to csv files
	# a_list = ['_'] 
	# b_list = ['_']
	# c_list = ['_']
	# for i in range(0, len(seqa)) :
	# 	a_list.append(seqa[i])
	# for i in range(0, len(seqb)) :
	# 	b_list.append(seqb[i])
	# for i in range(0, len(seqc)) :
	# 	c_list.append(seqc[i])


	# ab_df = pd.DataFrame(a_vs_b, columns = a_list)
	# ab_df.insert(loc = 0, column = "y", value = b_list)
	# ab_df.to_csv('AB_Table.csv')


	# ac_df = pd.DataFrame(a_vs_c, columns = a_list)
	# ac_df.insert(loc = 0, column = "y", value = c_list)
	# ac_df.to_csv('AC_Table.csv')


	# bc_df = pd.DataFrame(b_vs_c, columns = b_list)
	# bc_df.insert(loc = 0, column = "y", value = c_list)
	# bc_df.to_csv('BC_Table.csv')




# -----PROBLEM 3 CODE-----
def PandasPeril_Greedy(A) :
	first = 0
	last = len(A)-1
	choice = None

	if A[first] >= A[last] :
		choice = A[first]
		del A[first]
		return choice
	else :
		choice = A[last]
		del A[last]
		return choice

def PandasPeril_Dynamic(A) :
	sum1 = A[0]
	sum2 = A[len(A)-1]
	choice = None

	# If Player 1 chooses the first card
	i1 = 1
	j1 = len(A)-1
	# Player 2 chooses the largest of the next 2 cards
	if A[i1] >= A[j1] :
		i1 += 1
	else :
		j1 -= 1
	# Continue the game until there are no cards left
	while i1 < j1 :
		if A[i1] >= A[j1] :
			sum1 += A[i1]
			i1 += 1
		else :
			sum1 += A[j1]
			j1 -= 1

		if A[i1] >= A[j1] :
			i1 += 1
		else :
			j1 -= 1 

	# Case 2: Player 1 chooses the last card
	i2 = 0
	j2 = len(A)-2
	# Player 2 chooses the largest of the next 2 cards
	if A[i2] >= A[j2] :
		i2 += 1
	else :
		j2 -= 1
	# Continue the game until there are no cards left
	while i2 < j2 :
		if A[i2] >= A[j2] :
			sum2 += A[i2]
			i2 += 1
		else :
			sum2 += A[j2]
			j2 -= 1

		if A[i2] >= A[j2] :
			i2 += 1
		else :
			j2 -= 1

	# Compare both sums, choose the card that produces the largest sum
	if sum1 >= sum2 :
		choice = A[0]
		del A[0]
		return choice
	else :
		choice = A[len(A)-1]
		del A[len(A)-1]
		return choice


def problem_3() :
	print("___PROBLEM 3: Pandas Peril___")

	# Number of games played
	games = 2

	# For loop simulating a number of games
	for x in range(0,games) :
		# Assign random set of random even length
		set1 = []
		set1_length = random.randint(1,10) * 2
		for i in range(0,set1_length) :
			set1.append(random.randint(1,100))
		print("GAME %d" % (x+1))
		print("Set:",set1)
		
		# Create player sets
		player1_set = []
		player2_set = []

		# Play the game until there are no cards remaining
		while len(set1) > 0 :
			player1_set.append(PandasPeril_Dynamic(set1))
			player2_set.append(PandasPeril_Greedy(set1))

		# Find the sum of each set
		player1_sum = sum(player1_set)
		player2_sum = sum(player2_set)

		print("Player 1 (Dynamic):", player1_set)
		print("\tTotal: %d" % player1_sum)
		print("Player 2 (Greedy):",player2_set)
		print("\tTotal: %d" % player2_sum)

		# See which set wins
		if player1_sum > player2_sum :
			print("Player 1 Wins!")
		elif player1_sum < player2_sum :
			print("Player 2 Wins!")
		else:
			print("It's a Tie!")
		print()

	print()
	print()
	return




# -----PROBLEM 4 CODE-----
def MinMax_Compare(A1, A2) :
	minmax_coords = [0,0]

	# If both arrays contain 1 number, compare those numbers and place the
	# lowest as the minimum and the highest as the maximum
	if len(A1) == 1 and len(A2) == 1 :
		minmax_coords[0] = min(A1[0],A2[0])
		minmax_coords[1] = max(A1[0],A2[0])
	# If one of the two arrays only contains 1 number, compare the number
	# with each the two numbers in the other array, and place the minimum
	# in the first element and the maximum in the second element
	elif len(A1) == 1 :
		minmax_coords[0] = min(A1[0],A2[0])
		minmax_coords[1] = max(A1[0],A2[1])
	elif len(A2) == 1 :
		minmax_coords[0] = min(A1[0],A2[0])
		minmax_coords[1] = max(A1[1],A2[0])
	# If both contain a minimum and maximum element, compare the first elements
	# and keep the minimum of the two, and then compare the second elements
	# and return the maximum of the two
	else :
		minmax_coords[0] = min(A1[0],A2[0])
		minmax_coords[1] = max(A1[1],A2[1])

	return minmax_coords


def MinMax_Merge(A) :
	if len(A) > 1 :
		p = math.floor(len(A)/2)
		# Divide - Split list in half until we get each seperate element
		A1 = MinMax_Merge(A[0:p])
		A2 = MinMax_Merge(A[p:len(A)])

		# Conquer - Compare minimum and maximum elements, until you have
		# the largest element in the set, and the smallest element in the
		# set.
		return MinMax_Compare(A1,A2)

	# When we have one element left begin to merge
	return A


def Smallest_Rectangle(M) :
	# Lists of x-coordinates and y-coordinates in S 
	x_coords = M[:,0]
	y_coords = M[:,1]

	# Minimum & Maximum coordinates for x and y
	minmax_x = MinMax_Merge(x_coords)
	minmax_y = MinMax_Merge(y_coords)

	# Coordinates of each corner in R
	pointBL = [minmax_x[0],minmax_y[0]]
	pointTL = [minmax_x[0],minmax_y[1]]
	pointBR = [minmax_x[1],minmax_y[0]]
	pointTR = [minmax_x[1],minmax_y[1]]


	R = np.array([pointBL, pointTL, pointBR, pointTR])

	return R

def problem_4 ():
	print("___PROBLEM 4: Smallest Bounding Rectangle___")

	# Create a set 50 random points on an xy-plane
	points = 50
	S = np.zeros((points,2))
	for i in range(0,points) :
		S[i,0] = random.randint(0,250)
		S[i,1] = random.randint(0,250)

	print("Set of points S:\n",S.tolist())
	print()

	# Finds the smallest rectangle containing the points in S
	R = Smallest_Rectangle(S)

	print("Smallest rectangle R:", R.tolist())

	return


if __name__ == "__main__":
	# Run Problem 1
	problem_1()

	# Run Problem 3
	problem_3()
	
	# Reun Problem 4
	problem_4()