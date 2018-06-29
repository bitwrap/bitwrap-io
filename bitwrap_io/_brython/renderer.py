from browser import window, console

class Draw(object):
    """ Use Snap.SVG to draw PNet graph """

    paper = None
    """ Snap.svg instance """

    symbols = {}
    """ svg graphic elements used to render a Petri-Net """

    @staticmethod
    def origin(x1=0, y1=0, x2=100, y2=100):
        """ draw x/y axis """

        Draw.paper.line({
            'x1': x1,
            'y1': y1,
            'x2': x2,
            'y2': 0,
        }).attr({
            'id': 'origin_x',
            'class': 'origin',
            'stroke': '#000',
            'strokeWidth': 2,
            'markerEnd': Draw.symbols['arrow']
        })

        Draw.paper.line({
            'x1': x1,
            'y1': y1,
            'x2': 0,
            'y2': y2,
        }).attr({
            'id': 'origin_y',
            'class': 'origin',
            'stroke': '#000',
            'strokeWidth': 2,
            'markerEnd': Draw.symbols['arrow']
        })

    @staticmethod
    def handle(x=0, y=50, size=40, refid=None, symbol=None, tokens=0, editor=None):
        """
        add group of elements needed for UI interaction
        here mouse events are bound to controler actions
        """

        _id = refid + '-handle'

        point = Draw.symbols[refid]
        handle = Draw.paper.g(point, Draw._label(refid))

        if symbol == 'place':
           el = Draw._place(x=x, y=y, size=size, refid=refid, symbol=symbol)
           el.data('refid', refid)
           token_el = Draw._tokens(refid, value=tokens)
           handle.add(el, token_el)
        elif symbol == 'transition':
           el = Draw._transition(x=x, y=y, size=size, refid=refid, symbol=symbol)
           handle.add(el)

        el.data('refid', refid)
        Draw.symbols[_id] = handle

        def _move_and_redraw():
            """ trigger action in UI """

            try:
                delta = handle.data('tx')

                if symbol == 'place':
                    _defs = editor.instance.place_defs
                elif symbol == 'transition':
                    _defs = editor.instance.transition_defs

                _coords = _defs[refid]['position']
                _defs[refid]['position'] = [int(_coords[0]) + delta[0], int(_coords[1]) + delta[1]]
            except:
                pass
            finally:
                editor.render()

        def _drag_start(x, y, evt):
            """ begin mouse interaction """
            editor.on_click(evt)

        def _drag_end(evt):
            """ complete mouse interaction """
            if not editor.move_enabled:
                return

            editor.reset(callback=_move_and_redraw)

        def _dragging(dx, dy, x, y, event):
            """ svg transformation while dragging """
            if not editor.move_enabled:
                return

            _tx = 't %i %i' % (dx, dy)
            handle.transform(_tx)
            handle.data('tx', [dx, dy])
        
        handle.drag(_dragging, _drag_start, _drag_end)

        return el

    @staticmethod
    def place(x, y, label=None):
        """ adds a place node """
        return Draw._node(x, y, label=label, symbol='place')

    @staticmethod
    def transition(x, y, label=None):
        """ adds a transition node """
        return Draw._node(x, y, label=label, symbol='transition')

    @staticmethod
    def arc(sym1, sym2, token_weight=1, editor=None):
        """ draw arc between 2 points """
        x1 = float(_attr(sym1).x2.value)
        y1 = float(_attr(sym1).y2.value)
        x2 = float(_attr(sym2).x2.value)
        y2 = float(_attr(sym2).y2.value)

        if Draw.symbols[sym2].data('symbol') == 'place':
            start='transition'
            end='place'
        else:
            end='transition'
            start='place'

        _id = '%s>%s' % (sym1, sym2)
        el = Draw._arc(x1, y1, x2, y2, refid=_id, start=start, weight=token_weight, end=end, editor=editor)
        el.data('symbol', 'arc')
        el.data('start', sym1)
        el.data('end', sym2)

        return el

    @staticmethod
    def _node(x, y, label=None, symbol=None):
        """ adds a petri-net symbol to the graph """

        point_el= Draw._point(x=x, y=y, refid=label)
        point_el.data('symbol', symbol)
        point_el.data('label', label)

        Draw.symbols[label] = point_el
        return point_el

    @staticmethod
    def _point(x=0, y=0, refid=None):
        """ draw hidden point """

        el = Draw.paper.line({
            'x1': 0,
            'y1': 0,
            'x2': x,
            'y2': y,
        }).attr({
            'id': refid,
            'class': 'point',
            #'stroke': '#87CDDE',
            'strokeWidth': 2
        })

        Draw.symbols[refid] = el
        return el


    @staticmethod
    def _arc(x1, y1, x2, y2, weight=1, refid=None, start=None, end=None, editor=None):
        """
        draw arc with arrow
        This also adjusts x coordintates to match place/transition size
        """

        if start == 'place':
            if x1 > x2:
                x1 = x1 - 20 
                x2 = x2 + 10
            else:
                x1 = x1 + 20
                x2 = x2 - 10

        elif end == 'place':
            if x1 > x2:
                x1 = x1 - 5 
                x2 = x2 + 20
            else:
                x1 = x1 + 5
                x2 = x2 - 20

        el = Draw.paper.line({
            'x1': x1,
            'y1': y1,
            'x2': x2,
            'y2': y2,
        }).attr({
            'id': refid,
            'class': 'arc',
            'stroke': '#000',
            'stroke-opacity': '0.8',
            'strokeWidth': 1,
            'markerEnd': Draw.symbols['arrow']
        })

        label_x = (x1 + x2) / 2 - 5
        label_y = (y1 + y2) / 2

        Draw._arc_handle(label_x, label_y, weight=weight, refid=refid, editor=editor)

        Draw.symbols[refid] = el
        return el

    def _arc_handle(label_x, label_y, weight=1, refid=None, editor=None):
        """ clickable handle to display and change arc weight """

        def _drag_start(x, y, evt):
            """ begin mouse interaction """
            editor.on_click(evt)

        # TODO add a selectable region in front of this txt
        # should trigger a dialog to change weight
        handle = Draw.paper.text(
            label_x,
            label_y - 5,
            weight
        ).attr({
            'id': refid + '-arcweight',
            'class': 'txtlabel',
            'style': 'font-size: 12; font-weight: bold; cursor: crosshair'
        })

        handle.drag(None, _drag_start, None)

    @staticmethod
    def _arrow():
        """ arrowhead """

        return Draw.paper.path(
            "M 2 59 L 293 148 L 1 243 L 121 151 Z"
        ).marker({
            'x': 0,
            'y': 0,
            'width': 8000,
            'height': 8000,
            'refX': 260,
            'refY': 150
        }).attr({
            'fill':'white',
            'stroke': 'black',
            'strokeWidth': 10,
            'markerUnits':'strokeWidth',
            'markerWidth': 350,
            'markerHeight':350,
            'orient': "auto" 
        })

    @staticmethod
    def _tokens(sym, value=0):
        """ token values """

        _id = sym + '-tokens'

        # TODO: draw numbers <= 5 as dots
        if value == 1:

            return Draw.paper.circle({
                'cx': float(_attr(sym).x2.value),
                'cy': float(_attr(sym).y2.value),
                'r': 2
            }).attr({
                'id': _id,
                'class': 'tokens',
                'fill': '#000',
                'fill-opacity': 1,
                'stroke': '#000',
                'orient': 0,
                'style': 'cursor: crosshair'
            })

        if value == 0:
            _txt = ''
        else:
            _txt = str(value)

        return Draw.paper.text(
            float(_attr(sym).x2.value),
            float(_attr(sym).y2.value),
            _txt
        ).attr({
            'id': _id,
            'class': 'txtlabel',
            'style': 'cursor: crosshair'
        })

    @staticmethod
    def _label(sym):
        """ add txt label to a symbol """
        _txt = Draw.symbols[sym].data('label')

        el = Draw.paper.text(float(_attr(sym).x2.value) - 10, float(_attr(sym).y2.value) + 35, _txt)
        el.attr({ 'class': 'label', 'style': 'font-size: 12px; cursor: default'})
        return el

    @staticmethod
    def _transition(x=0, y=50, size=40, refid=None, symbol=None):
        """ draw transition """
        _id = '%s-%s' % (refid, symbol)

        return Draw.paper.rect({
            'x': x - 5,
            'y': y - 17,
            'width': 10,
            'height': 34,
        }).attr({
            'id': _id,
            'class': symbol,
            'fill': 'black',
            'fill-opacity': 1,
            'stroke': '#000',
            'strokeWidth': 2,
            'orient': 0 
        })

    @staticmethod
    def _place(x=0, y=50, size=40, refid=None, symbol=None):
        """ draw place """

        _id = '%s-%s' % (refid, symbol)

        return Draw.paper.circle({
            'cx': x,
            'cy': y,
            'r': (size/2)
        }).attr({
            'id': _id,
            'class': symbol,
            'fill': '#FFF',
            'fill-opacity': 1,
            'stroke': '#000',
            'orient': 0 
        })


