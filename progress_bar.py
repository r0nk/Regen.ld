# this function creates a progress bar

def progress_bar(amt, change_lenght_of_bar = 2):
	'''
	this function prints out a progress bar 
	based on a percentage form 0% to 100%.
	to shorten the progress bar increase change_lenght_of_bar number:
	1, 2, 5, 10 will produce equal bars
	1  = 100 ticks
	2  =  50 ticks
	5  =  20 ticks
	10 =  10 ticks
	'''

	# extended ascii codes needed to print out the progress bar
	em = bytes([176]).decode('cp437')
	full = bytes([178]).decode('cp437')

	not_amt = 100 - amt
	str = full * round(amt/change_lenght_of_bar) + em * round(not_amt/change_lenght_of_bar)
	return str

# to test 0% though 100%
if __name__ == "__main__":
	for i in range(101):
		print(progress_bar(i, 5))