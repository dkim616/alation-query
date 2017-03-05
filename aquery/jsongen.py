import sys
import json
import random

if __name__ == '__main__':
	pairs = {}

	if len(sys.argv) == 2:
		gen = sys.argv[1]

		if gen == 'gen':
			for i in range(1000000):
				alphabet = 'abcdefghijklmnopqrstuvwxyz'
				first = []
				second = []
				for _ in range(8):
					first.append(alphabet[random.randint(0, len(alphabet)-1)])
					second.append(alphabet[random.randint(0, len(alphabet)-1)])
				name = "".join(first) + '_' + "".join(second)
				pairs[name] = random.randint(0, 1000000)

			output_name = 'test2'

	if not pairs:
		with open('./data/data.txt', 'r') as f:
			for line in f:
				values = line.split()
				name = values[0]
				score = values[1]
				pairs[name] = score

		output_name = 'test'

	encoded = json.dumps(pairs)

	with open('./data/'+output_name+'.json', 'w') as f:
		f.write(encoded)