class RenderMixin(object):
    """ interface for rendering PNet as an SVG """

    def reset(self):
        """ create symbols used by editor and redraw default svg"""
        if not Draw.paper:
            Draw.paper = window.Snap('#net')

        Draw.paper.clear()

        Draw.symbols['arrow'] = Draw._arrow()
        Draw.origin()

    def render(self, token_ledger=None):
        """ draw the petri-net """
        self.draw_nodes(token_ledger=token_ledger)
        self.draw_handles()
        self.draw_arcs()

    def draw_nodes(self, token_ledger=None):
        """ draw points used to align other elements """

        for name, attr in self.place_defs.items():
            el = Draw.place(attr['position'][0], attr['position'][1], label=name)
            el.data('offset', attr['offset'])
            if not token_ledger:
                el.data('tokens', attr['initial']) 
            else:
                el.data('tokens', token_ledger[name]) 

            self.places[name] = el

        for name, attr in self.transition_defs.items():
            el = Draw.transition(attr['position'][0], attr['position'][1], label=name)
            self.transitions[name] = el

    def draw_handles(self):
        """ draw places and transitions """

        for label, pl in self.places.items():
            self.handles[label] = Draw.handle(
                x=float(pl.node.attributes.x2.value),
                y=float(pl.node.attributes.y2.value),
                refid=label,
                symbol='place',
                tokens=pl.data('tokens'),
                editor=self.editor
            )

        for label, tx in self.transitions.items():
            self.handles[label] = Draw.handle(
                x=float(tx.node.attributes.x2.value),
                y=float(tx.node.attributes.y2.value),
                refid=label,
                symbol='transition',
                editor=self.editor
            )

    def draw_arcs(self):
        """ draw the petri-net """

        for label, txns in self.arc_defs.items():
            for txn in txns:
                el = Draw.arc(txn['source'], txn['target'], token_weight=txn['weight'], editor=self.editor)
                el.data('weight', txn['weight'])
                el.data('offset', txn['offset'])
                el.data('delta', txn['delta'])
                self.arcs.append(el)

def _attr(sym):
    """ access attributes of an existing symbol """
    return Draw.symbols[sym].node.attributes
