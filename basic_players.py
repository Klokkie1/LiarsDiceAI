import numpy as np

from helper_functs import *

def printer(dice_total, my_dice, round_log):
	print("dice_total:", dice_total, flush=True)
	print("my_dice:", my_dice, flush=True)
	print("round_log:", round_log, flush=True)
	return (0, 0)

def incrementer(dice_total, my_dice, round_log):
	if len(round_log["player"]) == 0: # it is going first
		return 1, 2
	prev_amount = round_log["amount"][-1]
	prev_face = round_log["face"][-1]
	if prev_face == 6:
		return prev_amount+1, 2
	else:
		return prev_amount, prev_face+1
	
def incrementer2(dice_total, my_dice, round_log):
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

def ExpectedPlayer(dice_total, my_dice, round_log):

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