from abc import ABC, abstractmethod

class Learner(ABC):
    @abstractmethod
    def induce(self, examples, modes, knowledge, solver, options=None):
        pass