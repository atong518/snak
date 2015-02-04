from matrix import * # includes inporting Interest

# get all user's interests from relation objects
# need user or relation orm first to write this

def match(current, other, matrix):
	score = 0

	#interest_order = 

	current_interests = getInterests(user)
	other_interests = getInterests(other)

	for int1 in current_interests:
		for int2 in other_interests:

			# can't iterate into matrix like this
			score += 1 / (matrix[my_int, other_int) * my_int.get_freq())

	return score / len(current_interests)