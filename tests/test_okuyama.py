# -*- coding: utf-8 -*-
"""
    okuyama.tests.test_okuyama
    ~~~~~~~~~~~~~~~~~~~~~~~~~~

    Tests for Python okuyama client.


    :copyright: (c) 2014 Shinya Ohyanagi, All rights reserved.
    :copyright: (c) 2014 Kobe Digital Labo Inc, All rights reserved.
    :license: BSD, see LICENSE for more details.
"""
import logging
import mock
from unittest import TestCase
from okuyama.client import Client, Constants, GetCommand, SetCommand, \
    DeleteCommand, GetKeysByTagCommand, OkuyamaError, to_unicode


class TestOkuyama(TestCase):
    def test_should_create_instance(self):
        """ Client() should create instance. """
        c = Client()
        self.assertTrue(isinstance(c, Client))

    def test_should_set_default_logger(self):
        """ Client() should set default logger. """
        c = Client()
        self.assertTrue(isinstance(c.logger, logging.Logger))

    def test_should_raise_error_when_host_format_is_wrong(self):
        """ Client().auto_connect() should raise error when host format is wrong. """
        c = Client()
        with self.assertRaises(OkuyamaError):
            c.auto_connect(['localhost'])

    @mock.patch('okuyama.client.socket')
    def test_should_execute_command(self, m):
        """ Client().execute() should execute command. """
        m.recv.return_value = '2,true,YmFy\n'

        c = Client()
        c.socket = m
        ret = c.execute('get', key='foo')
        self.assertEqual(to_unicode(ret), 'bar')

    @mock.patch('okuyama.client.socket')
    def test_should_execute_get(self, m):
        """ Client().get() should return result of get value. """
        m.recv.return_value = '2,true,YmFy\n'

        c = Client()
        c.socket = m
        ret = c.get(key='foo')
        self.assertEqual(to_unicode(ret), 'bar')

    @mock.patch('okuyama.client.socket')
    def test_should_execute_set(self, m):
        """ Client().set() should return True when set success. """
        m.recv.return_value = '1,true,OK\n'

        c = Client()
        c.socket = m
        ret = c.set(key='foo', value='bar')
        self.assertTrue(ret)

    @mock.patch('okuyama.client.socket')
    def test_should_register_command(self, m):
        """ Client().register_command() should register command. """
        m.recv.return_value = '2,true,YmFy\n'

        c = Client()
        c.register_command('foo', GetCommand)

        c.socket = m
        ret = c.execute('foo', key='foo')
        self.assertEqual(to_unicode(ret), 'bar')


class TestGetCommand(TestCase):
    @classmethod
    def setUpClass(cls):
        logger = logging.getLogger(__name__)
        cls.command = GetCommand(Constants, logger)

    def test_should_build_command(self):
        """ GetCommand().build() should build get command. """
        ret = self.command.build(key='foo')
        self.assertEqual(ret, '2,Zm9v\n')

    def test_should_parse_response(self):
        """ GetCommand().parse() should parse get command response. """
        ret = self.command.parse('2,true,YmFy\n')
        self.assertEqual(to_unicode(ret), 'bar')


class TestSetCommand(TestCase):
    @classmethod
    def setUpClass(cls):
        logger = logging.getLogger(__name__)
        cls.command = SetCommand(Constants, logger)

    def test_should_build_command(self):
        """ SetCommand().build() should build set command. """
        ret = self.command.build(key='foo', value='baz')
        self.assertEqual(ret, '1,Zm9v,(B),0,YmF6\n')

    def test_should_parse_response(self):
        """ SetCommand().parse() should parse get command response. """
        ret = self.command.parse('1,true,OK\n')
        self.assertTrue(ret)

    def test_should_build_command_with_tag(self):
        """ SetCommand.build() shoul build set command with tag. """
        ret = self.command.build(key='foo', value='bar', tags='baz')
        self.assertEqual(ret, '1,Zm9v,YmF6,0,YmFy\n')

    def test_should_build_command_with_tags(self):
        """ SetCommand.build() shoul build set command with tags. """
        ret = self.command.build(key='foo', value='bar', tags=['tag1', 'tag2'])
        self.assertEqual(ret, '1,Zm9v,dGFnMQ==:dGFnMg==,0,YmFy\n')


class TestDeleteCommand(TestCase):
    @classmethod
    def setUpClass(cls):
        logger = logging.getLogger(__name__)
        cls.command = DeleteCommand(Constants, logger)

    def test_should_build_command(self):
        """ DeleteCommand().build() should build delete command. """
        ret = self.command.build(key='foo')
        self.assertEqual(ret, '5,Zm9v,0\n')

    def test_should_parse_response(self):
        """ DeleteCommand().parse() should parse delete command response. """
        ret = self.command.parse('5,true,YmF6\n')
        self.assertTrue(ret)


class TestGetKeysByTagCommand(TestCase):
    @classmethod
    def setUpClass(cls):
        logger = logging.getLogger(__name__)
        cls.command = GetKeysByTagCommand(Constants, logger)

    def test_should_build_command(self):
        """ GetKeysByTagCommand().build() should build getKeysByTag command. """
        ret = self.command.build(tag='foo')
        self.assertEqual(ret, '3,Zm9v,false\n')

    def test_should_parse_response(self):
        """ GetKeysByTagCommand().parse() should parse getKeysByTag command response. """
        ret = self.command.parse('4,true,Zm9vX2tleV85Mw==\n')
        self.assertEqual(to_unicode(ret[0]), 'foo_key_93')

    def test_should_parse_multi_response(self):
        """ GetKeysByTagCommand().parse() should parse getKeysByTag command response(multipul keys). """
        ret = self.command.parse('4,true,Zm9vX2tleV85Mw==:Zm9vX2tleV80Mg==\n')
        self.assertEqual(to_unicode(ret[0]), 'foo_key_93')
        self.assertEqual(to_unicode(ret[1]), 'foo_key_42')
