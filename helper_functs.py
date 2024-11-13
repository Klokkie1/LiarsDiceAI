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
	output = dice[:]
	for i in range(6):
		output[i] += dice[0]
	return output

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
		if my_binom.cdf(dice-i) >= (chance):
			return i
	return 0
		
def statistical_call(dice_total, my_dice, round_log, required_prob, verbose=False):
	"""
	gets the statistical likelihood of the previous bid being correct using:
	 - number of dice not yours
	 - your dice
	if the likelihood is less than required_prob, then returns True, else returns False

	if this function is called as the first play of the round, then it returns False immediately
	"""
	if len(round_log["player"]) == 0: # it is going first
		return False

	n_my_dice = np.sum(my_dice[:])
	dice_count_not_mine = dice_total - n_my_dice

	my_dice_effective = effective_dice(my_dice)
	
	prev_amount = round_log["amount"][-1]
	prev_face = round_log["face"][-1]

	my_binom = binom(dice_count_not_mine, 2/3)
	required_amount = prev_amount - my_dice_effective[prev_face-1]
	bin_prob = my_binom.cdf(dice_count_not_mine - required_amount)
	if verbose:
		print(f"not_mine: {dice_count_not_mine}, required_amount: {required_amount}, bin_prob: {round(bin_prob,3)}")
		# print(f"dice_total: {dice_total}, n_my_dice: {n_my_dice}")
		# print(f"my_dice: {my_dice}")
	if bin_prob <= required_prob:
		return True
	return False