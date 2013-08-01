import sys
from optparse import OptionParser
from PreSplit import PreSplit

class Usage(Exception):
	def __init__(self, msg):
		self.msg = msg

def main(args=sys.argv):
	parser = OptionParser()
	parser.add_option( "--gen", dest="gen", help="generate Commands for Split(split) or Insert(insert), Default: split", default='split')
	parser.add_option( "--dbColl", dest="dbColl", help="DbName.CollectionName, Default: 'test.foo'", default='test.foo')
	parser.add_option( "--minId", dest="minId", help="Min Id(Int) Default: 0", default=0)
	parser.add_option( "--maxId", dest="maxId", help="Max Id(Hex), Default: FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF", default='FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF')
	parser.add_option( "--recordsPerChunk", dest="recordsPerChunk", help="Records Per Chunk(Hex), Default: 00010000000000000000000000000000 ", default='00010000000000000000000000000000')
	parser.add_option( "--noOfShards", dest="noOfShards", help="No of Shards, Default: 5", default='5')
	parser.add_option( "--outFile", dest="outFile", help="Output File, Default: console", default='console')
	parser.add_option( "--top", dest="top", help="get top n Splits, Default: None", default=None)



	(options, args) = parser.parse_args(args)
	print options
	#print args
	# process arguments	
	psplit = PreSplit()
	if options.gen == 'split':
		psplit.getSplitCmds( options.dbColl, options.minId, options.maxId, options.recordsPerChunk, options.noOfShards, options.outFile, options.top )
	else:
		psplit.testInsert( options.dbColl, options.minId, options.maxId, options.recordsPerChunk, options.outFile, options.top )
	
def getParser():
	return parser

if __name__ == "__main__":
	sys.exit(main())
