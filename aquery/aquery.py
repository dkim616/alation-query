import redis
import pickle
import json

from pairtrie import PairTrie
from pair import Pair, from_json
from flask import Flask, g

app = Flask(__name__)

app.config.from_envvar('AQUERY_SETTINGS', silent=True)

def decode_pairs():
	with app.open_resource('data/test.json', 'r') as f:
		decoded = json.JSONDecoder(object_hook=from_json).decode(f.read())
	return decoded

def get_redis():
	if not hasattr(g, 'redis'):
		g.redis = redis.Redis(host='localhost', port=6379, db=0)
	return g.redis

def get_trie():
	r = get_redis()
	if not hasattr(g, 'trie'):
		trie = r.get('trie')
		if not trie:
			g.trie = PairTrie()
		else:
			g.trie = PairTrie(pickle.loads(trie))
	return g.trie

def init_trie():
	r = get_redis()
	pairs = decode_pairs()
	trie = get_trie()

	print 'Flushing DB'
	r.flushdb()

	for pair in pairs:
		trie.add_pair(pair, r)

	p = trie.get_pickle()
	r.set('trie', p)

	r.bgsave()

@app.cli.command('init')
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