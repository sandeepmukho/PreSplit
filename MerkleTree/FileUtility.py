
def readFile(path):
	inputFile = open(path, "rb") # opening for [r]eading as [b]inary
	data = inputFile.read() # if you only wanted to read 512 bytes, do .read(512)
	inputFile.close
	return data
