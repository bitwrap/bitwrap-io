"""
"""
import os
from glob import glob
from bitwrap_io.machine import pnml as petrinet
from bitwrap_io.machine import dsl


def set_pnml_path(pnml_dir):
    """ set path to pnml source files """
    PTNet.pnml_path = pnml_dir

def schema_to_file(name):
    """ build schema filename from name """
    return os.path.join(PTNet.pnml_path, '%s.xml' % name)

def schema_files():
    """ list schema files """
    return glob(PTNet.pnml_path + '/*.xml')

def schema_list():
    """ list schema files """
    return [os.path.basename(xml)[:-4] for xml in schema_files()]

class PTNet(object):
    """ p/t net """

    pnml_path = os.environ.get('PNML_PATH', os.path.abspath(__file__ + '/../../../schemata'))

    def __init__(self, name):
        self.name = name
        self.places = None
        self.transitions = None
        self.filename = schema_to_file(name)
        self.net = petrinet.parse_pnml_file(self.filename)[0]

        def reindex():
            """ rebuild net """

            self.places = dsl.places(self.net)
            self.transitions = dsl.transitions(self.net, self.places)
            dsl.apply_edges(self.net, self.places, self.transitions)

        reindex()


    def empty_vector(self):
        """ return an empty state-vector """
        return [0] * len(self.places)

    def initial_vector(self):
        """ return initial state-vector """
        vector = self.empty_vector()

        for _, place in self.places.items():
            vector[place['offset']] = place['initial']

        return vector

    def to_machine(self):
        """ open p/t-net """

        return {
            'state': self.initial_vector(),
            'transitions': self.transitions
        }
