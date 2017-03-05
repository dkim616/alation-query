import redis
import json
import config

from pairtrie import PairTrie
from flask import Flask, g, current_app

app = Flask(__name__)

app.config.from_object(config)
app.config.from_envvar('AQUERY_SETTINGS', silent=True)

def decode_pairs():
	with app.open_resource(app.config['DATA'], 'r') as f:
		decoded = json.loads(f.read())
	return decoded

# def get_redis():
# 	if not hasattr(g, 'redis'):
# 		g.redis = redis.Redis(
# 			host=app.config['REDIS_HOST'], 
# 			port=app.config['REDIS_PORT'], 
# 			db=app.config['REDIS_DB']
# 		)
# 	return g.redis

def get_trie():
	if not hasattr(g, 'trie'):
		g.trie = PairTrie()
	return g.trie

def init_trie():
	pairs = decode_pairs()
	trie = get_trie()

	print 'Adding pairs'
	count = 0
	for name, score in pairs.iteritems():
		trie.add_pair(name, score)
		count += 1
		if count % 10000 == 0:
			print 'Added', count

# @app.cli.command('init')
def init_command():
	init_trie()
	print('Initialized data.')

@app.route('/')
def empty():
	return json.dumps([])

# @app.route('/printtrie')
# def print_trie():
# 	trie = get_trie()
# 	trie.print_trie()
# 	return json.dumps([])

@app.route('/query/<prefix>')
def query(prefix):
	trie = get_trie()
	return json.dumps(trie.query(prefix))

if __name__ == '__main__':
	with app.app_context():
		init_command()
		app.run(use_reloader=False)