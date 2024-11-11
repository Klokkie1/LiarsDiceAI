import numpy as np
from scipy.stats import nbinom, binom

from helper_functs import *

def printer(dice_total, my_dice, round_log, *args, **kwargs):
	"""
	bids: incrementer
	calls: never

	prints out the input parameters
	"""
	if len(round_log["player"]) == 0: # it is going first
		return 1, 2

	print("dice_total:", dice_total)
	print("my_dice:", my_dice)
	print("round_log:", round_log)
	return incrementer(dice_total, my_dice, round_log, *args, **kwargs)

def incrementer(dice_total, my_dice, round_log, *args, **kwargs):
	"""
	bids: incrementer
	calls: never
	"""
	if len(round_log["player"]) == 0: # it is going first
		return 1, 2
	prev_amount = round_log["amount"][-1]
	prev_face = round_log["face"][-1]
	if prev_face == 6:
		return prev_amount+1, 2
	else:
		return prev_amount, prev_face+1
	
def incrementer2(dice_total, my_dice, round_log, *args, **kwargs):
	"""
	bids: incrementer
	calls: if the bid dice is more than the total dice
	"""
	if len(round_log["player"]) == 0: # it is going first
		return 1, 2
	prev_amount = round_log["amount"][-1]
	prev_face = round_log["face"][-1]
	if prev_amount > dice_total:
		return 0, 0 # calling
	if prev_face == 6:
		return prev_amount+1, 2
	else:
		return prev_amount, prev_face+1

def ExpectedPlayer(dice_total, my_dice, round_log, *args, **kwargs):
	"""
	bids: expected amount using its dice
	calls: if bid is above expected
	
	expected: int divide by 3 (divide then floor)
	"""

	n_my_dice = np.sum(my_dice)
	dice_count_not_mine = dice_total - n_my_dice
	out_expected = [dice_count_not_mine//3]*6
	expected = np.add(out_expected, my_dice)


	if len(round_log["player"]) == 0: # it is going first
		# get the largest amount of dice i have, and bit that plus expected
		return get_largest_highest_face(expected)
	
	# have to deal with previous bids
	prev_amount = round_log["amount"][-1]
	prev_face = round_log["face"][-1]

	if prev_amount > expected[prev_face-1]:
		# if the previous bid is higher than expected amounts, call
		return 0, 0
	
	# if not calling, bid the highest expected amount
	amount, face = get_largest_highest_face(expected)
	if (is_valid(prev_face, prev_amount, face, amount)):
		return amount, face
	else: # if it is not a valid bid, just increment it
		# i am not 100% sure if it is even possible to get here
		return incrementer(dice_total, my_dice, round_log)
	
def ExpectedPlayer2(dice_total, my_dice, round_log, *args, **kwargs):
	"""
	bids: expected amount using its dice
	calls: if bid is above expected
	
	expected: divide by 3 then round
	"""

	n_my_dice = np.sum(my_dice)
	dice_count_not_mine = dice_total - n_my_dice
	out_expected = [round(dice_count_not_mine/3)]*6
	expected = np.add(out_expected, my_dice)


	if len(round_log["player"]) == 0: # it is going first
		# get the largest amount of dice i have, and bit that plus expected
		return get_largest_highest_face(expected)
	
	# have to deal with previous bids
	prev_amount = round_log["amount"][-1]
	prev_face = round_log["face"][-1]

	if prev_amount > (expected[prev_face-1]):
		# if the previous bid is higher than expected amounts, call
		return 0, 0
	
	# if not calling, bid the highest expected amount
	amount, face = get_largest_highest_face(expected)
	if (is_valid(prev_face, prev_amount, face, amount)):
		return amount, face
	else: # if it is not a valid bid, just increment it
		# i am not 100% sure if it is even possible to get here
		return incrementer(dice_total, my_dice, round_log)

def inc_binom_caller(dice_total, my_dice, round_log, *args, **kwargs):
	"""
	bids: incrementer
	calling: uses a binomial distribution to determine if the bid is likely correct or not
	 - required_prob
	"""
	required_prob = 0.5

	if len(round_log["player"]) == 0: # it is going first
		return 1, 2
	
	n_my_dice = np.sum(my_dice[:])
	dice_count_not_mine = dice_total - n_my_dice

	my_dice_effective = effective_dice(my_dice)
	
	prev_amount = round_log["amount"][-1]
	prev_face = round_log["face"][-1]

	my_binom = binom(dice_count_not_mine, 2/3)
	required_amount = prev_amount - my_dice_effective[prev_face-1]
	bin_prob = my_binom.cdf(dice_count_not_mine - required_amount)
	if kwargs.get("verbose"):
		print(f"not_mine: {dice_count_not_mine}, required_amount: {required_amount}, bin_prob: {round(bin_prob,3)}")
		# print(f"dice_total: {dice_total}, n_my_dice: {n_my_dice}")
		# print(f"my_dice: {my_dice}")
	if bin_prob < required_prob:
		return 0, 0
	return incrementer(dice_total, my_dice, round_log)