from aloe.clause import Operator, Constant, Variable
from aloe.variablebank import VariableBank

class ModeHandler:
    def __init__(self, modes=None, determinations=None, options=None):
        """
        Inputs:
            -modes: list of all modes
            -determinations: dict: modeh -> list of modeb
        """
        modes = modes or []
        determinations = determinations or []
        
        self.modeh = {mode.deterform():mode for mode in modes if isinstance(mode, Modeh)}
        self.modeb = {mode.deterform():mode for mode in modes if isinstance(mode, Modeb)}

        self.determinations = dict()
        for (deterh, l_deterb) in determinations:
            # Check for error in mode declarations vs determinations
            if deterh not in self.modeh:
                raise Exception("%s present in declaration(%s,%s) does not correspond to any modeh." 
                                % (deterh,deterh,','.join(l_deterb)))
            for deterb in l_deterb:
                if deterb not in self.modeb:
                    raise Exception("%s present in declaration(%s,%s) does not correspond to any modeb." 
                                    % (deterh,deterh,','.join(l_deterb)))

            if not deterh in self.determinations:
                self.determinations[deterh] = set()
            self.determinations[deterh].update(l_deterb)
            
    def modeb4modeh(self, modeh):
        deterh = modeh if isinstance(modeh, str) else modeh.determform()
        if deterh in self.determinations:
            return [self.modeb[deterb] for deterb in self.determinations[deterh]]
        else:
            return [value for _, value in self.modeb.items()]
            
    def __repr__(self):
        
        return 'modeh: %s\nmodeb: %s\ndeterminations: %s' % (repr(self.modeh), 
                                                             repr(self.modeb),
                                                             repr(self.determinations))
    


            
class Mode:
    def __init__(self, recall, atom):
        self.recall = recall
        self.atom   = atom
        
    def atom_arity(self):
        return self.atom.arity
    
    def deterform(self):
        """ 
        Determination form of a mode
        Ex: Input: modeh(*,parent_of(+person,-person)) (as a Mode object)
            Ouput: 'parent_of/2' (string)
        """
        return "%s/%d" % (self.atom.name, self.atom_arity())
        
class Modeh(Mode):
    def __repr__(self):
        return 'modeh(%s,%s).' % (repr(self.recall), repr(self.atom))
class Modeb(Mode):
    def __repr__(self):
        return 'modeb(%s,%s).' % (repr(self.recall), repr(self.atom))

class Type:
    def __init__(self, prefix, name):
        self.prefix = prefix
        self.name   = name
        
    def __repr__(self):
        return self.prefix+str(self.name)            