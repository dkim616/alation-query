class Pair(object):
	def __init__(self, name, score):
		self.name = name
		self.score = score

def from_json(json_obj):
	return (Pair(json_obj['name'], int(json_obj['score'])))