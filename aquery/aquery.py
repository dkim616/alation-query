import redis
import pickle
import json

from pairtrie import PairTrie
from pair import Pair, from_json
from flask import Flask, g, current_app

app = Flask(__name__)

app.config.from_envvar('AQUERY_SETTINGS', silent=True)

def decode_pairs():
	with app.open_resource('data/test2.json', 'r') as f:
		decoded = json.loads(f.read())
	return decoded

def get_redis():
	if not hasattr(g, 'redis'):
		g.redis = redis.Redis(host='localhost', port=6379, db=0)
	return g.redis

def get_trie():
	r = get_redis()
	if not hasattr(g, 'trie'):
		# trie = r.get('trie')
		# if not trie:
		print 'New Trie'
		g.trie = PairTrie(r)
		# else:
		# 	g.trie = PairTrie(pickle.loads(trie), redis=r)
	return g.trie

def init_trie():
	r = get_redis()

	# print 'Flushing DB'
	# r.flushdb()

	if not r.hgetall('0:'):
		pairs = decode_pairs()
		trie = get_trie()

		print 'Adding pairs'
		count = 0
		for name, score in pairs.iteritems():
			# if not r.get(name):
			# 	r.set(name, score)
			trie.add_pair(name, score)
			count += 1
			if count % 10000 == 0:
				print 'Added', count

	# print 'Pickling trie'
	# p = trie.get_pickle()

	# print 'Adding trie to redis'
	# r.set('trie', p)

	print 'Saving redis data in background'
	r.bgsave()

# @app.cli.command('init')
def init_command():
	init_trie()
	print('Initialized data.')

@app.route('/')
def empty():
	return json.dumps([])

@app.route('/printtrie')
def print_trie():
	trie = get_trie()
	trie.print_trie()
	return json.dumps([])

@app.route('/query/<prefix>')
def query(prefix):
	r = get_redis()
	trie = get_trie()
	return json.dumps(trie.query(prefix, r))

if __name__ == '__main__':
	with app.app_context():
		init_command()
		app.run(use_reloader=False)