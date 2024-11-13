import numpy as np
from scipy.stats import nbinom, binom

from helper_functs import *
from basic_players import *


def adaptive_binom_player(dice_total, my_dice, round_log, *args, **kwargs):
	"""
	bids: gets statistical amount of dice based on bid_prob
	- if it is above bid_prob, it just increments
	calling: uses a binomial distribution to determine if the bid is likely correct or not
	 - required_prob
	"""
	# calculate:
	# required_prob = 0.3
	# bid_prob = 0.3

	n_my_dice = np.sum(my_dice[:])
	dice_count_not_mine = dice_total - n_my_dice

	dice_counts = kwargs.get("dice_counts")
	player_dice_not_mine = list(np.delete(dice_counts, dice_counts.index(n_my_dice)))

	player_dice_not_zero = player_dice_not_mine[:]
	while(len(player_dice_not_zero) > np.count_nonzero(player_dice_not_zero)):
		player_dice_not_zero = list(np.delete(player_dice_not_zero, player_dice_not_zero.index(0)))

	# print(player_dice_not_mine)
	# print(player_dice_not_zero)

	# setting the bid probs to be:
	# - the average dice of players that still have dice, not including me
	# - divided by that number plus n_my_dice
	# - so if I have most of the dice, the required prob to call is much higher
	# - - so im playing safer
	# - if i have less than the average, the required_prob is lower, so I call more
	# - - more risky
	# - similarly, the opposite is true for the bid probability
	# - - which is 1 - required_prob
	# - - so when im behind the average, i bid more aggressively, with a lower prob
	avg_dice_not_zero = np.average(player_dice_not_zero)
	required_prob = avg_dice_not_zero / (avg_dice_not_zero + n_my_dice)
	bid_prob = 1 - required_prob

	if kwargs.get("verbose"):
		print(f"required_prob: {round(required_prob,3)}")
		print(f"bid_prob: {round(bid_prob,3)}")

	if len(round_log["player"]) == 0: # it is going first
		stat_amount = get_statistical_amount(dice_count_not_mine, bid_prob)

		amount, face = get_largest_highest_face(my_dice)
		return amount + stat_amount, face
	
	if statistical_call(dice_total, my_dice, round_log, required_prob, kwargs.get("verbose")):
		return 0, 0
	
	prev_amount = round_log["amount"][-1]
	prev_face = round_log["face"][-1]

	stat_amount = get_statistical_amount(dice_count_not_mine, bid_prob)

	amount, face = get_largest_highest_face(my_dice)
	increase = 0
	while True:
		if is_valid(prev_face, prev_amount, face, amount + stat_amount + increase):
			return amount + stat_amount + increase, face
		increase += 1
		if amount + stat_amount + increase > dice_total:
			return 0, 0