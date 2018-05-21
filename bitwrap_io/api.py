# -*- coding: utf-8 -*-
"""
Provide resources for bitwrap HTTP API
"""
import os
import json

from flask import Flask, request
from flask_restful import Resource, Api
from flask_cors import CORS, cross_origin

import bitwrap_io.machine as pnml
from bitwrap_io.machine import ptnet
from bitwrap_io.rpc import eventstore, call

app = Flask(__name__)
api = Api(app)
CORS(app)
VERSION = 'v0.3.0'

# TODO: does Resource allow for Etags?

class Rpc(Resource):

    def post(self):
        """
        handle rpc calls

        will accept post body
        or
        form encoded request with a field called 'json'
        """
        res = {}
        req = {}

        try:
            if request.data == '':
              payload = request.form.get('json')
            else:
              payload = request.data

            req = json.loads(payload)
            res['id'] = req.get('id')
            res['result'] = call(req['method'], req['params'])
            res['error'] = None
        except Exception as ex:
            msg = str(ex).splitlines()[0]
            res = {'id': req.get('id'), 'error': msg}

        return res, 200, None


class Dispatch(Resource):

    def post(self, schema, oid, action):
        if not request.data:
            event = request.form.get('json')
        else:
            event = request.data

        if not event:
            event = '{}'

        if type(event) is bytes:
            _payload = event.decode('utf8')
        else:
            _payload = event

        res = eventstore(schema)(oid=oid, action=action, payload=_payload)
        return res, 200, None

class Event(Resource):

    def get(self, schema, eventid):
        res = eventstore(schema).storage.db.events.fetch(eventid)
        return res, 200, None

class Machine(Resource):

    def get(self, schema):
        machine = pnml.Machine(schema)
        res = {
            'machine': {
                'name': schema,
                'places': machine.net.places,
                'transitions': machine.net.transitions
            }
        }

        return res, 200, None

class Schemata(Resource):

    def get(self):
        res = {'schemata': ptnet.schema_list()}
        return res, 200, None

class State(Resource):

    def get(self, schema, oid):
        res = eventstore(schema).storage.db.states.fetch(oid)
        return res, 200, None

class Stream(Resource):

    def get(self, schema, streamid):
        res = eventstore(schema).storage.db.events.fetchall(streamid)
        return res, 200, None

class Config(Resource):
    """ config """

    def get(self, stage):
        """ direct web app to api """

        res = {
            'endpoint': os.environ.get('ENDPOINT', ''),
            'version': VERSION,
            'stage': stage,
            'use_websocket': False # no clean integration w/ Twisted/Flask websockets investating porting to asyncio
        }
        return res, 200, None

def __load_routes():
    """ load resource routes """

    routes = [
        dict(resource=Dispatch, urls=['/dispatch/<schema>/<oid>/<action>'], endpoint='dispatch'),
        dict(resource=State, urls=['/state/<schema>/<oid>'], endpoint='state'),
        dict(resource=Machine, urls=['/machine/<schema>'], endpoint='machine'),
        dict(resource=Event, urls=['/event/<schema>/<eventid>'], endpoint='event'),
        dict(resource=Stream, urls=['/stream/<schema>/<streamid>'], endpoint='stream'),
        dict(resource=Schemata, urls=['/schemata'], endpoint='schemata'),
        dict(resource=Rpc, urls=['/api'], endpoint='api'),
        dict(resource=Config, urls=['/config/<stage>.json'], endpoint='config')
    ]

    for route in routes:
        api.add_resource(route.pop('resource'), *route.pop('urls'), **route)

__load_routes()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
