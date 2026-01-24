from ..constraints.constraints import constraints
class Pair: # For nC2 combinations. 
    def __init__(self, w1, w2):
        self.w1 = w1 # Word 1, obviously
        self.w2 = w2 # Word 2, obviously 
        self.difference = self.w1.position - self.w2.position
    def apply_constraints(self):
        for constraint in constraints: # Loops through list of instances of object Constraint 
            if constraint.applies(self): # Checks if self.check returns True 
                constraint.apply(self) # Does everything it needs to