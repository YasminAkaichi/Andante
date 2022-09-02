"""
License
-------

This software is distributed under the terms of both the MIT license and the
Apache License (Version 2.0).

See LICENSE for details.

Acknowlegment
-------------

This software has benefited from the support of Wallonia thanks to the funding
of the ARIAC project (https://trail.ac), a project part of the
DigitalWallonia4.ai initiative (https://www.digitalwallonia.be).

It was done by Simon Jacquet at the University of Namur (https://www.unamur.be)
in the period of October 1st 2021 to August 31st 2022 under the supervision of
Isabelle Linden, Jean-Marie Jacquet and Wim Vanhoof. 
"""

from collections import OrderedDict

class LiveLog:
    """ Log for storing information during the learning of clauses """
    def __init__(self, parent=None):
        self._data = OrderedDict()
        self.pointer = self
        self.parent = parent
        
    @property
    def data(self): return self.pointer._data
        
    def beg_child(self, name, point_to_child=True):
        child = LiveLog(self.pointer)
        self.add_eventlog(name, child)
        if point_to_child:
            self.pointer = child
            
    def end_child(self):
        self.pointer = self.pointer.parent
        
    def add_eventlog(self, event_id, value):
        if event_id not in self.data:
            self.data[event_id] = value
        
    def __repr__(self):
        header = self.__class__.__name__        
        tab = ' '*3
        data = '\n'.join([tab+'%s: %s' % (repr(key), repr(value)) for key, value in self._data.items()])
        return '%s\n%s' % (header, data)

