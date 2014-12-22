okuyama
=======
.. image:: https://travis-ci.org/heavenshell/py-okuyama.svg?branch=master

Distributed key-value-store okuyama's Python client.


Usage
-----

Connect to MasterNode.

.. code:: python

  from okuyama import Client

  client = Client()
  client.auto_connect(['masternode1:8888', 'masternode2:8888'])


Set value

.. code:: python

  print(client.set('key', 'val')) # => True

.. code:: python

  print(client.get('key')) # => 'val'

Remove value

.. code:: python

  print(client.delete('key')) #=> True
  print(client.delete('key')) #=> None

Set tags

.. code:: python

  print(client.set('key1', 'val1', tags=['tag1'])) #=> True
  print(client.set('key2', 'val2', tags=['tag1', 'tag2'])) #=> True

Get keys from tag

.. code:: python

  print(client.execute('get_keys_by_tag', tag='tag1'])) #=> [key1, key2]
