import numpy as np
from scipy.stats import nbinom, binom

from helper_functs import *

def printer(dice_total, my_dice, round_log, *args, **kwargs):
	"""
	bids: incrementer
	calls: never

	prints out the input parameters
	"""

	print("dice_total:", dice_total)
	print("my_dice:", my_dice)
	print("round_log:", round_log)
	print("kwargs:", kwargs)

	if len(round_log["player"]) == 0: # it is going first
		return 1, 2
	
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

	if statistical_call(dice_total, my_dice, round_log, required_prob, kwargs.get("verbose")):
		return 0, 0
	return incrementer(dice_total, my_dice, round_log)

def binom_player(dice_total, my_dice, round_log, *args, **kwargs):
	"""
	bids: gets statistical amount of dice based on bid_prob
	- if it is above bid_prob, it just increments
	calling: uses a binomial distribution to determine if the bid is likely correct or not
	 - required_prob
	"""
	required_prob = 0.5
	bid_prob = 0.5

	if statistical_call(dice_total, my_dice, round_log, required_prob, kwargs.get("verbose")):
		return 0, 0
	
	n_my_dice = np.sum(my_dice[:])
	dice_count_not_mine = dice_total - n_my_dice

	if len(round_log["player"]) == 0: # it is going first
		stat_amount = get_statistical_amount(dice_count_not_mine, bid_prob)

		amount, face = get_largest_highest_face(my_dice)
		return amount + stat_amount, face
	

	prev_amount = round_log["amount"][-1]
	prev_face = round_log["face"][-1]

	stat_amount = get_statistical_amount(dice_count_not_mine, bid_prob)

	amount, face = get_largest_highest_face(my_dice)
	if is_valid(prev_face, prev_amount, face, amount + stat_amount):
		return amount + stat_amount, face
	else: # incrementing
		return incrementer(dice_total, my_dice, round_log, *args, **kwargs)