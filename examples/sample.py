#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from okuyama.client import Client


def main():
    c = Client()
    c.auto_connect(['localhost:8888'])

    #: Set data.
    for i in range(100):
        c.set(key='foo_key_{0}'.format(i), value='foo_{0}'.format(i))

    #: Get data.
    for i in range(100):
        ret = c.get(key='foo_key_{0}'.format(i))
        print(ret)

    #: Delete data.
    for i in range(100):
        ret = c.execute('delete', key='foo_key_{0}'.format(i))

    #: Set data with tags.
    for i in range(100):
        c.set(key='foo_key_{0}'.format(i), value='foo_{0}'.format(i),
              tags='foo')

    #: Get key and delete data.
    keys = c.execute('get_keys_by_tag', tag='foo')
    for k in keys:
        c.execute('delete', key=k)

    for i in range(100):
        c.set(key='foo_key_{0}'.format(i), value='foo_{0}'.format(i),
              tags=['foo', 'bar'])

    keys = c.execute('get_keys_by_tag', tag='foo')
    print(keys)
    print('-' * 80)
    keys = c.execute('get_keys_by_tag', tag='bar')
    print(keys)


if __name__ == '__main__':
    main()
