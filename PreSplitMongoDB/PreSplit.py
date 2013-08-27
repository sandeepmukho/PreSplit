import sys
from operator import itemgetter, attrgetter
import random

class PreSplit:
	#recordsPerChunk = '0000FFFFFFFFFFFFFFFFFFFFFFFFFFFF'
	sampleData = '", "cd" : 20110910, "gid" : 232, "md" : 20120418, "prof" : [     {       "dpid" : 7,     "md" : 20111214,        "duid" : "",    "prop" : [     {        "sid" : [       "324" ] } ] },  {       "md" : 20120418,        "dpid" : 4,     "prop" : [      {       "sid" : [       "335" ] } ] } ]'

	#get Split Commands
	def getSplitCmds(self, dbColl, minId, maxId, recordsPerChunk, noOfShards, outFile, top):
		i = 0
		moveChunkCmd = ''
		splitCmd = ''
		noOfChunks = self.getChunksPerShard( minId, maxId, recordsPerChunk, noOfShards )
		while ( minId + int( recordsPerChunk, 16 ) ) < int( maxId, 16):
			i = i + 1
			minId = minId + int( recordsPerChunk, 16 )
			splitId = hex( minId ).upper()[2:-1].zfill(32)
			splitId = splitId[:8] + '-' + splitId[8:12] + '-' + splitId[12:16] + '-' + splitId[16:20] + '-' + splitId[20:]
			splitCmd = 'printjson( db.runCommand( {split: "' + dbColl + '", middle: { _id : "' +  splitId + '" } } ) );'
			shardId = ( i / noOfChunks ) + 1
			shardName = 'shard' + str( shardId	)
			if shardId != 1:
				moveChunkCmd = 'printjson( db.runCommand( { moveChunk: "' + dbColl + '", find: { _id : "' + splitId + '" }, to: "' + shardName + '" } ) );'
			self.writeOutput(outFile, splitCmd, moveChunkCmd)
			if top is not None and i > int( top ):
				break

	#get Number of chunks Per Shard
	def getChunksPerShard(self, minId, maxId, recordsPerChunk, noOfShards):
		diff = int( maxId, 16) - minId
		noOfChunks = diff / int( recordsPerChunk, 16 )
		shardPerChunk = noOfChunks / int( noOfShards ) + 1
		return shardPerChunk
		
	def writeOutput(self, outFile, cmd1, cmd2):
		if outFile != 'console':
			f = open( outFile, 'a')
			f.write( cmd1 + '\n' )
			if cmd2 != '':
				f.write( cmd2 + '\n')
			f.close()
		else:
			print cmd1
			if cmd2 != '':
				print cmd2

	#Test inserts, random hundread inserts per chunk
	def testInsert(self, dbColl, minId, maxId, recordsPerChunk, outFile, top):
		rec = minId
		i = 0
		while ( rec + int( recordsPerChunk, 16 ) ) < int( maxId, 16):
			i = i + 1
			rec = rec + int( recordsPerChunk, 16 )
			for j in range(100):
				idVal = hex( rec + random.randint(0, 1000) ).upper()[2:-1].zfill(32)
				idVal = idVal[:8] + '-' + idVal[8:12] + '-' + idVal[12:16] + '-' + idVal[16:20] + '-' + idVal[20:]
				insCmd = dbColl + '.insert( { "_id" : "' +  idVal + PreSplit.sampleData + '} );'
				if outFile != 'console':
					print insCmd
				else:
					self.writeOutput(outFile, insCmd, '')
			if top is not None and i > int( top ):
				break


