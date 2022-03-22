from collections import OrderedDict

class LiveLog:
    """ """
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
        self.data[event_id] = value
        
    def __repr__(self):
        header = self.__class__.__name__        
        tab = ' '*3
        data = '\n'.join([tab+'%s: %s' % (repr(key), repr(value)) for key, value in self._data.items()])
        return '%s\n%s' % (header, data)
