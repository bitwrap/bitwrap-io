from unittest import TestCase
from bitwrap_io import rpc

class StreamTest(TestCase):
    """ setup rpc endpoint and invoke ping method """

    machine = 'counter'
    """ name of state machine """

    schema = 'trial'
    """ name of db schema """

    stream = 'foo'
    """ name of stream """

    num_events = 10
    """ number of events to generate in test """

    def setUp(self):
        """ build a sample eventstream """
        self.events = []

        rpc.rpc_schema_destroy(self.schema)
        self.assertTrue(rpc.rpc_schema_create(self.machine, self.schema))
        self.assertTrue(rpc.rpc_schema_exists(self.schema))
        self.assertTrue(rpc.rpc_stream_create(self.schema, self.stream))
        self.assertTrue(rpc.rpc_stream_exists(self.schema, self.stream))

        self.count_event = rpc.eventstore(self.schema)
        for _ in range(0, self.num_events):
            self.events.append(self.count_event(oid='foo', action='INC_0', payload='{"testing": "foo"}'))

    def test_eventstream(self):
        """ query eventstream """
        eventstream = self.count_event.storage.db.events.fetchall('foo')
        self.assertEqual(len(eventstream), self.num_events)

    def test_event_by_id(self):
        """ get single event """
        first_event = self.count_event.storage.db.events.fetch(self.events[0]['id'])

        self.assertEqual(first_event['id'], self.events[0]['id'])
        self.assertEqual(first_event['seq'], 1)
        self.assertEqual(first_event['oid'], self.stream)
        self.assertEqual(first_event['action'], 'INC_0')
        self.assertEqual(first_event['payload']['testing'], 'foo')
        self.assertTrue('timestamp' in first_event)

    def test_state(self):
        """ get state of stream """
        state = self.count_event.storage.db.states.fetch('foo')
        last_seq = self.num_events - 1
        last_event = self.count_event.storage.db.events.fetch(self.events[last_seq]['id'])

        self.assertTrue(state['id'], last_event['id'])
        self.assertEqual(state['rev'], 10)
        self.assertEqual(state['oid'], self.stream)
        self.assertEqual(state['action'], 'INC_0')
        self.assertEqual(state['payload']['testing'], 'foo')
        self.assertEqual(state['modified'], last_event['timestamp'])
        self.assertTrue('created' in state)

