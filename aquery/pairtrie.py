import pickle
import heapq
import json

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
			top_score = top[0]
			top_name = top[1]
			if score < top_score or score == top_score and name < top_name:
				heapq.heappop(self.names)
				heapq.heappush(self.names, (score, name))
		else:
			heapq.heappush(self.names, (score, name))

class PairTrie(object):
	def __init__(self, redis):
		self.r = redis
		# if root is None:
			# root = TrieNode('0:')

		self.root = '0:'
		self.createNode(self.root, None)

	def add_pair(self, name, score):
		keys = name.split('_')
		if len(keys) > 1:
			keys.append(name)

		score = int(score)

		for key in keys:
			# current = self.root

			depth = 0
			prev_name = '0'
			prev_hash_name = self.root
		
			for letter in key:
				depth += 1
				hash_name = letter + str(depth) + ':' + prev_name

				next = json.loads(self.r.hget(prev_hash_name, 'next'))
				if hash_name not in next:
					self.createNode(hash_name, letter)
					next.append(hash_name)
					self.r.hset(prev_hash_name, 'next', json.dumps(next))

				prev_hash_name = hash_name
				prev_name += letter + str(depth)

				self.addNameToNode(hash_name, name, score)

				# if letter not in current.next:
				# 	current.next[letter] = TrieNode(letter)
				# current = current.next[letter]
				# current.add_name(name, score)

	def createNode(self, hash_name, letter):
		self.r.hmset(hash_name, {
			'letter': letter,
			'next': json.dumps([]),
			'names': pickle.dumps([])
		})

	def addNameToNode(self, hash_name, name, score):
		names = pickle.loads(self.r.hget(hash_name, 'names'))
		if (score, name) in names:
			return

		if len(names) == 10:
			top = names[0]
			top_score = top[0]
			top_name = top[1]
			if score < top_score or score == top_score and name < top_name:
				heapq.heappop(names)
				heapq.heappush(names, (score, name))
		else:
			heapq.heappush(names, (score, name))

		self.r.hset(hash_name, 'names', pickle.dumps(names))

	def print_trie(self):
		current = self.root

		def dfs(node, level):
			for letter in node.next:
				print letter, level
				dfs(node.next[letter], level+1)

		dfs(current, 0)

	def query(self, prefix, redis):
		# current = self.root

		# for letter in prefix:
		# 	if letter not in current.next:
		# 		return 'False'
		# 	current = current.next[letter]

		# results = []
		# names = current.names[:]

		# for _ in range(len(names)):
		# 	results.append(heapq.heappop(names))

		# results = [[name, score] for score, name in results]
		# return list(reversed(results))

		depth = 0
		prev_name = '0'
		prev_hash_name = self.root

		for letter in prefix:
			depth += 1
			hash_name = letter + str(depth) + ':' + prev_name

			next = self.r.hget(prev_hash_name, 'next')
			if next is None:
				return False
			decoded_next = json.loads(next)
			if hash_name not in decoded_next:
				return 'False'

			prev_hash_name = hash_name
			prev_name += letter + str(depth)

		results = []
		names = pickle.loads(self.r.hget(hash_name, 'names'))[:]

		if names:
			for _ in range(len(names)):
				results.append(heapq.heappop(names))

			results = [[name, score] for score, name in results]
			return list(reversed(results))

		return 'False'

	
	def get_pickle(self):
		return pickle.dumps(self.root)