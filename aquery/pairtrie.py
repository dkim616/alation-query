import heapq

class TrieNode(object):
	def __init__(self, letter=None):

		self.letter = letter
		self.next = {}
		self.names = []
	
	def add_name(self, name, score):
		if (score, name) in self.names:
			return

		if len(self.names) == 10:
			top = self.names[0]
			top_name = top[1]
			top_score = top[0]
			if score > top_score or (score == top_score and name < top_name):
				heapq.heappop(self.names)
				heapq.heappush(self.names, (score, name))
		else:
			heapq.heappush(self.names, (score, name))

class PairTrie(object):
	def __init__(self):
		self.root = TrieNode()

	def add_pair(self, name, score):
		keys = name.split('_')
		if len(keys) > 1:
			keys.append(name)

		score = int(score)

		for key in keys:
			current = self.root
		
			for letter in key:
				if letter not in current.next:
					current.next[letter] = TrieNode(letter)
				current = current.next[letter]
				current.add_name(name, score)

	def print_trie(self):
		pass

	def query(self, prefix):
		current = self.root

		for letter in prefix:
			if letter not in current.next:
				return 'False'
			current = current.next[letter]

		results = []
		names = current.names[:]

		for _ in range(len(names)):
			results.append(heapq.heappop(names))

		results = [[name, score] for score, name in results]
		return list(reversed(results))