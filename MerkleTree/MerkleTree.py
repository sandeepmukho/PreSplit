import math
import os
import FileUtility
from MerkleTreeNode import MerkleTreeNode
import md5

""" Merkle Tree- http://en.wikipedia.org/wiki/Merkle_tree
Can be used to compare files
two improvements needed - Files should be read chunk by chunk
and Diff should contain file content difference
"""
class MerkleTree(object):
	algorthim = "MD5"
	DEFAULT_HEIGHT = 0
	DEFAULT_CHUNK_SIZE = 50
    
	def __init__(self, filePath):
		self.filePath = filePath
		readData = FileUtility.readFile(filePath)
		self.height = MerkleTree.getHeightOfMerkleTree(self.filePath, MerkleTree.DEFAULT_CHUNK_SIZE)
		print "filePath: " + self.filePath + " Length: " + str(len(readData)) + " Height: " + str(self.height)
		self.buildTree(readData)

	#!builds a merkle tree
	def buildTree(self, data):
		#! number of nodes
		self.startDataNode = int(math.pow( 2, self.height) - 1)
		self.dataBlocks = int(math.pow( 2, self.height))
		self.numberOfNodes = 2 * self.dataBlocks - 1
		#! dataBlockSize = data.length / dataBlocks - initially used it 
		self.dataBlockSize = MerkleTree.DEFAULT_CHUNK_SIZE
		self.nodes = [MerkleTreeNode(0)] * self.numberOfNodes
		startLength = 0
		destLength = 0

		for i  in range(self.startDataNode, self.numberOfNodes):
			#!calculates start and endLength of block size
			blockSize = self.dataBlockSize if (i != self.numberOfNodes - 1) else (len(data) - startLength)
			self.nodes[i] = MerkleTreeNode(blockSize)
			destLength = startLength + blockSize

			#!print "i: " + str(i) + " StartLength: " + str(startLength) + " Length: " + str(destLength)
			self.nodes[i].data = data[startLength:destLength]

			startLength += self.dataBlockSize		

	#!returns height of merkle tree based on chunk size
	@staticmethod
	def getHeightOfMerkleTree(path, chunkSize):
		fileSize = os.path.getsize(path)
		chunks = fileSize / chunkSize
		try:
			height = math.ceil(math.log(chunks))
		except ValueError:
			height = MerkleTree.DEFAULT_HEIGHT
			print 'File size less than 1KB'			
		height = MerkleTree.DEFAULT_HEIGHT if (height < MerkleTree.DEFAULT_HEIGHT) else height
		return height

	#! hash of ith node of Merkle Tree
	def hash(self, i):
		hash = None;
		m = md5.new()

		if i >= self.startDataNode:
			m.update(self.nodes[i].data)
			hash = m.hexdigest()
		else:
			leftHash = self.hash(2 * i + 1)
			rightHash = self.hash(2 * i + 2)
			resultHash = leftHash + rightHash
			m.update(resultHash)
			hash = m.hexdigest()
		return hash

	#! return true or false based on file is same or different
	def diff(self, tree, i):
		b = True
		if self.height != tree.height:
			b = False
		else:
			if (i < self.numberOfNodes):
				hash1 = self.hash(i)
				hash2 = tree.hash(i)
				b = b and (hash1 == hash2)
				if (i < self.startDataNode):
				    b = b and self.diff(tree, 2 * i + 1);
				    b = b and self.diff(tree, 2 * i + 2);
		return b

	#! diffList contains all the block nodeIds which are different
	def diff(self, tree, i, diffList):
		b = True
		if (self.height != tree.height):
			b = False
		else:
			if i < self.numberOfNodes:
				hash1 = self.hash(i)
				hash2 = tree.hash(i)
				b = (hash1 == hash2)
				if not b and i >= self.startDataNode:
					diffList.append(i)
				if i < self.startDataNode:
					b = self.diff(tree, 2 * i + 1, diffList);
					b = self.diff(tree, 2 * i + 2, diffList);


