okuyama
=======

Distributed key-value-store okuyama's Python client.

.. image:: https://travis-ci.org/heavenshell/py-okuyama.svg?branch=master

Usage
-----

Connect to MasterNode.

::
  from okuyama import Client

  client = Client()
  client.auto_connect(['masternode1:8888', 'masternode2:8888'])


Set value

::
  print(client.set('key', 'val')) # => True

::
  print(client.get('key')) # => 'val'

Remove value

::
  print(client.delete('key')) #=> True
  print(client.delete('key')) #=> None

Set tags

::
  print(client.set('key1', 'val1', tags=['tag1'])) #=> True
  print(client.set('key2', 'val2', tags=['tag1', 'tag2'])) #=> True

Get keys from tag

::

  print(client.execute('get_keys_by_tag', tag='tag1'])) #=> [key1, key2]
