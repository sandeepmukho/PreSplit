import os
from MerkleTree import MerkleTree

""" 
File comparison using Merkle Tree- http://en.wikipedia.org/wiki/Merkle_tree
Can be used to compare files
improvements needed - Diff should contain file content difference
"""
def compareFile(filePath1, filePath2):
	mt1 = MerkleTree(filePath1)
	mt2 = MerkleTree(filePath2)
	diffList = []
	mt1.diff(mt2, 0, diffList)
	if len(diffList) == 0:
		print 'Files are Same'
	else:	
		for i in range(len(diffList)):
			print 'Files Are Different'
			print 'Diff Node ' + str(diffList[i])
			fileSize1 = os.path.getsize(filePath1)
			startLength = (mt1.dataBlocks-1) * mt1.dataBlockSize
			endLength = mt1.dataBlockSize if (i != mt1.numberOfNodes - 1) else (fileSize1 - startLength )
			endLength = startLength + endLength
			#!print "i: " + str(diffList[i]) + " StartLength: " + str(startLength) + " " + "Length: " + str(endLength)
"""
def main():
	compareFile('/tmp/a1.txt', '/tmp/a2.txt')	

if  __name__ =='__main__':main()
"""

