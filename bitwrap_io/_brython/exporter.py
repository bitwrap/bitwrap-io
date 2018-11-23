""" Export Petri-Net as xml/PNML """

from browser import window 

class Export(object):

    header = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'

    def __init__(self, instance):
        self.instance = instance

    def _append_places(self, doc, net):
        for name  in sorted(self.instance.place_defs.keys()):
            attr = self.instance.place_defs[name]

            place = doc.createElement('place')
            place.setAttribute('id', name)
            net.appendChild(place)

            graphics = doc.createElement('graphics')
            pos = doc.createElement('position')
            pos.setAttribute('x', attr['position'][0])
            pos.setAttribute('y', attr['position'][1])
            graphics.appendChild(pos)
            place.appendChild(graphics)

            name_el = doc.createElement('name')
            graphics = doc.createElement('graphics')
            pos = doc.createElement('offset')
            pos.setAttribute('x', '0.0')
            pos.setAttribute('y', '0.0')
            graphics.appendChild(pos)
            name_el.appendChild(graphics)
            val = doc.createElement('value')
            val.appendChild(doc.createTextNode(name))
            name_el.appendChild(val)
            place.appendChild(name_el)

            capacity = doc.createElement('capacity')
            val = doc.createElement('value')
            val.appendChild(doc.createTextNode('0'))
            capacity.appendChild(val)
            place.appendChild(capacity)

            initial = doc.createElement('initialMarking')
            graphics = doc.createElement('graphics')
            pos = doc.createElement('offset')
            pos.setAttribute('x', '0.0')
            pos.setAttribute('y', '0.0')
            graphics.appendChild(pos)
            initial.appendChild(graphics)
            val = doc.createElement('value')
            val.appendChild(doc.createTextNode('Default,%i' % attr['initial']))
            initial.appendChild(val)
            place.appendChild(initial)

    def _append_transitions(self, doc, net):

        for name, attr  in self.instance.transition_defs.items():
            txn = doc.createElement('transition')
            txn.setAttribute('id', name)
            net.appendChild(txn)

            graphics = doc.createElement('graphics')
            pos = doc.createElement('position')
            pos.setAttribute('x', attr['position'][0])
            pos.setAttribute('y', attr['position'][1])
            graphics.appendChild(pos)
            txn.appendChild(graphics)

            name_el = doc.createElement('name')
            val = doc.createElement('value')
            val.appendChild(doc.createTextNode(name))
            graphics = doc.createElement('graphics')
            pos = doc.createElement('offset')
            pos.setAttribute('x', '0.0')
            pos.setAttribute('y', '0.0')
            graphics.appendChild(pos)
            name_el.appendChild(graphics)
            name_el.appendChild(val)
            txn.appendChild(name_el)

            infinite_srv = doc.createElement('infiniteServer')
            val = doc.createElement('value')
            val.appendChild(doc.createTextNode('false'))
            infinite_srv.appendChild(val)
            txn.appendChild(infinite_srv)

            timed = doc.createElement('timed')
            val = doc.createElement('value')
            val.appendChild(doc.createTextNode('false'))
            timed.appendChild(val)
            txn.appendChild(timed)

            priority = doc.createElement('priority')
            val = doc.createElement('value')
            val.appendChild(doc.createTextNode(1))
            priority.appendChild(val)
            txn.appendChild(priority)

            orientation = doc.createElement('orientation')
            val = doc.createElement('value')
            val.appendChild(doc.createTextNode(0))
            orientation.appendChild(val)
            txn.appendChild(orientation)

            rate = doc.createElement('rate')
            val = doc.createElement('value')
            val.appendChild(doc.createTextNode('1.0'))
            rate.appendChild(val)
            txn.appendChild(rate)

    def _arcpath(self, doc, arc, label=None, x=None, y=None):
        arcpath = doc.createElement('arcpath')
        arcpath.setAttribute('id', label)
        arcpath.setAttribute('x', x)
        arcpath.setAttribute('y', y)
        arcpath.setAttribute('curvepoint', 'false')
        arc.appendChild(arcpath)

    def _append_arcs(self, doc, net):
        for txn_name, arcs  in self.instance.arc_defs.items():
            for attr in arcs:
                arc = doc.createElement('arc')
                arc.setAttribute('id', attr['source'] + ' to ' + attr['target'])
                arc.setAttribute('source', attr['source'])
                arc.setAttribute('target', attr['target'])
                net.appendChild(arc)
                
                if txn_name == attr['target']:
                    target = self.instance.transition_defs[attr['target']]
                    source = self.instance.place_defs[attr['source']]
                else:
                    target = self.instance.place_defs[attr['target']]
                    source = self.instance.transition_defs[attr['source']]

                self._arcpath(doc, arc, label='source', x=source['position'][0], y=source['position'][1])
                self._arcpath(doc, arc, label='target', x=target['position'][0], y=target['position'][1])

                _type = doc.createElement('type')
                _type.setAttribute('value', 'normal')
                arc.appendChild(_type)

                inscription = doc.createElement('inscription')
                val = doc.createElement('value')
                val.appendChild(doc.createTextNode('Default,%i' % attr['weight']))
                inscription.appendChild(val)
                arc.appendChild(inscription)

    def to_xml(self):
        doc = window.document.implementation.createDocument(None, 'export', None)
        pnml = doc.createElement('pnml')
        doc.documentElement.appendChild(pnml)

        net = doc.createElement('net')
        pnml.appendChild(net)

        # NOTE: only support a single 'Default' token color
        token = doc.createElement('token')
        token.setAttribute('id', 'Default')
        token.setAttribute('red', '0')
        token.setAttribute('green', '0')
        token.setAttribute('blue', '0')
        net.appendChild(token)

        self._append_places(doc, net)
        self._append_transitions(doc, net)
        self._append_arcs(doc, net)

        return self.header + pnml.outerHTML

