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
	for i in range(5,-1,-1):
		if dice[i] > amount:
			amount = dice[i]
			face = i+1
	return amount, face