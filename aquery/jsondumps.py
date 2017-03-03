import json
import random

from pair import Pair

if __name__ == '__main__':
	# pairs = []
	pairs = {}

	# with open('./data/data.txt', 'r') as f:
	# 	for line in f:
	# 		values = line.split()
	# 		name = values[0]
	# 		score = values[1]
	# 		pairs[name] = score

	for i in range(1000000):
		alphabet = 'abcdefghijklmnopqrstuvwxyz'
		first = []
		second = []
		for _ in range(8):
			first.append(alphabet[random.randint(0, len(alphabet)-1)])
			second.append(alphabet[random.randint(0, len(alphabet)-1)])
		name = "".join(first) + '_' + "".join(second)
		pairs[name] = random.randint(0, 1000000)

	# encode = json.dumps([pair.__dict__ for pair in pairs])
	encode = json.dumps(pairs)

	with open('./data/test2.json', 'w') as f:
		f.write(encode)