import numpy as np
from scipy.stats import binom

def is_valid(prev_face, prev_amount, next_face, next_amount):
	if next_face not in [2,3,4,5,6]:
		return False
	if next_amount > prev_amount:
		return True
	if next_amount < prev_amount:
		return False
	# count is the same
	if next_face > prev_face:
		return True
	return False

def get_largest_highest_face(dice):
	amount = 0
	face = 0
	for i in range(5,0,-1):
		if dice[i] > amount:
			amount = dice[i]
			face = i+1
	return amount, face

def effective_dice(dice):
	for i in range(1, 6):
		dice[i] += dice[0]
	return dice[:]

def get_statistical_amount(dice, chance):
	"""
	dice: the amount of dice to analyse (usually total dice - your dice)
	chance: the chance you want to use
	 - 0.1: you want the highest number of dice that has more than 10% chance of being correct
	 - 0.5: 50% chance there are this number of dice
	 - - this is often just the expected value (so dice/3)
	 - if you are being safe, give a higher chance
	 - if you are being risky, give a lower chance
	"""
	my_binom = binom(dice, 2/3)
	for i in range(dice, 0, -1):
		if my_binom.cdf(dice-i) > (chance):
			return i