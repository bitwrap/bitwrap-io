from unittest  import TestCase
from bitwrap_io import rpc

class CommitTest(TestCase):
    """ setup rpc endpoint and invoke ping method """

    machine = 'counter'
    schema = 'trial'
    stream = 'foo'

    def setUp(self):
        rpc.rpc_schema_destroy(self.schema)
        self.assertTrue(rpc.rpc_schema_create(self.machine, self.schema))

    def tearDown(self):
        pass

    def test_rpc_operations(self):
        """ test schema & stream creation """
        self.assertTrue(rpc.rpc_schema_exists(self.schema))
        self.assertTrue(rpc.rpc_stream_create(self.schema, self.stream))
        self.assertTrue(rpc.rpc_stream_exists(self.schema, self.stream))

    def test_commit_missing_stream(self):
        """ try to append an event to a stream that doesn't exist """
        count_event = rpc.eventstore(self.schema)
        res = count_event(oid='foo', action='INC_0')
        self.assertTrue('id' not in res)
        self.assertEqual(res['__err__'], 'INVALID_INPUT')

    def test_commit_unknown_action(self):
        """ try to append an event to a stream that doesn't exist """
        self.assertTrue(rpc.rpc_stream_create(self.schema, self.stream))
        count_event = rpc.eventstore(self.schema)

        res = count_event(oid='foo', action='ACTION_THAT_DOES_NOT_EXIST')
        self.assertTrue('id' not in res)
        self.assertEqual(res['__err__'], 'INVALID_INPUT')

    def test_commit_invalid_action(self):
        """
        try to trigger an action that results in a negative (invalid) output
        """
        self.assertTrue(rpc.rpc_stream_create(self.schema, self.stream))
        count_event = rpc.eventstore(self.schema)

        res = count_event(oid='foo', action='DEC_0')
        self.assertTrue('id' not in res)
        self.assertEqual(res['__err__'], 'INVALID_OUTPUT')

    def test_valid_commit(self):
        """ append event to eventstore db with pre-existing stream"""
        self.assertTrue(rpc.rpc_stream_create(self.schema, self.stream))

        count_event = rpc.eventstore(self.schema)
        res = count_event(oid='foo', action='INC_0')

        self.assertTrue('__err__' not in res)
        self.assertTrue('id' in res)
        self.assertEqual(res['rev'], 1)
        self.assertEqual(res['oid'], self.stream)

        res = count_event(oid='foo', action='INC_0')

        self.assertTrue('__err__' not in res)
        self.assertTrue('id' in res)
        self.assertEqual(res['rev'], 2)
        self.assertEqual(res['oid'], self.stream)
