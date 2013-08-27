class Global:
	allowedChars = [ '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z' ]

	counter = 0
	prefix_url = "https://ly.com/"

def shorten(long_url):
	suffix_url = ''
	rem = 0
	num =  Global.counter
	if(num == 0):
		short_url = Global.allowedChars[num]

	while(num > 0):
		rem = num % len(Global.allowedChars)
		num = num / len(Global.allowedChars)
		suffix_url = Global.allowedChars[rem] + suffix_url
	Global.counter += 1
	return Global.prefix_url + suffix_url
	

