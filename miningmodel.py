import random

# see https://medium.com/@peoplma/an-attempt-at-a-simple-mathematical-model-for-quantifying-bitcoin-mining-centralization-pressure-db936c021442#.nbvctuxwi for discussion of this equation
# f = r(((s/b)y)/t))/(1-n((((s/b)y)/t)))
# f = minimum fee a transaction must pay to get included. Also equals the marginal risk of orphan that the miner takes by including it. (BTC)
# r = block reward (BTC)
# s = size of transaction (Bytes)
# b = upload bandwidth of miner (Bytes per second)
# y = number of peers miner will propagate the block to
# t = network average time to find a block (Seconds)
# n = total number of transactions in the block.

r = 25.000
s = 500.000
b = 9000000.000 # this is bandwidth of miner, vary this
y = 8.000
t = 600.000
#n = range(starting integer, ending integer, step)
fset = set()

for n in range(1,2000,1): # middle number is num of txes to calculate minfee for
	#print n
	f = (r*(((s/b)*y)/t))/(1-n*((((s/b)*y)/t))) # this calculates minimum fee each transaction must pay for a miner to include profitably
	#print f
	fset.add(f)
#print fset

tset = set()
for t in range(1,2000,1): # generates set of transactions, middle number is num txes
	t = random.normalvariate(0.0002, 0.0001) # generates normal curve of transaction fees (mean, stdev)
	if t <= 0: # sets transaction fees generated as negative to 0
		t = 0.000
	else:
		t = t
	tset.add(t)
#print tset
print str(len(tset))+"  :number of transactions paying >0 fee"
tsetdescending = sorted(tset, reverse=True) # sorts transaction fee set in descending order
#print tsetdescending

zipped = zip(fset, tsetdescending)
enumeration = enumerate(zipped)
totaltx = set()
totalfee = set()
for (x, (fset, tsetdescending)) in enumeration:
	totaltx.add(x)
	totalfee.add(tsetdescending)
	if tsetdescending <= fset or x==2000: # includes all transactions paying more than f up to x (x*s=max_block_size)
		print str(x) + "  :number of transactions included"
		print str(fset)+"  :minimum fee transactions had to pay"
		print str(tsetdescending) + "  :fee of first transaction that paid less than minimum fee"  
		#print len(totaltx)
		print str(sum(totalfee))+"  :total transaction fees included"
		perblock = 0.33333*(r+sum(totalfee)) # coefficient is miner's share of total network hashpower
		print str(perblock)+"  :total fees + block reward * % of hashpower" 
		orphanrateperblock = x*s/b*y/600
		print str(orphanrateperblock)+"  :expected chance of orphan (1=100%)"
		revenueperblock = perblock-(perblock*orphanrateperblock)
		print str(revenueperblock)+"  :revenue per block after orphan rate"
		break
		