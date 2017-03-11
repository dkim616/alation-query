# aquery-server

Simple Flask server to enable searching of a million string/int pairs with a prefix query. The query returns the top ten pairs related to prefix. Keywords from names are separated by "_".

Example:
Querying 'prefix' should return all pairs that start with prefix or have a "_" separated keyword starting with 'prefix'.

Query: foo
Returns foo_bar: 10000, foo: 2000, has_foo: 1000, one_two_foo: 123
