import json

from pair import Pair

if __name__ == '__main__':
	pairs = []

	with open('./data/data.txt', 'r') as f:
		for line in f:
			values = line.split()
			name = values[0]
			score = values[1]
			pairs.append(Pair(name, score))

	encode = json.dumps([pair.__dict__ for pair in pairs])

	with open('./data/test.json', 'w') as f:
		f.write(encode)